from django.conf import settings
from django.test.runner import DiscoverRunner

is_test_run = False

class ProjectTestRunner(DiscoverRunner):
    def __init__(self, *args, **kwargs):
        global is_test_run
        is_test_run = True
        super(ProjectTestRunner, self).__init__(*args, **kwargs)