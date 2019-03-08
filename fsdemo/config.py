import os

class AppConfig(object):
    '''
        The configured file of this APP.
    '''
    # Base configuration
    SECRET_KEY = 'dev'
    DEBUG = False
    DATABASE_URI = 'sqlite:///:memory:'

    # Upload configuration
    UPLOADS_DEFAULT_DEST = 'fsdemo/static/uploadfiles'
    UPLOADS_DEFAULT_URL = '/gallery/show/uploadfiles'
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024   # Limited size of upload file is 10MB.

class InitApp(AppConfig):
    def __init__(self):
        try:
            os.makedirs(os.path.join(os.getcwd(), self.UPLOADS_DEFAULT_DEST))
        except OSError:
            pass
        print('Folder [%s] created.' % (self.UPLOADS_DEFAULT_DEST), end='\n')
        print('Initialization done.')
