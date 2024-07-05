from django.shortcuts import render
from django.contrib import messages
from .models import Product,returned
from account.models import User
# Create your views here.
def returnd(request):
    a = Product.objects.get(id=1)
    if request.method == "POST":
        if request.user.is_authenticated:
            product_re = Product.objects.get(id = request.POST['id'])
            customerback = User.objects.get(id = request.user.id)
            returned.objects.create(product=product_re,customer=customerback)
            messages.add_message(request, messages.SUCCESS, "با موفقیت مرجوع شد")
    return render(request,'returned.html',{"a":a})
