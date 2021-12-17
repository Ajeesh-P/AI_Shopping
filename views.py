# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from app1.models import *
from django.http import HttpResponse,JsonResponse
from random import random
from django.core.files.storage import FileSystemStorage
import random
from django.core.mail import send_mail
from django.core.mail import EmailMessage

from django.core.files.storage import FileSystemStorage



##import cv2
# Create your views here.


def index_page(request):

    # obj=product_tb.objects.all()
    return render(request,"index.html")

def index_page_fn(request):
    return render(request,"index.html",{})

def register_page(request):
    return render(request,"register.html",{})

def login_page(request):
    return render(request,"login.html",{})

def admin_homepage(request):
    c=0
    obj=User.objects.filter(status='pending')
    c1=obj.count()
    c+=c1
    obj=Service_center.objects.filter(status='pending')
    c1=obj.count()
    c+=c1
    obj=Shop.objects.filter(status='pending')
    c1=obj.count()
    c+=c1

    return render(request,"admin_home.html",{'c':c})

def user_homepage(request):
    return render(request,"user_home.html",{})

def shop_home(request):
    return render(request,"shop_home.html",{})   

def ser_homepage(request):
    return render(request,"ser_homepage.html",{})           

def logout_fn(request):
    pass   

def view_products(request):
    sh_id=request.session['uid']
    obj=Product.objects.filter(sh_id=sh_id)
    return render(request,"shop_view_product.html",{'prs':obj})  

def add_trouble_page(request):
    return render(request,"add_trouble_page.html",{})      

def ser_view_bookings(request):
    sid=request.session['uid']
    print(sid)
    obj=Booking.objects.filter(sid=sid)
    return render(request,"ser_view_bookings.html",{'prs':obj})  

def add_trouble1(request):
    p_id=request.POST.get("id")
    obj3=Product.objects.filter(unique_id=p_id)
    if obj3.count()<=0:
        return HttpResponse("<script>alert('Unique id does not exists');window.location.href='/add_trouble_page/'</script>")

    trouble=request.POST.get("problem")
    solution=request.POST.get("solution")

    obj2=Trouble(product_id=p_id,trouble=trouble,solution=solution)
    obj2.save()
    return HttpResponse("<script>alert('Added');window.location.href='/add_trouble_page/'</script>")



    pass

def change_status(request):
    id=request.POST.get("id")
    status=request.POST.get("status")
    obj3=Booking.objects.get(id=id)
    obj3.status=status
    obj3.save()
    return HttpResponse("<script>alert('Status Updated');window.location.href='/ser_view_bookings/'</script>")

def change_status1(request):
    id=request.POST.get("id")
    status=request.POST.get("status")
    obj3=Order.objects.get(id=id)
    obj3.status=status
    obj3.save()
    return HttpResponse("<script>alert('Status Updated');window.location.href='/sview_orders/'</script>")

def troubleshoot_page(request):
    
    return render(request,"troubleshoot_page.html",{})   

def troubleshooting_page(request):
    pid=request.POST.get("product_id")
    obj3=Trouble.objects.filter(product_id=pid)
    
    return render(request,"troubleshooting_page.html",{'obj':obj3})   




def add_products(request):
    


    try:
        if request.method=="POST":

            name=request.POST.get("name")
            offer=request.POST.get("offer")
            amount=request.POST.get("amount")
            quantity=request.POST.get("quantity")
            #cat_id=request.POST.get("category")
            about_pro=request.POST.get("about_pro")
            brand=request.POST.get("brand")
            uid=request.POST.get("id")
            sh_id=request.session['uid']

            obj3=Product.objects.filter(unique_id=uid)
            if obj3.count()>0:
                return HttpResponse("<script>alert('Unique id already exists');window.location.href='/add_products_page/'</script>")


            
           
            image=request.FILES["image"]

            fs=FileSystemStorage("app1/static/product_image")
            fs.save(image.name,image)
            

            total=int(amount)-int(offer)
            
            obj2=Product(name=name,image=image,offer=int(offer),
                            amount=int(amount),quantity=int(quantity),unique_id=uid,sh_id=sh_id,
                        brand=brand,about_pro=about_pro,total=total)
            obj2.save()
            return HttpResponse("<script>alert('Successfull');window.location.href='/add_products_page/'</script>")

        

        else:

            return HttpResponse("<script>alert('some thing went wrong');window.location.href='/details_page/'</script>")

                

    except Exception as err:


        print("error",err)

        return HttpResponse("<script>alert('Try Again');window.location.href='/details_page/'</script>")

