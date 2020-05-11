import os
import django
from channels.routing import get_default_application
from channels.layers import get_channel_layer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wololo_project.settings.prod')

channel_layer = get_channel_layer()

django.setup()
application = get_default_application()
