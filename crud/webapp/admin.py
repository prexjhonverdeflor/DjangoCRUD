from django.contrib import admin
from . models import Record, BICSetup, MCRegister,PesoNet


admin.site.register(Record)

admin.site.register(BICSetup)

admin.site.register(MCRegister)

admin.site.register(PesoNet)


