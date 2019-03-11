from flask import Blueprint, render_template, request, current_app
from fsdemo.response import JsonResponse
from fsdemo.pagedata.blog import BlogPageData, BTagsMiddleware, BlogMiddleware

blog_page = Blueprint(
    'blog',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@blog_page.route('/', methods=['GET', 'POST'])
def blog_index():
    return render_template('blog_index.html', pageData=BlogPageData())


@blog_page.route('/save/tags', methods=['POST'])
def blog_save_tags():
    res = JsonResponse()
    try:
        tags = request.form.getlist('tags[]')
        tags.reverse()
        if BTagsMiddleware().save_all_to_db(tags):
            res.resMsg = 'Note: Tags saved successfully.'
        else:
            res.resMsg = 'Note: Failed to save tags.'
    except Exception as e:
        res.resCode = -1
        res.resMsg = e.args.__name__
        pass
    return res.outputJsonString()


@blog_page.route('/new', methods=['POST'])
def blog_new():
    res = JsonResponse()
    try:
        bitem = BlogMiddleware(
            title=request.form['blogtitle'],
            tags=request.form.getlist('tags'),
            content=request.form['blogcontent']
        )
        if bitem.save_to_db():
            res.resMsg = 'Note: New blog saved successfully.'
        else:
            res.resMsg = 'Note: Failed to save the blog.'
        # res.data = bitem.outputDict()
    except Exception:
        res.resCode = -1
        res.resMsg = 'Error: Network failed.' + \
            ' Check your network connection please.'
        pass
    # print(res.outputJsonString()) # Print for test.
    return res.outputJsonString()


@blog_page.route('/loadmore/<int:page>', methods=['GET'])
def blog_loadmore(page):
    res = JsonResponse()
    try:
        blist = BlogMiddleware().load_from_db(
            page, current_app.config['BLOG_PER_PAGE']
        )
        res.data = blist
        # print(res.data)  # Print for test.
    except Exception:
        res.resCode = -1
        res.resMsg = 'Error: Network failed.' + \
            ' Check your network connection please.'
        pass
    # print(res.outputJsonString())  # Print for test.
    return res.outputJsonString()
