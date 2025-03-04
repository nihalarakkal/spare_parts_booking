from django.urls import path

from . import views

from .views import (
    index, registration, loginview, profile, userupdate, usersingleview, spareupload,
    addtocartview, cartdisplay, incdec, remove, wishlistview, wishlistallview, wishremove,
    addaddress, delivery_details, final_summary, create_order, order_view, order_cancel,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('registration/', registration, name='registration'),
    path('loginview/', loginview, name='loginview'),
    path('logout/', views.logoutview, name='logout'),
    path('profile/', profile, name='profile'),
    path('usersingleview/<int:id>/', usersingleview, name='usersingleview'),
    path('userupdate/<int:id>/', userupdate, name='userupdate'),
    path('spareupload/', spareupload, name='spareupload'),
    path('addtocartview/<int:itemid>/', addtocartview, name='addtocartview'),
    path('cartdisplay/', cartdisplay, name='cartdisplay'),
    path('incdec/<int:cartid>/', incdec, name='incdec'),
    path('remove/<int:cartid>/', remove, name='remove'),
    path('wishlistview/<int:itemid>/', wishlistview, name='wishlistview'),
    path('wishlistallview/', wishlistallview, name='wishlistallview'),
    path('wishremove/<int:id>/', wishremove, name='wishremove'),
    path('addaddress/', addaddress, name='addaddress'),
    path('delivery_details/', delivery_details, name='delivery_details'),
    path('final_summary/', final_summary, name='final_summary'),
    path('create_order/', create_order, name='create_order'),
    path('order_view/', order_view, name='order_view'),
    path('order_cancel/<int:id>/', order_cancel, name='order_cancel'),
    path('contact_page/',views.contact_page,name='contact_page'),
   
    

]
