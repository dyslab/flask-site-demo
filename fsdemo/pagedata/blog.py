from datetime import datetime
from flask import current_app
from sqlalchemy import or_
from fsdemo.pagedata.base import PageData
from fsdemo.basefunc import StringToArrayWithoutSpace, GetBlogResponseList
from fsdemo.models import BTags, Blog
from fsdemo.db import db_session
import json


# Database Access Middleware: For model 'BTags'.
class BTagsMiddleware(object):
    def load_all(self):
        db_tags = BTags.query.order_by(BTags.updatetime.desc()).all()
        tags = [record.name for record in db_tags]
        return tags

    def save_all(self, tags):
        # print(tags) # print for TEST
        rflag = True
        try:
            # Remove all old tags.
            old_tags = BTags.query.all()
            for olditem in old_tags:
                db_session.delete(olditem)
            db_session.commit()
            # Insert all new tags.
            new_tags = [BTags(tag) for tag in tags]
            db_session.add_all(new_tags)
            # Commit.
            db_session.commit()
        except Exception:
            db_session.rollback()
            rflag = False
            pass
        return rflag

    # Update the field 'updatetime' of all database records to the current
    # timestamp according to the list item of 'tags'.
    def update_tags(self, tags):
        # print(tags)  # print for TEST
        rflag = True
        try:
            # Remove all old tags.
            for tag in tags:
                gtagitem = BTags.query.filter_by(name=tag).first()
                if gtagitem is not None:
                    # print(gtagitem.name)  # print for TEST
                    gtagitem.updatetime = datetime.now()
                    db_session.commit()
        except Exception:
            db_session.rollback()
            rflag = False
            pass
        return rflag


# Database Access Middleware: For model 'Blog'.
class BlogMiddleware(object):
    def save_one(self, title='', tags=None, content=''):
        rflag = True
        try:
            tags_str = json.dumps(tags, ensure_ascii=False)
            newitem = Blog(
                title=title,
                tags=tags_str,
                content=content
            )
            db_session.add(newitem)
            db_session.commit()
            # Update tags time.
            BTagsMiddleware().update_tags(tags)
        except Exception:
            db_session.rollback()
            rflag = False
            pass
        return rflag

    def load_by_id(self, id):
        if id > 0:
            bitem = Blog.query.filter_by(id=id).first()
            if bitem is not None:
                return {
                    'id': bitem.id,
                    'title': bitem.title,
                    'tags': json.loads(bitem.tags),
                    'content': bitem.content
                }
        return None

    def save_by_id(self, id=0, title='', tags=None, content=''):
        rflag = False
        if id > 0:
            try:
                tags_str = json.dumps(tags, ensure_ascii=False)
                bitem = Blog.query.filter_by(id=id).first()
                bitem.title = title
                bitem.tags = tags_str
                bitem.content = content
                bitem.updatetime = datetime.now()
                db_session.commit()
                # Update tags time.
                BTagsMiddleware().update_tags(tags)
                rflag = True
            except Exception:
                db_session.rollback()
                pass
        return rflag

    def delete_by_id(self, id):
        rflag = False
        if id > 0:
            bitem = Blog.query.filter_by(id=id).first()
            if bitem is not None:
                db_session.delete(bitem)
                db_session.commit()
                rflag = True
        return rflag

    def load_all(self, page=1, off=0, per_page=10):
        return_list = []
        if page > 0 and per_page > 0:
            if (page * per_page + off) < Blog.query.count():
                nextpage = page + 1
            else:
                nextpage = -1
            try:
                pageitems = Blog.query.order_by(
                    Blog.updatetime.desc()
                ).limit(per_page).offset((page-1)*per_page+off).all()
                return_list = GetBlogResponseList(pageitems)
            except Exception:
                pass
        return {
            'nextpage': nextpage,
            'offset': off,
            'bloglist': return_list
        }

    def search(self, page=1, off=0, per_page=10, tags=None, terms=None):
        return_list = []
        if page > 0 and per_page > 0:
            try:
                if tags is not None:
                    tags_1 = [('%' + tag + '%') for tag in tags]
                    tags_1.append('[]')
                    tagsrule = or_(
                        *[Blog.tags.like(t1) for t1 in tags_1]
                    )
                else:
                    tagsrule = None
                termsrule = None
                terms_1 = StringToArrayWithoutSpace(terms.strip())
                terms_2 = [('%' + te1 + '%') for te1 in terms_1]
                termsrule = or_(
                    *[or_(
                        Blog.title.like(te2),
                        Blog.content.like(te2)
                    ) for te2 in terms_2]
                )
                pageitems = Blog.query.order_by(
                    Blog.updatetime.desc()
                ).filter(
                    termsrule
                ).filter(
                    tagsrule
                ).limit(
                    per_page
                ).offset(
                    (page-1)*per_page+off
                ).all()
                return_list = GetBlogResponseList(pageitems, terms_1)
                search_count = Blog.query.order_by(
                    Blog.updatetime.desc()
                ).filter(
                    termsrule
                ).filter(
                    tagsrule
                ).count()
                if (page * per_page + off) < search_count:
                    nextpage = page + 1
                else:
                    nextpage = -1
            except Exception:
                pass
        return {
            'count': search_count,
            'nextpage': nextpage,
            'offset': off,
            'bloglist': return_list
        }


# Generate page data
class BlogPageData(PageData):
    def __init__(self):
        '''
            Initialize page data.
            Input Parameters:
                None
            Output Parameters:
                1. activePanelID: Active panel id.
                    0: List panel
                    1: Write/Edit panel
                    2: Search panel
        '''
        PageData.__init__(self)
        # Set active panel.
        self.activePanelID = 0
        # For blog list tab panel.
        self.pageTitle = self.pageTitle + ' / Blog Page'
        '''
            The blogList format example:
            self.blogList = [
                {
                    'id': 1,
                    'title': 'Blog title #1',
                    'time': '2019-3-3',
                    'tags': ['Personal', 'View'],
                    'content': 'Blog content Tag #3 Tag #2'
                },
                {
                    'id': 2,
                    'title': 'Blog title #2',
                    'time': '2019-3-2',
                    'tags': ['Dairy', 'Content', 'Test'],
                    'content': 'Blog content #3'
                },
                ...
            ]
        '''
        blogs = BlogMiddleware().load_all(
            1, 0, current_app.config['BLOG_PER_PAGE']
        )
        self.blogList = blogs['bloglist']
        self.nextPage = blogs['nextpage']
        self.offsetPos = blogs['offset']
        # For blog write/edit tab panel.
        self.objectTitle = 'Blog title'
        # eg. self.tagsList = ['Personal', 'View', 'Dairy', 'Content', 'Test']
        self.tagsList = BTagsMiddleware().load_all()
        self.manageTagsLink = '/blog/save/tags'
        self.objectTags = []
        self.objectContent = 'This is a blog content example.'
