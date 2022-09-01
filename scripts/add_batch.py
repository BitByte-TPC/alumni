from applications.alumniprofile.models import Batch
import datetime
current_time = datetime.datetime.now()
for num in range(2009, 2024):
    isActive = current_time.year() < num or (
        current_time.year == num and current_time.month < 6)
    b1 = Batch(batch=num, isActive=isActive)
    b1.save()