def login_check(request):
    print ("in login_check")
    if request.method=="POST":
        un=request.POST.get("username")
        ps=request.POST.get("password")
        print ("un",un,"ps",ps)
        user=Login.objects.filter(username=un,password=ps)
        print (user)
        count=user.count()

        if un=="admin" and ps=="admin":

            return HttpResponse("<script>alert('Welcome Admin');window.location.href='/admin_homepage/';</script>")

        else:
            pass
            

            
            if count==0:
                print("invalid user")
                return HttpResponse("<script>alert('invalid user');window.location.href='/register_page/';</script>")
                
            elif count==1:
                obj1=Login.objects.get(username=un,password=ps)
                lid=obj1.id
                type1=obj1.type1
                if type1=='user':
                    obj2=User.objects.get(lid=lid)
                    if obj2.status!='appoved':
                        return HttpResponse("<script>alert('Wait for approval');window.location.href='/register_page/';</script>")
                    else:
                        request.session['uid']=lid
                        return HttpResponse("<script>alert('Welcome User');window.location.href='/user_homepage/';</script>")

                if type1=='shop':
                    obj2=Shop.objects.get(lid=lid)
                    if obj2.status!='appoved':
                        return HttpResponse("<script>alert('Wait for approval');window.location.href='/register_page/';</script>")
                    else:
                        request.session['uid']=lid
                        return HttpResponse("<script>alert('Welcome Shop');window.location.href='/shop_home/';</script>")
                if type1=='ser':
                    obj2=Service_center.objects.get(lid=lid)
                    if obj2.status!='appoved':
                        return HttpResponse("<script>alert('Wait for approval');window.location.href='/register_page/';</script>")
                    else:
                        request.session['uid']=lid
                        return HttpResponse("<script>alert('Welcome Service center');window.location.href='/ser_homepage/';</script>")                
            
            else:
                   
                return HttpResponse("<script>alert('Try Again ');window.location.href='/register_page/';</script>")

    else:
               
        return HttpResponse("<script>alert('Try Again ');window.location.href='/register_page/';</script>")

def shop_register_page(request):
    return render(request,"shop_reg.html",{})

def ser_register_page(request):
    return render(request,"service_reg.html",{})

def add_products_page(request):
    return render(request,"shop_add_products.html",{})        


def reg_shop(request):
    print("registration")
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        password=request.POST.get("password")
        longi=request.POST.get("longi")
        lati=request.POST.get("lati")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        
        
        print("name",name)
        print("email",email)
        print("username",username)
        print("password",password)
        print("longi",longi)
        print("lati",lati)
        print("phone",phone)
        print("address",address)
        obj1=Login.objects.filter(username=username,password=password)
        if obj1.count()>0:
            return HttpResponse("<script>alert('Username already exists');window.location.href='/shop_register_page/';</script>")
        obj2=Login(username=username,password=password,type1='shop')   
        obj2.save()
        lid=obj2.id 
        print(lid)

        obj=Shop(
                name=name,email=email,latitude=lati,longitude=longi,phone=phone,address=address,lid=lid,status='pending'
                )
        obj.save()
    return HttpResponse("<script>alert('Registration Successful wait for approval');window.location.href='/login_page/';</script>")

def reg_ser(request):
    print("registration")
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        password=request.POST.get("password")
        longi=request.POST.get("longi")
        lati=request.POST.get("lati")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        
        
        print("name",name)
        print("email",email)
        print("username",username)
        print("password",password)
        print("longi",longi)
        print("lati",lati)
        print("phone",phone)
        print("address",address)
        obj1=Login.objects.filter(username=username,password=password)
        if obj1.count()>0:
            return HttpResponse("<script>alert('Username already exists');window.location.href='/ser_register_page/';</script>")
        obj2=Login(username=username,password=password,type1='ser')   
        obj2.save()
        lid=obj2.id 
        print(lid)

        obj=Service_center(
                name=name,email=email,latitude=lati,longitude=longi,phone=phone,address=address,lid=lid,status='pending'
                )
        obj.save()
    return HttpResponse("<script>alert('Registration Successful wait for approval');window.location.href='/login_page/';</script>") 


