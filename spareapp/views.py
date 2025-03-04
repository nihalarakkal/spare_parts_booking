from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime,timedelta
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import stripe
import razorpay
from django.contrib import messages
#

# Create your views here.

def index(request):
    return render(request, 'index.html')
def registration(request):
    if(request.method=='POST'):
        Fullname=request.POST.get('Fullname')
        Email=request.POST.get('Email')
        Mobile=request.POST.get('Mobile')
        Age=request.POST.get('Age')
        Gender=request.POST.get('Gender')
        Address=request.POST.get('Address')
        Propic=request.FILES.get('Propic')
        Password=request.POST.get('Password')
        Cpassword=request.POST.get('Cpassword')
        if(Password==Cpassword):
            data=newregistration(Fullname=Fullname,Email=Email,Mobile=Mobile,Age=Age,Gender=Gender,Address=Address,Propic=Propic,Password=Password)
            data.save()
            messages.success(request,"Registered Successfully")
            return redirect(loginview)
        else:
           messages.error(request,"Login Failed")
    return render(request,'registration.html')

def loginview(request):
    if(request.method=='POST'):
        email=request.POST.get('email')
        password=request.POST.get('password')
        data=newregistration.objects.all()
        for i in data:
            if(i.Password==password and i.Email==email):
                request.session['userid']=i.id
                messages.success(request,"Login Successfully")
                return redirect(profile)
        else:
            messages.error(request,"Login Failed")
    return render(request,'user_login.html')
def logoutview(request):
    try:
        # Check if user is logged in
        if 'userid' in request.session:
            # Clear specific session data
            del request.session['userid']
            # Flush all session data
            request.session.flush()
            messages.success(request, "Logged out successfully")
        else:
            messages.info(request, "You are not logged in")
            
    except Exception as e:
        messages.error(request, "An error occurred during logout")
        print(f"Logout error: {str(e)}")
    
    # Redirect to login page
    return redirect('index')


def profile(request):
    id1 = request.session['userid']
    data = newregistration.objects.get(id=id1)
    category = request.GET.get('sparecategory','all')  # get selected category , if there is no category selected all option will work
    if category == 'all':
        db = sparereg.objects.all()  # fetch all products
    else:
        db = sparereg.objects.filter(sparecategory=category)  # filter produc
    return render(request,'profile2.html',{'data':data,'db':db})




def usersingleview(request,id):
    data=newregistration.objects.get(id=id)
    return render(request,'usersingleview1.html',{'data':data})


def userupdate(request,id):
    data=newregistration.objects.get(id=id)
    if(request.method=='POST'):
        data.Fullname=request.POST.get('name')
        data.Email=request.POST.get('email')
        data.Mobile=request.POST.get('mobile')
        data.Age=request.POST.get('age')
        data.Gender=request.POST.get('gender')
        data.Address=request.POST.get('address')
        if (request.FILES.get('propic')==None):
            data.save()
        else:
            data.Propic=request.FILES.get('propic')
        data.save()
        return redirect(f"http://127.0.0.1:8000/spareapp/usersingleview/{id}")
    return render(request,'user_update.html',{'data':data})

def spareupload(request):
    if(request.method=='POST'):
        sparename=request.POST.get('sparenm')
        spareprice=request.POST.get('spareprc')
        sparepic=request.FILES.get('sparepc')
        sparecompany=request.POST.get('sparecmpny')
        sparedesc=request.POST.get('spareds')
        sparecategory=request.POST.get('sparect')
        sparemodel=request.POST.get('sparemdl')
        db=sparereg(sparename=sparename,spareprice=spareprice,sparepic=sparepic,sparecompany=sparecompany,sparedesc=sparedesc,sparecategory=sparecategory,sparemodel=sparemodel)
        db.save()
        messages.success(request,"Spare Upload Successfully")
    return render(request,'spareregister.html')


def addtocartview(request,itemid):
    item=sparereg.objects.get(id=itemid)
    cart=addtocart.objects.all()
    for i in cart:
        if i.item.id==itemid and i.userid==request.session['userid']:
            i.quantity+=1
            i.save()
            messages.success(request,"added to cart")
    else:
        db=addtocart(userid=request.session['userid'],item=item)
        db.save()
        return redirect(cartdisplay)


def cartdisplay(request):
    userid=request.session.get('userid')
    db=addtocart.objects.filter(userid=userid)
    total=0
    count=0
    fulltotal=0
    for i in db:
        i.item.spareprice*=i.quantity
        total+=i.item.spareprice
        count+=1
    fulltotal+=total+24+30
    return render(request,'cartdisplay1.html',{'db':db,'total':total,'count':count,'fulltotal':fulltotal})

