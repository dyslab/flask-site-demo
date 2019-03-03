from flask import Blueprint, render_template
from fsdemo.pagedata.gallery import GalleryPageData

gallery_page = Blueprint('gallery', __name__, static_folder='static', template_folder='templates')

@gallery_page.route('/', methods=['GET', 'POST'])
def gallery_index():
    return render_template('gallery_index.html', pageData=GalleryPageData())
