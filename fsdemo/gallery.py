from flask import Blueprint, render_template
from fsdemo.pagedata.base import PageData

gallery_page = Blueprint('gallery', __name__, static_folder='static', template_folder='templates')

@gallery_page.route('/')
def gallery_index():
    return render_template('gallery_index.html', pageData=PageData())
