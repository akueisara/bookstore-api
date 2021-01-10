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

UPLOAD_PHOTO_APIKEY = "d394465f8ceddab5768cbdc533549c39"
UPLOAD_PHOTO_URL = f"https://api.imgbb.com/1/upload?key={UPLOAD_PHOTO_APIKEY}"

REDIS_URL = "redis://localhost"

TESTING = True

TEST_DB_HOST = "localhost"
TEST_DB_USER = "test"
TEST_DB_PASSWORD = "test"
TEST_DB_NAME = "test"
TEST_DB_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/{TEST_DB_NAME}"
