from datetime import datetime
from fsdemo.pagedata.base import PageData
from fsdemo.models import BTags, Blog
from fsdemo.db import db_session
import json


# Database Access Middleware: For model 'BTags'.
class BTagsMiddleware(object):
    def load_all_from_db(self):
        db_tags = BTags.query.order_by(BTags.updatetime.desc()).all()
        tags = [record.name for record in db_tags]
        return tags

    def save_all_to_db(self, tags):
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
                    print(gtagitem.name)
                    gtagitem.updatetime = datetime.now()
                    db_session.commit()
        except Exception:
            db_session.rollback()
            rflag = False
            pass
        return rflag


# Database Access Middleware: For model 'Blog'.
class BlogMiddleware(object):
    def __init__(self, title='', tags=None, content=''):
        self.title = title
        self.tags = tags
        self.content = content

    def save_to_db(self):
        rflag = True
        try:
            tags_str = json.dumps(self.tags, ensure_ascii=False)
            newitem = Blog(
                title=self.title,
                tags=tags_str,
                content=self.content
            )
            db_session.add(newitem)
            db_session.commit()

            # Update tags time.
            BTagsMiddleware().update_tags(self.tags)
        except Exception:
            db_session.rollback()
            rflag = False
            pass
        return rflag

    def outputDict(self):
        return {
            'title': self.title,
            'tags': self.tags,
            'content': self.content
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
        self.blogList = [
            {
                'title': 'Blog title #1',
                'time': '2019-3-3',
                'tags': ['Personal', 'View'],
                'content': 'Blog content Tag #3 Tag #2'
            },
            {
                'title': 'Blog title #2',
                'time': '2019-3-2',
                'tags': ['Dairy', 'Content', 'Test'],
                'content': 'Blog content #3'
            },
            {
                'title': 'Blog title #3',
                'time': '2019-3-1',
                'tags': ['Content', 'Test'],
                'content': 'Blog content #5'
            }
        ]
        # For blog write/edit tab panel.
        self.objectTitle = 'Blog title'
        # eg. self.tagsList = ['Personal', 'View', 'Dairy', 'Content', 'Test']
        self.tagsList = BTagsMiddleware().load_all_from_db()
        self.manageTagsLink = '/blog/save/tags'
        self.objectTags = []
        self.objectContent = 'This is a blog content example.'
