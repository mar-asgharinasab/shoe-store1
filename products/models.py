from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
import os


# -----------------------------
#       IMAGE PATH
# -----------------------------
def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    unique_id = get_random_string(length=15)
    final_name = f"image-{unique_id}{ext}"
    return f"products/{final_name}"


# -----------------------------
#       DISCOUNT
# -----------------------------
class Discount(models.Model):
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.discount}%"


# -----------------------------
#       SIZE
# -----------------------------
class Size(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


# -----------------------------
#       COLOR
# -----------------------------
class Color(models.Model):
    title = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7, default="#FFFFFF")
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


# -----------------------------
#       BRAND
# -----------------------------
class Brand(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title


# -----------------------------
#       CATEGORY
# -----------------------------
from django.utils.text import slugify

class Category(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children'
    )

    class Meta:
        ordering = ['parent__id', 'title']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.parent} → {self.title}" if self.parent else self.title

    def get_full_slug(self):
        """ مسیر کامل دسته + والدها برای URL """
        if self.parent:
            return f"{self.parent.get_full_slug()}/{self.slug}"
        return self.slug



# -----------------------------
#       PRODUCT
# -----------------------------
class Product(models.Model):
    title = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)

    categories = models.ManyToManyField(Category)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    og_price = models.IntegerField()
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE)
    is_sale = models.BooleanField(default=False)

    colors = models.ManyToManyField(Color, blank=True)
    size = models.ManyToManyField(Size)

    # حذف فیلدهای duplicate
    # discounted_price
    # sell_price

    star = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

    is_available = models.BooleanField(default=True)
    inventory = models.IntegerField(default=0)

    image = models.ImageField(upload_to=upload_image_path)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    @property
    def discounted_price(self):
        """تخفیف واقعی به تومان"""
        return int((self.og_price * self.discount.discount) / 100)

    @property
    def sell_price(self):
        """قیمت نهایی محصول"""
        return int(self.og_price - self.discounted_price)


# -----------------------------
#       COMMENT
# -----------------------------
class Comment(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


# -----------------------------
#       GALLERY
# -----------------------------
class Gallary(models.Model):
    title = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
