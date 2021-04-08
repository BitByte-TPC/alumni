from django.contrib.auth.models import User
from applications.alumniprofile.models import Profile

users = Profile.objects.all()
for user in users:
    print(user.reg_no)
    #user.user.is_active = True
    user.user.set_password(user.reg_no)
    user.user.save()
