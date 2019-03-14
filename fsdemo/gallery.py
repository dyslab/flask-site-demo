from flask import Blueprint, request, redirect, render_template
from flask import url_for, current_app
from flask_uploads import UploadSet, IMAGES, configure_uploads
from fsdemo.pagedata.gallery import GalleryUploadPageData, GalleryListPageData
from fsdemo.pagedata.gallery import GalleryEditPageData
from fsdemo.pagedata.gallery import GTagsMiddleware, GalleryMiddleware
from fsdemo.response import JsonResponse

gallery_page = Blueprint(
    'gallery',
    __name__,
    static_folder='static',
    template_folder='templates'
)


@gallery_page.route('/', methods=['GET', 'POST'])
def gallery_index():
    return redirect(url_for('.gallery_list'))


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
        if GTagsMiddleware().save_all(tags):
            res.resMsg = 'Note: Tags saved successfully.'
        else:
            res.resMsg = 'Note: Failed to save tags.'
    except Exception:
        res.resCode = -1
        res.resMsg = "Network error occurred."
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
            gflag = GalleryMiddleware().save_one(
                link=photos.url(filename),
                tags=request.form.getlist('tags'),
                caption=request.form['caption']
            )
            if gflag:
                res.resMsg = 'Note: Photo saved successfully.'
            else:
                res.resMsg = 'Note: Failed to save photo.'
            res.data = {
                'link': photos.url(filename),
                'tags': request.form.getlist('tags'),
                'caption': request.form['caption']
            }
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


@gallery_page.route('/list', methods=['GET', 'POST'])
def gallery_list():
    return render_template(
        'gallery_list.html',
        pageData=GalleryListPageData()
    )


@gallery_page.route('/list/photos', methods=['POST'])
def gallery_list_photos():
    res = JsonResponse()
    try:
        keyword = request.form['keyword']
        if keyword == 'ALL':
            glist = GalleryMiddleware().load_all(
                int(request.form['page']),
                int(request.form['offset']),
                current_app.config['GALLERY_PER_PAGE'],
            )
        elif keyword == 'TAG':
            glist = GalleryMiddleware().load_by_tag(
                int(request.form['page']),
                int(request.form['offset']),
                current_app.config['GALLERY_PER_PAGE'],
                request.form['tag']
            )
        elif keyword == 'YEAR':
            glist = GalleryMiddleware().load_by_year(
                int(request.form['page']),
                int(request.form['offset']),
                current_app.config['GALLERY_PER_PAGE'],
                int(request.form['year'])
            )
        else:
            glist = None
        if glist is not None:
            res.resMsg = 'Note: Gallery loaded successfully.'
        else:
            res.resMsg = 'Note: Failed to load gallery.'
        res.data = glist
    except Exception:
        res.resCode = -1
        res.resMsg = "Network error occurred."
        pass
    return res.outputJsonString()

    return


@gallery_page.route('/download/<int:id>', methods=['GET'])
def gallery_download(id):
    return GalleryMiddleware().downloadByID(id)


@gallery_page.route('/delete/<int:id>', methods=['GET'])
def gallery_delete(id):
    res = JsonResponse()
    try:
        gflag = GalleryMiddleware().delete_by_id(id)
        if gflag:
            res.resMsg = 'Note: Deleted photo successfully.'
        else:
            res.resCode = -1
            res.resMsg = 'Note: Failed to delete the photo.'
    except Exception:
        res.resCode = -1
        res.resMsg = 'Error: Network failed.' + \
            ' Check your network connection please.'
        pass
    # print(res.outputJsonString())  # Print for test.
    return res.outputJsonString()


@gallery_page.route('/edit/<int:id>', methods=['GET'])
def gallery_edit(id):
    return render_template(
        'gallery_item.html',
        action='EDIT',
        pageData=GalleryEditPageData(id)
    )


@gallery_page.route('/edit/save/<int:id>', methods=['POST'])
def gallery_edit_save(id):
    res = JsonResponse()
    try:
        bflag = GalleryMiddleware().save_by_id(
            id=id,
            tags=request.form.getlist('tags'),
            caption=request.form['caption']
        )
        if bflag:
            res.resMsg = 'Note: Saved changes successfully.'
        else:
            res.resMsg = 'Note: Failed to save the changes.'
    except Exception:
        res.resCode = -1
        res.resMsg = 'Error: Network failed.' + \
            ' Check your network connection please.'
        pass
    # print(res.outputJsonString()) # Print for test.
    return res.outputJsonString()
