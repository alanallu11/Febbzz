from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.firsthomefn),
    path('register', views.registerfn),
    path('login', views.loginfn, name='login'),          # ← added name='login'
    path('home', views.homefn, name='home'),
    path('account', views.accountfn),
    path('adminpage', views.adminpagefn),
    path('women/', views.womenfn, name='women'),
    path('kids', views.kidsfn, name='kids'),
    path('womenadd', views.womenaddfn),
    path('kidsadd', views.kidsaddfn),
    path('logout/', views.logoutfn, name='logout'),
    path('adminwomenlist/', views.adminwomenlistfn, name='adminwomenlist'),
    path('adminwomenedit/<d>/', views.adminwomeneditfn, name='adminwomenedit'),
    path('adminwomendelete/<int:id>/', views.adminwomendeletefn, name='adminwomendelete'),
    path('adminkidslist/', views.adminkidslistfn, name='adminkidslist'),
    path('adminkidsedit/<int:f>/', views.adminkidseditfn, name='adminkidsedit'),
    path('adminkidsdelete/<int:id>/', views.adminkidsdeletefn, name='adminkidsdelete'),
    path('add-ladies-to-cart/<int:id>/', views.add_ladies_to_cart, name='add_ladies_to_cart'),
    path('add-kids-to-cart/<int:id>/', views.add_kids_to_cart, name='add_kids_to_cart'),
    path('cart/', views.cartfn, name='cart'),
    path('increase/<int:id>/', views.increase_qty, name='increase_qty'),
    path('decrease/<int:id>/', views.decrease_qty, name='decrease_qty'),
    path('delete/<int:id>/', views.delete_item, name='delete_item'),
    path('account/', views.accountfn, name='account'),
    path('update_email/', views.update_email, name='update_email'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/ladies/<int:product_id>/', views.add_ladies_to_wishlist, name='add_ladies_to_wishlist'),
    path('wishlist/add/kids/<int:product_id>/', views.add_kids_to_wishlist, name='add_kids_to_wishlist'),
    path('wishlist/remove/<int:item_id>/', views.remove_wishlist, name='remove_wishlist'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)