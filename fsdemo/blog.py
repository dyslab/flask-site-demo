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
        if BTagsMiddleware().save_all(tags):
            res.resMsg = 'Note: Tags saved successfully.'
        else:
            res.resMsg = 'Note: Failed to save tags.'
    except Exception:
        res.resCode = -1
        res.resMsg = "Network error occurred."
        pass
    return res.outputJsonString()


@blog_page.route('/new', methods=['POST'])
def blog_new():
    res = JsonResponse()
    try:
        bflag = BlogMiddleware().save_one(
            title=request.form['blogtitle'],
            tags=request.form.getlist('tags'),
            content=request.form['blogcontent']
        )
        if bflag:
            res.resMsg = 'Note: New blog saved successfully.'
        else:
            res.resMsg = 'Note: Failed to save the blog.'
    except Exception:
        res.resCode = -1
        res.resMsg = 'Error: Network failed.' + \
            ' Check your network connection please.'
        pass
    # print(res.outputJsonString()) # Print for test.
    return res.outputJsonString()


@blog_page.route('/edit/<int:id>', methods=['GET'])
def blog_edit(id):
    res = JsonResponse()
    try:
        blog = BlogMiddleware().load_by_id(id=id)
        if blog is not None:
            res.data = blog
    except Exception:
        res.resCode = -1
        res.resMsg = 'Error: Network failed.' + \
            ' Check your network connection please.'
        pass
    # print(res.outputJsonString()) # Print for test.
    return res.outputJsonString()


@blog_page.route('/delete/<int:id>', methods=['GET'])
def blog_delete(id):
    res = JsonResponse()
    try:
        bflag = BlogMiddleware().delete_by_id(id=id)
        if bflag:
            res.resMsg = 'Note: Blog deleted successfully.'
        else:
            res.resMsg = 'Note: Failed to delete the blog.'
    except Exception:
        res.resCode = -1
        res.resMsg = 'Error: Network failed.' + \
            ' Check your network connection please.'
        pass
    # print(res.outputJsonString()) # Print for test.
    return res.outputJsonString()


@blog_page.route('/edit/save', methods=['POST'])
def blog_edit_save():
    res = JsonResponse()
    try:
        bflag = BlogMiddleware().save_by_id(
            id=int(request.form['blogid']),
            title=request.form['blogtitle'],
            tags=request.form.getlist('tags'),
            content=request.form['blogcontent']
        )
        if bflag:
            res.resMsg = 'Note: Blog saved successfully.'
        else:
            res.resMsg = 'Note: Failed to edit the blog.'
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
        off = int(request.args.get('off', '0'))
        blist = BlogMiddleware().load_all(
            page, off, current_app.config['BLOG_PER_PAGE']
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


@blog_page.route('/search', methods=['POST'])
def blog_search():
    res = JsonResponse()
    try:
        blist = BlogMiddleware().search(
            1, 0, current_app.config['BLOG_PER_PAGE'],
            request.form.getlist('searchtags'),
            request.form['searchterms'],
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


@blog_page.route('/search/loadmore/<int:page>', methods=['GET', 'POST'])
def blog_search_loadmore(page):
    res = JsonResponse()
    try:
        off = int(request.args.get('off', '0'))
        blist = BlogMiddleware().search(
            page, off, current_app.config['BLOG_PER_PAGE'],
            request.form.getlist('searchtags'),
            request.form['searchterms'],
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
