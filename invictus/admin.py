from django.contrib import admin
from invictus.models import Member_reg
from invictus.models import Contact
from invictus.models import reg_members
from invictus.models import Uploads
from invictus.models import Profile
from invictus.models import Accounts
from invictus.models import Transact
from invictus.models import Jipange_Acc
from invictus.models import Timiza_Acc
from invictus.models import Fixed_Acc
from invictus.models import Help

# Register your models here.

admin.site.register(Contact)
admin.site.register(Member_reg)
admin.site.register(reg_members)
admin.site.register(Uploads)
admin.site.register(Profile)
admin.site.register(Accounts)
admin.site.register(Transact)
admin.site.register(Jipange_Acc)
admin.site.register(Timiza_Acc)
admin.site.register(Fixed_Acc)
admin.site.register(Help)