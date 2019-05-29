import os
import django
from channels.routing import get_default_application
import channels 

# channel_layer = channels.asgi.get_channel_layer()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoPostgresProject.settings')

django.setup()
application = get_default_application()
