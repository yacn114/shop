from django.shortcuts import render
from django.contrib import messages
from .models import Product,returned,Category,product_sold
from account.models import User
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
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

# search product
def search(request):
    if request.POST['search']:
        search_words = request.POST['search']
        searchResualt = Product.objects.filter(name__contains=search_words)
        return render(request,'search.html',{'resualt':searchResualt,"user_search":search_words})
    
def categoryPage(request,name):
    cat = get_object_or_404(Category,name=name)
    product = Product.objects.filter(category=cat)
    return render(request,"category.html",{"product":product})

def mount_data(request):
    thirty_days_ago = datetime.now() - timedelta(days=30)
    queryset = product_sold.objects.filter(date__gte=thirty_days_ago).values('product','price_sold','user')
    for item in queryset:
        print(item)
