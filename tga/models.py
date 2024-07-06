from django.db import models
from django.utils import timezone as ti
from django.db.models.signals import post_save
from django.dispatch import receiver
from account.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# from .models import Order
# from sms_utils import send_sms


class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=40)
    description = models.CharField(max_length=500, default="", blank=True, null=True)
    price = models.DecimalField(default=0, decimal_places=0, max_digits=12)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    picture = models.ImageField(upload_to='upload/product')
    video = models.FileField(upload_to='upload/product/videos', blank=True, null=True)
    inventory = models.IntegerField(verbose_name="موجودی محصول")
    is_sale = models.BooleanField(verbose_name="تخفیف",default=False)
    sale_price = models.DecimalField(verbose_name="قیمت تخفیف",default=0, decimal_places=0, max_digits=12)
    def __str__(self):
        return self.name


# New
# Star Product
class Stars(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    star = models.IntegerField(verbose_name="تعداد ستاره")

    def __str__(self):
        return self.product.name

# New
# returned product  
class returned(models.Model):
    customer = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    ش = ti.now() + ti.timedelta(weeks=1)
    time_back = models.DateTimeField(default=ش)
    def __str__(self):
        return self.product.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    address = models.CharField(max_length=400, default='', blank=True)
    phone = models.CharField(max_length=20, blank=True)
    date = models.DateTimeField(default=ti.datetime.today())
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Invoice(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} for {self.customer.user.username}"

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    

#===========================
# @receiver(post_save, sender=Order)
# def order_status_changed(sender, instance, **kwargs):
#     if kwargs.get('created', False):
#         # اگر سفارش جدید باشد، پیامک ارسال می‌شود.
#         send_sms(
#             to=instance.User.phone_number,
#             message=f"Your order with ID {instance.id} has been successfully placed."
#         )
#     else:
#         # اگر وضعیت سفارش تغییر کند، پیامک ارسال می‌شود.
#         send_sms(
#             to=instance.User.phone_number,
#             message=f"Your order with ID {instance.id} status has been updated to {instance.status}."
#         )