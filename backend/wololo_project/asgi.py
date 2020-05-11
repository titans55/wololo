import os
import django
from channels.routing import get_default_application
from channels.asgi import get_channel_layer

channel_layer = channels.asgi.get_channel_layer()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wololo_project.settings.prod')

django.setup()
application = get_default_application()
