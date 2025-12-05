from django.utils.crypto import get_random_string
from django.db import models
import os
from django.contrib.auth.models import Permission, User
from django.core.validators import MinValueValidator,MaxValueValidator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"image-{unique_id}{ext}"
    return f"products/{final_name}" # change directory name

class Discount(models.Model):
    discount=models.IntegerField(default=0,blank=True)
    description = models.CharField(max_length=50,blank=True)

    def __str__(self):
        return f"{self.discount} درصد"


    


class Size(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()

    def __str__(self):
        return f"{self.title}"
    
# class Color(models.Model): 
#     title = models.CharField(max_length=50) 
#     description = models.TextField()


#     def __str__(self):
#         return f"{self.title}"
    



class Color(models.Model): 
    title = models.CharField(max_length=50) 
    hex_code = models.CharField(max_length=7,default="#FFFFFF", help_text="کد رنگ به صورت HEX (مثال: #FF5733)")
    description = models.TextField()

    def __str__(self):
        return self.title


class Brand(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.title

   
class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    
    image = models.ImageField(
        upload_to="categories/", 
        blank=True, 
        null=True,
        help_text="تصویر دسته‌بندی (اختیاری)"
    )

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"
        ordering = ['parent__id', 'title']  # مرتب‌سازی بهتر

    def save(self, *args, **kwargs):
        # ایجاد خودکار slug
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=False)
        super().save(*args, **kwargs)

    def __str__(self):
        # نمایش زیباتر در ادمین
        if self.parent:
            return f"{self.parent} → {self.title}"
        return self.title
    



class Product(models.Model):
    title = models.CharField(max_length=50,blank=True)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True, related_name='products')
    og_price= models.IntegerField()
    is_sale = models.BooleanField(default=False)
    discount= models.ForeignKey(Discount, on_delete=models.CASCADE)
    colors = models.ManyToManyField(Color,blank=True)
    size = models.ManyToManyField(Size)
    discounted_price = models.IntegerField(null=True)
    sell_price = models.IntegerField(null=True)
    star = models.IntegerField(default=0, validators=[MaxValueValidator(5),MinValueValidator(0)])
    is_available = models.BooleanField()
   
    # سایر فیلدها...
    inventory = models.IntegerField(default=0, null=False, blank=False)

    image = models.ImageField(upload_to=upload_image_path)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.title}"
    
    @property
    def discounted_price(self):
        # og_price =self.og_price
        # discount =self.discount

        return ((self.og_price)*(self.discount.discount))/100

    @property
    def sell_price(self):
        og_price =self.og_price
        discounted_price =self.discounted_price

        return (og_price)-(discounted_price)
    
    
class Comment(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    created_update = models.DateTimeField(auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    
    
class Gallary(models.Model):
    title = models.CharField(max_length=20,blank=True)
    image = models.ImageField(upload_to=upload_image_path,blank=True) 
    product = models.ForeignKey(Product, on_delete=models.CASCADE)



# Create your models here.
