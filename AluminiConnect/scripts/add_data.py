import datetime, xlrd
from applications.alumniprofile.models import Profile, Batch
from django.contrib.auth.models import User

loc = "acc.xlsx"
wb = xlrd.open_workbook(loc)
sheet = wb.sheet_by_index(0)

for row in range(1, sheet.nrows):
    vals = sheet.row_values(row)
    a1 = sheet.cell_value(rowx=row, colx=5)
    u1 = User(username=str(int(vals[0])), email=str(sheet.cell(row, 3).value))
    u1.set_password(str(int(vals[0])))
    u1.save()
    p1 = Profile(user=u1, email=str(sheet.cell(row, 3).value), roll_no=int(vals[0]), first_name=vals[1], last_name=vals[2], sex=vals[4], programme=vals[6], branch=vals[7], batch=Batch(int(vals[8])) , date_of_birth=datetime.datetime(*xlrd.xldate_as_tuple(a1, wb.datemode)))
    
    p1.save()
