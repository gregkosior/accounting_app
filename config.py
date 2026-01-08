import os

class Config:
    SECRET_KEY = 'your_secret_key'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'data', 'uploads')
    ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
