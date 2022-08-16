from applications.alumniprofile.models import Batch

for num in range(2009, 2023):
    b1 = Batch(batch = num)
    b1.save()