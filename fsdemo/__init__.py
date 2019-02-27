from flask import Flask, render_template
from fsdemo.pagedata.index import *
from fsdemo.pagedata.about import *

app = Flask(__name__)

from fsdemo.gallery import gallery_page
app.register_blueprint(gallery_page, url_prefix='/gallery')

@app.route('/')
def index(pageTitle = None):
    indexData = IndexPageData()
    return render_template('index.html', pageData = indexData)

@app.route('/about')
def about(pageTitle = None):
    aboutData = AboutPageData()
    return render_template('about.html', pageData = aboutData)
