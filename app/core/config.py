from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer



SECRET_KEY = "codewithamit"
ALGORITHM = "HS256"
TOKEN_EXPIRES = 30

pwd_context = CryptContext(schemes=['bcrypt'],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "token")