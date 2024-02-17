from applications.alumniprofile.models import Batch

def add_batch() :
    try :
        batch_list = [Batch(batch = year) for year in range(2009, 2024)]
        Batch.objects.bulk_create(batch_list, ignore_conflicts=True)
        print("Batch added successfully")
    except Exception as e :
        print(f'An error occured: {e}')
        raise
