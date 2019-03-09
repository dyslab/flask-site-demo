from fsdemo.pagedata.base import PageData


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
        self.allTagList = ['Personal', 'View', 'Dairy', 'Content', 'Test']
        self.objectTags = ['Dairy', 'Test']
        self.objectContent = 'This is a blog content example.'
