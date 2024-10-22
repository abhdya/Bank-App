from itsdangerous import URLSafeTimedSerializer
from fastapi.templating import Jinja2Templates


templates = Jinja2Templates(directory="templates")

# SECRET_KEY and SALT for token generation
SECRET_KEY = "supersecretkey"
SALT = "emailsalt"

s = URLSafeTimedSerializer(SECRET_KEY)