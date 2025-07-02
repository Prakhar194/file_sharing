from itsdangerous import URLSafeTimedSerializer

SECRET = "supersecretlink"
s = URLSafeTimedSerializer(SECRET)

def generate_signed_url(file_id):
    return s.dumps(file_id)

def verify_signed_url(token, max_age=600):
    try:
        return s.loads(token, max_age=max_age)
    except Exception:
        return None
