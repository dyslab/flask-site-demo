from flask import Blueprint, render_template
from fsdemo.pagedata.blog import BlogPageData

blog_page = Blueprint('blog', __name__, static_folder='static', template_folder='templates')

@blog_page.route('/', methods=['GET', 'POST'])
def blog_index():
    return render_template('blog_index.html', pageData=BlogPageData())
