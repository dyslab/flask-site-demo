from flask import Blueprint, request, redirect, render_template
from flask import url_for, current_app
from flask_uploads import UploadSet, IMAGES, configure_uploads
from fsdemo.pagedata.gallery import GalleryUploadPageData
from fsdemo.response import JsonResponse
from fsdemo.pagedata.gallery import GTagsMiddleware, GalleryMiddleware

gallery_page = Blueprint(
    'gallery',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@gallery_page.route('/upload', methods=['GET', 'POST'])
def gallery_upload():
    # print(current_app.config['UPLOADS_DEFAULT_DEST'])
    return render_template(
        'gallery_item.html',
        action='UPLOAD',
        pageData=GalleryUploadPageData()
    )


@gallery_page.route('/save/tags', methods=['POST'])
def gallery_save_tags():
    res = JsonResponse()
    try:
        tags = request.form.getlist('tags[]')
        tags.reverse()
        if GTagsMiddleware().save_all_to_db(tags):
            res.resMsg = 'Note: Tags saved successfully.'
        else:
            res.resMsg = 'Note: Failed to save tags.'
    except Exception as e:
        res.resCode = -1
        res.resMsg = e.args.__name__
        pass
    return res.outputJsonString()


@gallery_page.route('/do/upload', methods=['POST'])
def gallery_do_upload():
    res = JsonResponse()
    res.resMsg = 'Upload start.'
    if 'photo' in request.files:
        try:
            photos = UploadSet('photos', IMAGES)
            configure_uploads(current_app, (photos))
            filename = photos.save(request.files['photo'])
            gitem = GalleryMiddleware(
                link=photos.url(filename),
                tags=request.form.getlist('tags'),
                caption=request.form['caption']
            )
            if gitem.save_to_db():
                res.resMsg = 'Note: Photo saved successfully.'
            else:
                res.resMsg = 'Note: Failed to save photo.'
            res.data = gitem.outputDict()
        except Exception:
            res.resCode = -1
            res.resMsg = 'Error: Upload failed.\n\n' + \
                'The file size maybe exceeds limited size [' + \
                '{0}'.format(current_app.config['MAX_CONTENT_LENGTH_MB']) + \
                'MB].'
            pass
    else:
        res.resCode = -1
        res.resMsg = 'Error: Cannot find the file field in your upload form.'
    # print(res.outputJsonString()) # Print for test.
    return res.outputJsonString()


@gallery_page.route('/show/<path:fullpath>', methods=['GET'])
def gallery_show_uploadfiles(fullpath):
    return redirect(url_for('static', filename=fullpath))
