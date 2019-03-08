from flask import Flask, request
from flask_uploads import UploadSet, IMAGES, configure_uploads

app = Flask(__name__)

from fsdemo.index import index_page
from fsdemo.gallery import gallery_page
from fsdemo.blog import blog_page
from fsdemo.exceljson import exceljson_page
from fsdemo.config import InitApp

InitApp()
app.config.from_object('fsdemo.config.AppConfig')
app.register_blueprint(index_page, url_prefix='/')
app.register_blueprint(gallery_page, url_prefix='/gallery')
app.register_blueprint(blog_page, url_prefix='/blog')
app.register_blueprint(exceljson_page, url_prefix='/exceljson')

'''
    Since the module 'flask-uploads' cannot be used in blueprint.
    The upload router has to be put into this main process.
'''
photos = UploadSet('photos', IMAGES)
configure_uploads(app, (photos))

@app.route('/do/upload', methods=['POST'])
def do_upload():
    returnmsg = 'upload started.'
    # print(request.form.getlist('tags'))
    # print(request.form['caption'])
    if 'photo' in request.files:
        try:
            filename = photos.save(request.files['photo'])
            returnmsg = photos.url(filename)
        except:
            returnmsg = 'Error occurred\n\n' + \
                'Details: the file is not an image.\n\n' + \
                'Or the file size exceeded maximum allowed size [' + \
                '{0}'.format(app.config['MAX_CONTENT_LENGTH'] / 1024 / 1024) +' MB].'
            pass
    return returnmsg
