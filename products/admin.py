from django.contrib import admin
from .models import *


from django.forms import ModelForm, TextInput
from .models import Color

class ColorForm(ModelForm):
    class Meta:
        model = Color
        fields = '__all__'
        widgets = {
            'hex_code': TextInput(attrs={'type': 'color'}),  # ویجت انتخاب رنگ
        }

class ColorAdmin(admin.ModelAdmin):
    form = ColorForm

admin.site.register(Color, ColorAdmin)



admin.site.register(Product)
admin.site.register(Discount)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Gallary)
# admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Brand)