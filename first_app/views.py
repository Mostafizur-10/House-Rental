from django.http import HttpResponse  
from django.shortcuts import render, redirect ,get_object_or_404 
from django.contrib.auth import login, authenticate ,logout 
from .forms import SignupForm  
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string   
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage 
from .token import account_activation_token
from django.contrib import messages
from django.contrib.auth import get_user_model
from first_app.models import Ad,Profile
from django.core.paginator import Paginator
from django.db.models import Count
from random import randint
import pgeocode



def index(request):
    return render(request,'base.html')


def rent(request):
    
    list = Ad.objects.get_queryset().order_by('-datetime')
    paginator = Paginator(list,3) 
    page_number = request.GET.get('page',1)
    page_obj = paginator.page(page_number)
    cat_list = (Ad.objects.values('category').annotate(dcount = Count('category')).order_by())
    

    if request.method == 'POST':
        new_list=[]
        id_list = request.POST.getlist('check_cat')
        my_dict = Ad.objects.all().values()
        for i in range(0,len(id_list)):
            for j in range(0,len(my_dict)):
                if id_list[i] == str(my_dict[j]['category']):
                    new_list.append(my_dict[j])
        
        return render(request,'listing.html',{'page_obj':page_obj,'count_cat':cat_list,'new_list':new_list})


    return render(request, 'listing.html', {'page_obj':page_obj,'count_cat':cat_list})


def login_process(request):
    
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(request, username=loginusername , password=loginpassword)


        if user is not None:
            login(request,user)
            return redirect('/dashboard')
        else:
            messages.error(request,"Invalid Credentials, Please try again")
            return redirect('/login')
    
    return render(request,'login.html')


def logout_process(request):
    logout(request)
    return redirect('/')

def dashboard(request):
    dash = Ad.objects.filter(username=str(request.user))
    pre_post = Profile.objects.filter(username=str(request.user)).values()
    p1 = ""
    if pre_post:
        p1 = pre_post[0]['owner_image']

    if request.method == 'POST':
        Profile.objects.filter(username = str(request.user)).delete()
        username = request.user
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        address = request.POST.get('address')
        mobile_no = request.POST.get('mobile_no')
        owner_image = request.FILES.get('owner_image')
        email = request.POST.get('email')


        if not mobile_no:
            mobile_no = None 
        if not owner_image:
            owner_image = p1
            
        store = Profile(username=username,fname=fname,lname=lname,address=address,email=email,owner_image=owner_image,phone=mobile_no)
        selected = request.POST.get('gender')


        if selected == 'male':
            store.gender='male'

        elif selected == 'female':
            store.gender='female'

        store.save()
        pre_post = Profile.objects.filter(username=str(request.user)).values()
        dash = Ad.objects.filter(username=str(request.user))
        messages.success(request,"Successfully updated")
        
        return render(request,'dashboard.html',locals())  
    return render(request,'dashboard.html',locals())


def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
   
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        messages.success(request,"Successfully registered")
        return redirect('/rent') 
    else: 
        messages.success(request,"Successfully registered") 
        return redirect('/rent')  

def signup(request):  
    
    
    if request.method == 'POST':  
        form = SignupForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save()  
            # user.is_active = False  
            # to get the domain of the current site  
            # current_site = get_current_site(request)  
            # mail_subject = 'Activation link has been sent to your email id'  
            # message = render_to_string('acc_active_email.html', {  
            #     'user': user,  
            #     'domain_name': current_site.domain,  
            #     'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
            #     'token':account_activation_token.make_token(user),  
                
            # })  
            # to_email = form.cleaned_data.get('email')  
            # email = EmailMessage(  
            #             mail_subject, message,to=[to_email]  
            # )  
            # email.send() 
            user.save()   
            return redirect('/login')  
    else:  
        form = SignupForm()  
    return render(request, 'varification.html', {'form': form})  



