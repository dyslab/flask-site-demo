from flask import Blueprint, render_template
from fsdemo.pagedata.gallery import GalleryUploadPageData

gallery_page = Blueprint('gallery', __name__, static_folder='static', template_folder='templates')

@gallery_page.route('/upload', methods=['GET', 'POST'])
def gallery_upload():
    return render_template('gallery_item.html', action='UPLOAD', pageData=GalleryUploadPageData())