def reg(request):
    print("registration")
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        password=request.POST.get("password")
        dob=request.POST.get("dob")
        gender=request.POST.get("gender")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        
        
        print("name",name)
        print("email",email)
        print("username",username)
        print("password",password)
        print("dob",dob)
        print("gender",gender)
        print("phone",phone)
        print("address",address);obj1=Login.objects.filter(username=username,password=password)
        obj1=Login.objects.filter(username=username,password=password)
        if obj1.count()>0:
            return HttpResponse("<script>alert('Username already exists');window.location.href='/register_page/';<script>")
        obj2=Login(username=username,password=password,type1='user')
        obj2.save()
        lid=obj2.id    
        
        obj=User(
                name=name,email=email,
                    dob=dob,gender=gender,phone=phone,address=address,lid=lid,status='pending'
                )
        obj.save()
    return HttpResponse("<script>alert('Registration Successful');window.location.href='/login_page/';</script>")          


def approve_shop_page(request):
    obj=Shop.objects.filter(status='pending')
    return render(request,"admin_add_shop.html",{'shops':obj})
def add_shop(request):
    if request.method=='POST':
        id=request.POST['id']
        obj=Shop.objects.get(reg_id=id)
        obj.status='appoved'
        obj.save()
        return HttpResponse("<script>alert('Approved');window.location.href='/approve_shop_page/';</script>") 

def approve_ser_page(request):
    obj=Service_center.objects.filter(status='pending')
    return render(request,"add_ser_page.html",{'shops':obj})
def add_ser(request):
    if request.method=='POST':
        id=request.POST['id']
        obj=Service_center.objects.get(reg_id=id)
        obj.status='appoved'
        obj.save()
        return HttpResponse("<script>alert('Approved');window.location.href='/approve_ser_page/';</script>")         

def approve_user_page(request):
    obj=User.objects.filter(status='pending')
    return render(request,"add_user.html",{'shops':obj})
    
def add_user(request):
    if request.method=='POST':
        id=request.POST['id']
        obj=User.objects.get(reg_id=id)
        obj.status='appoved'
        obj.save()
        return HttpResponse("<script>alert('Approved');window.location.href='/approve_user_page/';</script>")      



def shop_delete_product(request):

    
    print("admin_delete_product")

    try:

        if request.method=="GET":

            id1=request.GET.get("id")

            print("id",id1)

            obj_del=Product.objects.get(id=int(id1))

            obj_del.delete()

            

            return HttpResponse("Deleted")
        
        else:
            
            return HttpResponse("Try Again")

    except:

        return HttpResponse("Try Again")
##

def shop_edit_product(request):

    
    print("admin_edit_user")

    try:

        if request.method=="GET":

            id1=request.GET.get("id")
            name=request.GET.get("name")
            offer=request.GET.get("offer")
            amount=request.GET.get("amount")
            quantity=request.GET.get("quantity")
            
            cat_id=request.GET.get("category")
            brand=request.GET.get("brand")
            about_pro=request.GET.get("about_pro")
            unique_id=request.GET.get("about_pro")

            total=int(amount)-int(offer)


            print(total)

                
            

            obj_sav=Product.objects.get(id=int(id1))

            obj_sav.name=name
            obj_sav.offer=offer
            obj_sav.amount=amount

            obj_sav.quantity=quantity
            obj_sav.unique_id
            obj_sav.total=total
            obj_sav.brand=brand
            obj_sav.about_pro=about_pro
    

            obj_sav.save()
            

            return HttpResponse("Updated")
        
        else:
            
            return HttpResponse("Try Again")

    except Exception as err:

        print("error",err)

        return HttpResponse("Try Again")

from math import sin, cos, sqrt, atan2, radians

from django.db.models.expressions import RawSQL
import math
from django.db.backends.signals import connection_created
from django.dispatch import receiver


@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    if connection.vendor == "sqlite":
        # sqlite doesn't natively support math functions, so add them
        cf = connection.connection.create_function
        cf('acos', 1, math.acos)
        cf('cos', 1, math.cos)
        cf('radians', 1, math.radians)
        cf('sin', 1, math.sin)
        cf('least', 2, min)
        cf('greatest', 2, max)





