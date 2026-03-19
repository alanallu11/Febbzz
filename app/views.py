from django.shortcuts import render,redirect, get_object_or_404
from .models import Ladies
from .models import Register,Ladies,Kids,Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
def home(re):
    return HttpResponse("got it")
def registerfn(re):
    if re.method == "POST":
        username=re.POST.get("username")
        email=re.POST.get("email")
        password=re.POST.get("password")
        if Register.objects.filter(username=username).exists():
            return render(re,"register.html",{
                'error':"User already exist."
            })
        else:
            Register.objects.create(
                username=username,
                email=email,
                password=password,
            )
    return render(re,"register.html")

def loginfn(re):
    if re.method =="POST":
        username=re.POST["username"]
        password=re.POST["password"]
        if username=="admin" and password=="admin123":
            re.session['admin'] = username
            return redirect(adminpagefn)
        try:
            user= Register.objects.get(username=username)
            if user.password==password:
                re.session['user']= username
                return redirect("home")
            else:
                return render(re,"login.html",{
                    'error':"Invalid Password"
                })
            
        except Register.DoesNotExist:
            return render(re,"login.html",{
                'error':"User not exist."
            })

    return render(re,"login.html")

def logoutfn(re):
    re.session.flush()
    return redirect(loginfn)

def firsthomefn(re):
    if 'user' in re.session:
        return render(re,"firsthomepage.html")
    else:
        return redirect(loginfn)

def homefn(re):
    if 'user' in re.session:
        s=re.session['user']
        return render(re,"homepage.html",{'s':s})
    else:
        return redirect(loginfn)

def accountfn(re):
    if 'user' in re.session:
        username = re.session['user']
        user = Register.objects.get(username=username)
        return render(re, "account.html", {'user': user})
    else:
        return redirect(loginfn)

def adminpagefn(re):
    if 'admin' in re.session:
        f=re.session['admin']
        a=Ladies.objects.all()
        return render(re,"adminpage.html",{'f':f,'d':a})
    else:
        return redirect(loginfn)

def womenfn(re):
    if 'user' in re.session:
        l=Ladies.objects.all()
        return render(re,"women.html",{'l':l})
    else:
        return redirect(loginfn)
    
def kidsfn(re):
    if 'user' in re.session:
        k=Kids.objects.all()
        return render(re,"kids.html",{'k':k})
    else:
        return redirect(loginfn)
    
def womenaddfn(re):
    if re.method == "POST":
        Ladies.objects.create(
            name=re.POST.get("name"),
            price=re.POST.get("price"),
            description=re.POST.get("description"),
            image=re.FILES.get("image",None),
        )
        return redirect(womenaddfn)
    return render(re,"womenadd.html")

def kidsaddfn(re):
    if re.method=="POST":
        Kids.objects.create(
            kidsname=re.POST.get("kidsname"),
            kidsprice=re.POST.get("kidsprice"),
            kidsdescription=re.POST.get("kidsdescription"),
            kidsimage=re.FILES.get("kidsimage"),
        )
        return redirect(kidsaddfn)
    return render(re,"kidsadd.html")


def adminwomeneditfn(request, d):
    product = get_object_or_404(Ladies, pk=d)

    if request.method == "POST":
        product.name = request.POST.get('productname')
        product.price = request.POST.get('productprice')
        product.description = request.POST.get('productdescription')

        # update image only if new image selected
        if request.FILES.get('productimage'):
            product.image = request.FILES.get('productimage')

        product.save()
        messages.success(request, "Product updated successfully")
        return redirect(womenfn)   # change to your list page name

    if "admin" in request.session:
        return render(request, "adminwomenedit.html", {"d": product})

    return redirect(adminwomenlistfn)

def adminwomenlistfn(request):
    if "admin" in request.session:
        products = Ladies.objects.all()
        return render(request, "adminwomenlist.html", {"products": products})
    return redirect(loginfn)


