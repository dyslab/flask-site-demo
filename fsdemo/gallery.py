from flask import Blueprint, redirect, render_template, url_for
from fsdemo.pagedata.gallery import GalleryUploadPageData

gallery_page = Blueprint('gallery', __name__, static_folder='static', template_folder='templates')

@gallery_page.route('/upload', methods=['GET', 'POST'])
def gallery_upload():
    # print(current_app.config['UPLOADS_DEFAULT_DEST'])
    return render_template('gallery_item.html', action='UPLOAD', pageData=GalleryUploadPageData())

@gallery_page.route('/show/<path:fullpath>', methods=['GET'])
def gallery_show_uploadfiles(fullpath):
    return redirect(url_for('static', filename=fullpath))
