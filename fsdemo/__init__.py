from flask import Flask, request
import os

def create_app():
    app = Flask(__name__)

    from fsdemo.index import index_page
    from fsdemo.gallery import gallery_page
    from fsdemo.blog import blog_page
    from fsdemo.exceljson import exceljson_page

    app.config.from_object('fsdemo.config.Config')
    app.register_blueprint(index_page, url_prefix='/')
    app.register_blueprint(gallery_page, url_prefix='/gallery')
    app.register_blueprint(blog_page, url_prefix='/blog')
    app.register_blueprint(exceljson_page, url_prefix='/exceljson')

    InitApp(app)

    return app

from fsdemo.db import db_session

def InitApp(app):
    try:
        os.makedirs(os.path.join(os.getcwd(), app.config['UPLOADS_DEFAULT_DEST']))
    except OSError:
        pass
    print(' * Folder [%s] created.' % app.config['UPLOADS_DEFAULT_DEST'])

    try:
        os.makedirs(os.path.join(os.getcwd(), app.config['DATABASE_DEST']))
    except OSError:
        pass
    print(' * Folder [%s] created.' % app.config['DATABASE_DEST'])
    print(' * Database [%s] is ready.' % app.config['DATABASE_URI'])
    
    app.teardown_appcontext(shutdown_session)
    
    print(' * App initialization done.')

def shutdown_session(exception=None):
    db_session.remove()
