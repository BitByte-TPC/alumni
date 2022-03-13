from applications.alumniprofile.models import Profile
from AlumniConnect.views import reg_no_gen,convert_int

print(Profile.objects.all().order_by('user__date_joined'))

# def reg_no_gen(degree_, spec_, year):
#     print(Profile.objects.all().order_by('user__date_joined'))
#     print(Profile.objects.all().order_by('user__date_joined'))
#     degree = {"B.Tech" : "1", "B.Des" : '2', "M.Tech" : '3', "M.Des" : '4', "PhD" : '5'}
#     spec = {"NA" : '00', "CSE": "01", "ECE": "02", "ME":"03", "MT": "04", "NS":"05", "DS":"06"}
#     last_reg_no = Profile.objects.filter(year_of_admission=year).order_by('user__date_joined').last()
#     new_reg_no = (int(str(last_reg_no.reg_no)[-4:]) + 1) if last_reg_no else 1
#     return degree[degree_] + spec[spec_] + str(year)[2:] + str(convert_int(new_reg_no, 4))

# def convert_int(number,decimals) :
#     return str(number).zfill(decimals)
for p in Profile.objects.all().order_by('user__date_joined'):
    # p.is_verified=True
    #p.save()
    p.reg_no = reg_no_gen(p.programme, p.branch, p.year_of_admission, p.user.date_joined)
    
    #p.reg_no = 0
    print(p.name, p.reg_no, int(p.reg_no))
    p.save()