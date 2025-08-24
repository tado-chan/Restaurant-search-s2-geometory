"""
WSGI config for restaurant_search project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_search.settings')

application = get_wsgi_application()