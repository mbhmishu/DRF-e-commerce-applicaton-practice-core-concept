from django.contrib import admin
from .models import *

admin.site.register(Product)
admin.site.register(Category)

admin.site.register(ProductImg)
admin.site.register(ImgConnector)
admin.site.register(Tag)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Material)
admin.site.register(Attribute)




# Register your models here.