def get_locations_nearby_coords(latitude, longitude, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    # Great circle distance formula
    gcd_formula = "6371 * acos(least(greatest(cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)), -1), 1))"
    distance_raw_sql = RawSQL(gcd_formula,(latitude, longitude, latitude))
    qs = Shop.objects.all().annotate(distance=distance_raw_sql).order_by('distance')
    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance)
    return qs


def get_locations_nearby_coords2(latitude, longitude, max_distance=None):
    """
    Return objects sorted by distance to specified coordinates
    which distance is less than max_distance given in kilometers
    """
    # Great circle distance formula
    gcd_formula = "6371 * acos(least(greatest(cos(radians(%s)) * cos(radians(latitude)) * cos(radians(longitude) - radians(%s)) + sin(radians(%s)) * sin(radians(latitude)), -1), 1))"
    distance_raw_sql = RawSQL(gcd_formula,(latitude, longitude, latitude))
    qs = Service_center.objects.all().annotate(distance=distance_raw_sql).order_by('distance')
    if max_distance is not None:
        qs = qs.filter(distance__lt=max_distance)
    return qs
# nearby_locations = get_locations_nearby_coords(9.9930384, 90.2971463, 2)
# print(nearby_locations)

def view_shops(request):
    
    lati=request.POST.get('lat')
    longi=request.POST.get('longi')
    # lati=9.9930384
    # longi=76.2971463
    
    print(longi,'=======================================')
    print(lati,'=======================================')
    if longi is None:
        print("inside")
        longi=10.8505159

    if lati is None:
        print("inside lati")
        lati=76.2710833
    

    qs = get_locations_nearby_coords(float(lati), float(longi), 20)


   
    return render(request,"view_shops.html",{'shops':qs})

def book_service_page(request):
    lati=request.POST.get('lat')
    longi=request.POST.get('longi')
    # lati=9.9930384
    # longi=76.2971463
    if longi is None:
        print("inside")
        longi=10.8505159

    if lati is None:
        print("inside lati")
        lati=76.2710833
    qs = get_locations_nearby_coords2(float(lati), float(longi), 20)

    
    
     
    return render(request,"book_service_page.html",{'obj':qs}) 

def book_service(request):
    pid=request.POST.get('product_id')
    obj=Product.objects.filter(unique_id=pid)
    uid=request.session['uid']
    if obj.count()<0:
        return HttpResponse("<script>alert('Enter valid product ID');window.location.href='/book_service_page/';</script>") 

    sid=request.POST.get('ser')
    problem=request.POST.get('problem')
    obj=Booking(uid=uid,product_id=pid,sid=sid,problem=problem,status='pending')
    obj.save()
    return HttpResponse("<script>alert('Booked');window.location.href='/book_service_page/';</script>") 


def view_bookings(request):
    id=request.session['uid']
    
    obj=Booking.objects.filter(uid=id).order_by('-date')

    return render(request,'view_bookings.html',{'products':obj})

def view_orders(request):
    id=request.session['uid']
    
    obj=Order.objects.filter(uid=id).order_by('-date')

    return render(request,'view_orders.html',{'products':obj})    

def user_view_products(request,obj):
    return render(request,'user_view_products.html',{'products':obj})
    pass   

def visit_shop(request):
    id=request.POST.get('id')
    request.session['s_id']=id
    print(id,'@@@@@@@@@@@@@@@@@@@@@@@@')
    
    
    obj=Product.objects.filter(sh_id=id)
    return user_view_products(request,obj)

    

def buynow(request):
    id=request.POST.get('id')
    uid=request.session['uid']
    s_id=request.POST.get('sh_id')
    obj2=Product.objects.get(id=id)
    amt1=int(obj2.quantity)
    if amt1==0:
        return HttpResponse("<script>alert('Out of stock');window.location.href='/user_homepage/';</script>") 

    obj2.quantity=amt1-1
    obj2.save()
    
    print(s_id,'===============')
    obj=Order(uid=uid,product_id=id,status='ordered',sh_id=s_id)
    obj.save()

    return HttpResponse("<script>alert('Ordered');window.location.href='/view_orders/';</script>")   
   

