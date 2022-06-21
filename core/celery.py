import os
import dotenv
from celery import Celery


# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

env_file = os.path.join(os.path.dirname(os.path.dirname(
     os.path.realpath(__file__))), '.env'
 )
dotenv.read_dotenv(env_file)

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
