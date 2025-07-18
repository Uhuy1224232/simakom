import os
from celery import Celery

# Set default setting untuk Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'monitoring_komputer.settings')

# Inisialisasi objek Celery
app = Celery('monitoring_komputer')

# Load konfigurasi Celery dari setting Django dengan prefix 'CELERY'
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover semua task dari semua apps terdaftar di INSTALLED_APPS
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
