from django.contrib.auth.models import User
from applications.alumniprofile.models import Profile


def add_pass() :
    print("Adding password")
    try :
        profiles = Profile.objects.all()
        users_to_update = []
        for profile in profiles:
            profile.user.set_password(profile.reg_no)
            users_to_update.append(profile.user)
        User.objects.bulk_update(users_to_update, ['password'])
        print("Password added successfully")
    except Exception as e :
        print(f'An error occured: {e}')
        raise
