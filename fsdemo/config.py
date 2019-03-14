import os


class Config(object):
    '''
        The configured file of this APP.
    '''
    # Base configuration
    SECRET_KEY = 'dev'
    DEBUG = False

    # Database configuration
    DATABASE_DEST = 'fsdemo/db'
    DATABASE_FILENAME = 'gblog.db'
    DATABASE_URI = 'sqlite:///' + \
        os.path.join(os.getcwd(), DATABASE_DEST, DATABASE_FILENAME)

    # Gallery configuration
    GALLERY_PER_PAGE = 18

    # Gallery Upload configuration
    UPLOADED_PHOTOS_DEST = 'fsdemo/static/uploadfiles/photos'
    UPLOADED_PHOTOS_URL = '/gallery/show/uploadfiles/photos/'
    # UPLOADS_DEFAULT_DEST = 'fsdemo/static/uploadfiles'
    # UPLOADS_DEFAULT_URL = '/gallery/show/uploadfiles'
    # Limited size of upload file is 10MB.
    MAX_CONTENT_LENGTH_MB = 10
    MAX_CONTENT_LENGTH = MAX_CONTENT_LENGTH_MB * 1024 * 1024

    # Blog configuration
    BLOG_PER_PAGE = 10
