
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from .models import UploadedFile, User
from .serializers import UserSerializer, FileSerializer
from .permissions import IsClientUser
from .utils import generate_signed_url, verify_signed_url

# Signup
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        signed = generate_signed_url(user.id)
        # simulate sending verification email
        print(f"Verification token for {user.email}: {signed}")

# Verify Email
@api_view(['GET'])
def verify_email(request, token):
    user_id = verify_signed_url(token, max_age=3600)
    if not user_id:
        return Response({"error": "invalid or expired"}, status=400)
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.is_verified = True
    user.save()
    return Response({"message": "email verified"})

# Upload (admin/staff only)
class UploadView(generics.CreateAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise ValidationError("Only admin/staff can upload files.")
        ext = self.request.FILES['file'].name.split(".")[-1].lower()
        if ext not in ['pptx', 'docx', 'xlsx']:
            raise ValidationError("Only pptx, docx, xlsx allowed.")
        serializer.save(uploader=self.request.user)

# List files (client only)
class ListFilesView(generics.ListAPIView):
    queryset = UploadedFile.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, IsClientUser]

# Generate download link (client only)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsClientUser])
def get_download_link(request, pk):
    signed = generate_signed_url(pk)
    return Response({
        "download_link": f"/api/download-file/{signed}",
        "message": "success"
    })

# Download file (client only)
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated, IsClientUser])
def download_file(request, token):
    file_id = verify_signed_url(token, max_age=600)
    if not file_id:
        return Response({"error": "invalid/expired"}, status=400)
    file = UploadedFile.objects.get(id=file_id)
    return Response({"message": f"Download {file.file.url} (you can serve the file here)"})