def incdec(request,cartid):
    data=addtocart.objects.get(id=cartid)
    action=request.GET.get('action')
    if(action=='increment'):
        data.quantity+=1
        data.save()
    elif(action=='decrement' and data.quantity>0):
        data.quantity-=1
        data.save()
    return redirect(cartdisplay)

def remove(request,cartid):
    data=addtocart.objects.get(id=cartid)
    data.delete()
    return redirect(cartdisplay)

def wishlistview(request,itemid):
    item=sparereg.objects.get(id=itemid)
    data=wishlist.objects.all()
    if(request.method=='GET'):
        for i in data:
            if(i.item.id==itemid and i.userid==request.session['userid']):
                messages.error(request,"Already moved")
        else:
            data=wishlist(item=item,userid=request.session['userid'])
            data.save()
            return redirect(wishlistallview)


def wishlistallview(request):
    userid=request.session['userid']
    data=wishlist.objects.filter(userid=userid)
    return render(request,'wishlist.html',{'data':data})


def wishremove(request,id):
    wish=wishlist.objects.get(id=id)
    wish.delete()
    messages.success(request,"Successfully Removed")
    return redirect(wishlistallview)

def addaddress(request):
    id1=request.session['userid'] #5
    userdata=newregistration.objects.get(id=id1)
    if(request.method=='POST'):
        address1=request.POST.get('address1')
        address2=request.POST.get('address2')
        pincode=request.POST.get('pincode')
        city=request.POST.get('city')
        state=request.POST.get('state')
        contact_name=request.POST.get('contact_name')
        contact_number=request.POST.get('contact_number')
        db=address(userdetails=userdata,addressline1=address1,addressline2=address2,pincode=pincode,city=city,state=state,contact_name=contact_name,contact_number=contact_number)
        db.save()
        return redirect(delivery_details)
    return render(request,'address.html')

def delivery_details(request):
    userid=request.session['userid']
    data=address.objects.filter(userdetails__id=userid)
    return render(request,'delivery_details.html',{'data':data})

def final_summary(request):
    userid=request.session['userid']
    address_id=request.GET.get('address')
    addressnew=address.objects.get(id=address_id)
    cartitems=addtocart.objects.filter(userid=userid)
    key=settings.STRIPE_PUBLISHABLE_KEY
    total=0
    striptotal=0
    for i in cartitems:
        i.item.spareprice*=i.quantity
        total+=i.item.spareprice
        striptotal=total*100
    total+=54
    return render(request,'summary1.html',{'addressnew':addressnew,'cartitems':cartitems,'total':total,'key':key,'striptotal':striptotal})

def create_order(request): #after payment
    if(request.method=='POST'):
        order_items=[]
        total_price=0
        total=0
        userid=request.session['userid']
        user=newregistration.objects.get(id=userid)
        address_id=request.POST.get('address_id')
        address1=address.objects.get(id=address_id)

        cart=addtocart.objects.filter(userid=userid)

        order=Order.objects.create(userdetails=user,address=address1)

        for i in cart:
            OrderItem.objects.create(
                order=order,
                order_pic=i.item.sparepic,
                pro_name=i.item.sparename,
                quantity=i.quantity,
                price=i.item.spareprice

            )
            total_price+=i.item.spareprice*i.quantity
            total=total_price+54
            order_items.append({
                'product':i.item.sparename,
                'quantity':i.quantity,
                'price':i.item.spareprice*i.quantity,
            })

        expeceted_delivery_date=datetime.now()+timedelta(days=7)
        subject='order confirmation'
        context={
            'order_items':order_items,
            'total_price':total_price,
            'total':total,
            'expected_delivery_date':expeceted_delivery_date.strftime('%Y-%m-%d')
        }
        html_message=render_to_string('order_confirmation.html',context)
        plain_message=strip_tags(html_message)

        from_email='nihalarakkal578@gmail.com'

        to_email=[user.Email]

        send_mail(subject,plain_message,from_email,to_email,html_message=html_message)

        cart.delete()

        return HttpResponse('order created succesfully')

def order_view(request):
    userid=request.session['userid']
    order=OrderItem.objects.filter(order__userdetails__id=userid).order_by('-order__ordered_date')
    return render(request,'order.html',{'order':order})

def order_cancel(request,id):
    userid=request.session['userid']
    user=newregistration.objects.get(id=userid)
    db=OrderItem.objects.get(id=id)
    db.order_status=False
    db.save()
    subject='order cancelled'
    context={'product_name':db.pro_name,'price':db.price}
    html_message=render_to_string('order_cancel.html',context)
    plain_message=strip_tags(html_message)
    from_email='nihalarakkal578@gmail.com'
    to_email=[user.Email]
    send_mail(subject,plain_message,from_email,to_email,html_message=html_message)
    return HttpResponse('order cancelled')
def contact_page(request):
    return render(request,"contact.html")







