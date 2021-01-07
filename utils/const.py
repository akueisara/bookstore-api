JWT_SECRET_KEY = "3d4f603fecdbae76c9cac5871c379bced62e604def86424ebaa17e9c2094fe91"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_TIME_MINUTES = 60 * 24 * 5 # 5 days

TOKEN_DESCRIPTION = "It checks username and password if they are true, it returns a JWT to you."
TOKEN_SUMMARY = "It returns a JWT."

ISBN_DESCRIPTION = "It is a unique identifier for books"

DB_HOST = "localhost"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_NAME = "bookstore"
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
