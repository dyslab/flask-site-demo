from flask import Blueprint, render_template, request
from fsdemo.response import JsonResponse
from fsdemo.pagedata.blog import BlogPageData, BTagsMiddleware

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