def view_more(request):

    try:
        if request.method=="POST":

           
            id1=request.POST.get("id")
            s_id=request.session['s_id']
            print(s_id,'2222222222222222222222222222222')
          
            print("id1",id1,id1)
            
            obj2=Product.objects.get(id=int(id1))
            obj3=Feedback.objects.filter(pro_id=int(id1)).order_by('-date')

            print(obj2)
            
            return render(request,'view_more.html',{'data':obj2,'feedback':obj3})

        

        else:

            return HttpResponse("<script>alert('Try Again');window.location.href='/user_view_products/'</script>")

                

    except Exception as err:


        print("error",err)

        return HttpResponse("<script>alert('Try Again');window.location.href='/user_view_products/'</script>")



from testing  import predict1   
# 
def text_test(text):
    from keras import backend as K 
    K.clear_session()
    res=predict1(text)[0][0]
    if res>0.5:
        res=1
    else:
        res=0  
    if text.__contains__("not bad"):
       res=0 
    elif text.__contains__("not good"):
         res=1 
    elif text.__contains__("not satisfied"):
         res=1     
    #if ["not bad"] in text:
     #   res=0
    #elif ["not good"] in text:
     #   res=1

    print(res)
    return res


def add_to_cart(request):
    pass

def admin_user_page(request):
    obj=User.objects.filter(status='appoved')
    return render(request,"admin_user_page.html",{'obj':obj})

def admin_shop_page(request):
    obj=Shop.objects.filter(status='appoved')
    return render(request,"admin_shop_page.html",{'obj':obj})

def admin_ser_page(request):
    obj=Service_center.objects.filter(status='appoved')
    return render(request,"admin_ser_page.html",{'obj':obj})


def add_feedback(request):
    user_id=request.session['uid']
    feed=request.POST.get('feedback')
    s=text_test(feed)
    name=''
    pr_id=request.POST['id']
    obj4=Feedback.objects.filter(lid=user_id,pro_id=pr_id)
    if obj4.count()>=2:
        return HttpResponse("<script>alert('You can add only two reviews');window.location.href='/user_homepage/'</script>")

    obj3=Order.objects.filter(uid=user_id,product_id=pr_id,status='delivered')
    if obj3.count()<=0:
        return HttpResponse("<script>alert('Purchase product to add review');window.location.href='/user_homepage/'</script>")

    from datetime import datetime
    now = datetime.now()
    id = 1
    formatted_date = now.strftime('%Y-%m-%d %H:%M:%S')
    
    today = datetime.today()
    print(today,'=================')

    
    if s==1:

        obj2=Feedback.objects.filter(date__year=today.year, date__month=today.month, date__day=today.day,sentiment=1)
        if obj2.count()>5:
            return HttpResponse("<script>alert('Negative Feedback limit reached!!!');window.location.href='/user_homepage/'</script>")

    
    obj3=User.objects.get(lid=user_id)
    name=obj3.name

    obj=Feedback(name=name,feedback=feed,lid=user_id,pro_id=pr_id,sentiment=s)
    obj.save()
    obj5=Product.objects.get(id=pr_id)
    obj6=Feedback.objects.filter(pro_id=pr_id)
    obj7=Feedback.objects.filter(pro_id=pr_id,sentiment=1)
    obj8=Feedback.objects.filter(pro_id=pr_id,sentiment=0)
    cntp=obj8.count()
    cntn=obj7.count()
    cnt2=obj6.count()
    
    if cnt2==0:
        cnt2=1

    #pr=(cntp/cnt2)*10
    #nr=(cntn/cnt2)*10
    #r=(pr-nr)
    pr=(cntp/cnt2)*5
    r=round(pr,1)
    print(user_id)
    obj5.rating=r
    obj5.save()
    print(pr_id)
    print(s)
    print(feed)
    return HttpResponse("<script>alert('Review added');window.location.href='/user_homepage/'</script>")

def sview_orders(request):
    lid=request.session['uid']
    obj3=Shop.objects.get(lid=lid)
    sh_id=obj3.reg_id
    obj=Order.objects.filter(sh_id=lid).exclude(status='cancelled').order_by('-date')
    return render(request,"sview_orders.html",{'prs':obj})

def cancel(request):
    ord=request.POST.get('id')
    obj=Order.objects.get(id=ord)
    obj.status='cancelled'
    obj.save()
    pid=obj.product_id
    obj2=Product.objects.get(id=pid)
    cnt=int(obj2.quantity)+1
    obj2.quantity=cnt
    obj2.save()

    
    return HttpResponse("<script>alert('Order Cancelled');window.location.href='/user_homepage/'</script>")