def adminwomendeletefn(request, id):
    if request.method == "POST":
        product = get_object_or_404(Ladies, pk=id)
        product.delete()
    return redirect('adminwomenlist')   # your list page name

def adminkidslistfn(request):
    if "admin" in request.session:
        kiddu = Kids.objects.all()
        return render(request, "adminkidslist.html", {"kiddu": kiddu})
    return redirect(loginfn)

def adminkidseditfn(request, f):
    kiddu = get_object_or_404(Kids, pk=f)

    if request.method == "POST":
        kiddu.kidsname = request.POST.get('productname')
        kiddu.kidsprice = request.POST.get('productprice')
        kiddu.kidsdescription = request.POST.get('productdescription')

        # update image only if new image selected
        if request.FILES.get('productimage'):
            kiddu.kidsimage = request.FILES.get('productimage')

        kiddu.save()
        messages.success(request, "Product updated successfully")
        return redirect('adminkidslist')   # better to use url name

    if "admin" in request.session:
        return render(request, "adminkidsedit.html", {"d": kiddu})

    return redirect('adminkidslist')

def adminkidsdeletefn(request, id):
    if "admin" in request.session:
        if request.method == "POST":
            kiddu = get_object_or_404(Kids, pk=id)
            kiddu.delete()
            messages.success(request, "Product deleted successfully")
    return redirect('adminkidslist')

def add_ladies_to_cart(re, id):
    if 'user' in re.session:
        product = Ladies.objects.get(id=id)

        cart_item, created = Cart.objects.get_or_create(
            ladies_product=product,
            user=re.session['user']
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')
    else:
        return redirect('login')

def add_kids_to_cart(re, id):
    if 'user' in re.session:
        product = Kids.objects.get(id=id)

        cart_item, created = Cart.objects.get_or_create(
            kids_product=product,
            user=re.session['user']
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        return redirect('cart')
    else:
        return redirect('login')

def cartfn(re):
    if 'user' in re.session:
        items = Cart.objects.filter(user=re.session['user'])  # ✅ FIXED
        total = 0

        for item in items:
            if item.ladies_product:
                item.subtotal = item.ladies_product.price * item.quantity
            elif item.kids_product:
                item.subtotal = item.kids_product.kidsprice * item.quantity
            else:
                item.subtotal = 0

            total += item.subtotal

        return render(re, 'cart.html', {
            'items': items,
            'total': total
        })
    else:
        return redirect('login')

def increase_qty(re, id):
    if 'user' in re.session:
        item = get_object_or_404(Cart, id=id)
        item.quantity += 1
        item.save()
        return redirect(cartfn)

def decrease_qty(re, id):
        if 'user' in re.session:
            item = get_object_or_404(Cart, id=id)
            if item.quantity > 1:
                item.quantity -= 1
                item.save()
            return redirect(cartfn)

def delete_item(re, id):
    if 'user' in re.session:
        item = get_object_or_404(Cart, id=id)
        item.delete()
        return redirect(cartfn)

def update_email(request):
    if request.method == "POST":
        if 'user' in request.session:
            username = request.session['user']
            user = Register.objects.get(username=username)
            new_email = request.POST.get("email")
            user.email = new_email
            user.save()
    return redirect("account")

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Wishlist, Ladies, Kids

@login_required(login_url='login')   # redirects to login page if not logged in
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)
    return render(request, 'wishlist.html', {'items': items})

@login_required(login_url='login')
def add_ladies_to_wishlist(request, product_id):
    product = Ladies.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, ladies_product=product)
    return redirect('wishlist')

@login_required(login_url='login')
def add_kids_to_wishlist(request, product_id):
    product = Kids.objects.get(id=product_id)
    Wishlist.objects.get_or_create(user=request.user, kids_product=product)
    return redirect('wishlist')

@login_required(login_url='login')
def remove_wishlist(request, item_id):
    Wishlist.objects.filter(id=item_id, user=request.user).delete()
    return redirect('wishlist')