def house(request,house_id):
    selected_house = get_object_or_404(Ad,house_id=house_id)
    details = Ad.objects.all()
    house = {}
    for x in range(0,len(details)):
        if details[x] == selected_house:
            house2 = {  
                        'price':details[x].price,
                        'image1':details[x].image1,
                        'image2':details[x].image2,
                        'image3':details[x].image3,
                        'image4':details[x].image4,                        
                        'no_of_room':details[x].no_of_room,
                        'pub_date':details[x].pub_date, 
                        'username':details[x].username,
                        'description':details[x].description,
                        'division':details[x].division,
                        'district':details[x].district,
                        'thana':details[x].thana,
                        'union':details[x].union,
                        'value':details[x].value,
                     }
    
    house.update(house2)
    x = Ad.objects.filter(house_id=house_id).values()
    y = x[0]['username']
    host = Profile.objects.filter(username=str(y)).values()   
    
    return render(request,'house.html',{'selected_house':house,'host':host})


def ads(request):


    get_username = request.user
    x = Profile.objects.filter(username=str(get_username))
    pos = randint(-10000000000,10000000000)

    if not x:
        messages.warning(request,"Complete your profile before any advertisement")
        return render(request,'dashboard.html')

    else:
        if request.method == 'POST':

            username = request.user
            house_id = str(request.user) + str(pos)
            no_of_room = request.POST.get('nor')
            image1 = request.FILES.get('img-house-1')
            image2 = request.FILES.get('img-house-2')
            image3 = request.FILES.get('img-house-3')
            image4 = request.FILES.get('img-house-4')
            pub_date = request.POST.get('publish_date')
            price = request.POST.get('price')
            postal_code = request.POST.get('postal_code')
            store = Ad(username=username,house_id=house_id,price=price,no_of_room=no_of_room,pub_date=pub_date,image1=image1,image2=image2,image3=image3,image4=image4)

            x = str(postal_code)
            y = pgeocode.Nominatim('BD')

            store.postal_code = postal_code
            store.division = y.query_postal_code(x).state_name
            store.district = y.query_postal_code(x).county_name
            store.thana = y.query_postal_code(x).community_name
            store.union = y.query_postal_code(x).place_name
            

            selected = request.POST.get('category')

            if selected == 'flat':
                store.category='flat'

            elif selected == 'villa':
                store.category='villa'

            elif selected == 'house':
                store.category='house'


            elif selected == 'hostel':
                store.category='hostel'

            store.save()
            pos = pos + 1
            messages.success(request,"Successfully Published")
        return render(request,'ads.html')

def custom(request,house_id):
    x = house_id
    selected_house = get_object_or_404(Ad,house_id=house_id)
    if request.method == 'POST':
       selected_house = Ad.objects.filter(house_id=house_id).values()
       get_status = request.POST.get('value')
       new_postal = request.POST.get('postal_code')
       new_price = request.POST.get('price')
       p0 = selected_house[0]['username']
       p1 = selected_house[0]['house_id']
       p2 = selected_house[0]['category']
       p3 = selected_house[0]['price']
       p4 = selected_house[0]['pub_date']
       p5 = selected_house[0]['no_of_room']
       p6 = selected_house[0]['image1']
       p7 = selected_house[0]['image2']
       p8 = selected_house[0]['image3']
       p9 = selected_house[0]['image4']
       p10 = selected_house[0]['division']
       p11 = selected_house[0]['district']
       p12 = selected_house[0]['thana']
       p13 = selected_house[0]['union']
       p14 = selected_house[0]['postal_code']
       p15 = selected_house[0]['datetime']
       p16 = selected_house[0]['description']

       
       store = Ad(username=p0,house_id=p1,no_of_room=p5,pub_date=p4,image1=p6,image2=p7,image3=p8,image4=p9,datetime=p15,
       category=p2,value=get_status,description=p16)

       if new_postal:
        x = str(new_postal)
        y = pgeocode.Nominatim('BD')
        store.postal_code = new_postal
        store.division = y.query_postal_code(x).state_name
        store.district = y.query_postal_code(x).county_name
        store.thana = y.query_postal_code(x).community_name
        store.union = y.query_postal_code(x).place_name
       else:
        store.postal_code = p14
        store.division=p10
        store.district=p11
        store.thana=p12
        store.union=p13

       if new_price:
        store.price = new_price  
       else:
        store.price = p3     
        

       Ad.objects.filter(house_id=house_id).delete()
       store.save()
       selected_house = get_object_or_404(Ad,house_id=house_id)
       messages.success(request,"Successfully updated")
       return render(request,'custom.html',locals())

    return render(request,'custom.html',locals())