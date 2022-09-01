
from django.http import HttpResponseRedirect


def custom_login_required(function):
    """
     This decorator checks if user is logged in as well as if user profile is verified by by admin or not ,
     And then redirect user accordingly, if required
    """
    
    def wrapper(request,*args, **kwargs):
        user = request.user
        if not (user.is_authenticated):
            return HttpResponseRedirect('/')   # case when user is not logged in 
        elif (not user.profile.verify) and (user.is_authenticated == True) and (request.path != '/complete_profile/'):
            return HttpResponseRedirect('/complete_profile/')  # case when user is logged in but haven't completed profile as after completing profile only  user will be able to login
        else:
            return function(request,*args,**kwargs)
    
    return wrapper
