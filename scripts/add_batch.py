import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AlumniConnect.settings.development")
django.setup()

from applications.alumniprofile.models import Batch

def add_batch() :
    try :
        batch_list = [Batch(batch = year) for year in range(2000, 2024)]
        Batch.objects.bulk_create(batch_list, ignore_conflicts=True)
        print("Batch added successfully")
    except Exception as e :
        print(f'An error occured: {e}')
        raise
