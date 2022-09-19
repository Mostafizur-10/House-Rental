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
from first_app.models import Ad
from django.core.paginator import Paginator
from django.db.models import Count

# Create your views here.


def index(request):
    return render(request,'base.html')


def rent(request):
    list = Ad.objects.get_queryset().order_by('username')
    paginator = Paginator(list,2) 
    page_number = request.GET.get('page',1)
    page_obj = paginator.page(page_number)
    cat_list = (Ad.objects.values('category').annotate(dcount = Count('category')).order_by())

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
    dash = Ad.objects.all() 
    return render(request,'dashboard.html',{'dash':dash})


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
            user = form.save(commit=False)  
            user.is_active = False  
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain_name': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
                
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(  
                        mail_subject, message,to=[to_email]  
            )  
            email.send() 
            user.save()   
            return redirect('/login')  
    else:  
        form = SignupForm()  
    return render(request, 'varification.html', {'form': form})  



def house(request,username):
    selected_house = get_object_or_404(Ad, username = username)
    details = Ad.objects.all()
    house = {}
    
    for x in range(0,len(details)):
        if details[x] == selected_house:
            house2 = { 'owner_location':details[x].owner_location,
                        'category':details[x].category,
                        'owner_img':details[x].owner_img,
                        'price':details[x].price,
                        'image1':details[x].image1,
                        'image2':details[x].image2,
                        'image3':details[x].image3,
                        'image4':details[x].image4,                        
                        'no_of_room':details[x].no_of_room,
                        'pub_date':details[x].pub_date,
                        'contact':details[x].contact,
                        'username':details[x].username,
                     }
    
    house.update(house2)
    # print(house)

    return render(request,'house.html',{'selected_house':house})


def ads(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        contact = request.POST.get('phone_no')
        owner_location = request.POST.get('address')

        owner_img = request.FILES.get('owner_img')
        
        no_of_room = request.POST.get('nor')
        image1 = request.FILES.get('img-house-1')
        image2 = request.FILES.get('img-house-2')
        image3 = request.FILES.get('img-house-3')
        image4 = request.FILES.get('img-house-4')
        pub_date = request.POST.get('publish_date')
        price = request.POST.get('price')
        map = request.POST.get('map')

        ads_store = Ad(username=username,owner_location=owner_location,
        owner_img=owner_img,contact=contact,map=map,
        price=price,no_of_room=no_of_room,pub_date=pub_date,image1=image1,
        image2=image2,image3=image3,image4=image4)

        selected = request.POST.get('category')

        if selected == 'flat':
            ads_store.category='flat'

        elif selected == 'villa':
            ads_store.category='villa'

        elif selected == 'house':
            ads_store.category='house'


        elif selected == 'hostel':
            ads_store.category='hostel'



        ads_store.save()
        messages.success(request,"Successfully Published")
    return render(request,'ads.html')