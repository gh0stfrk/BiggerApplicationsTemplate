import os 
from .. import app_dir

class Config:
    MEDIA_DIR = os.getenv('MEDIA_DIR', os.path.join(app_dir, 'media'))
    ALLOWED_IMAGE_TYPES = ['image/png', 'image/jpg', 'image/jpeg']
    MAX_IMAGE_SIZE = 24000
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    ALGORITHM = os.getenv('ALGORITHM', 'HS256')