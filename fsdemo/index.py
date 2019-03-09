from flask import Blueprint, render_template, current_app

index_page = Blueprint('index', __name__, static_folder='static', template_folder='templates')

@index_page.route('/')
def index(pageTitle = None):
    from fsdemo.pagedata.index import IndexPageData
    indexData = IndexPageData()
    return render_template('index.html', pageData = indexData)

@index_page.route('/about')
def about(pageTitle = None):
    from fsdemo.pagedata.about import AboutPageData
    aboutData = AboutPageData()
    return render_template('about.html', pageData = aboutData) 
