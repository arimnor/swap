from django.contrib import messages
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from swapapp import settings


def main_page_view(request):
   
    return render(request, 'main.html')

def authenticated_view(request):
   
    return render(request, 'authenticated.html')

def unatuhenticated_view(request):
    
    return render(request,'unauthenticated.html')

def profile_view(request):
    
    return render(request,'partials/profile.html')

def calender_view(request):
    
    return render (request,'calender/calender.html')

def elektrik_view(request):
    
    return render(request,"categories/elektrik-elektronikcategory.html")

def kişisel_view(request):
    
    return render(request,"categories/kişiselgelişimcategory.html")

def office_view(request):
    
    return render(request,"categories/officecategory.html")

def olasılık_view(request):
    
    return render(request,"categories/olasılıkcategory.html")

def tasarım_view(request):
    
    return render(request,"categories/tasarımcategory.html")

def yazılım_view(request):
    
    return render(request,"categories/yazılımcategory.html")

def odeme_view(request):
    
    return render(request,"partials/odeme.html")

def policy_view(request):
    
    return render(request,'policy/policy.html')
       
def register_instructor_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST['email']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "registration/register.html", {
                    "error": "Username is already taken",
                    "username": username,
                    "email": email
                })
            elif User.objects.filter(email=email).exists():
                return render(request, "registration/register.html", {
                    "error": "Email is already taken",
                    "username": username,
                    "email": email
                })
            elif not email.endswith('@edu.tr'):
                return render(request, 'registration/register_instructor.html',{
                'error': 'Sadece edu.tr uzantılı e-posta adresleri kabul edilmektedir.',
                'username': username,
                'email': email    
                })    
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False  # Kullanıcıyı hemen aktif hale getirmiyoruz
                user.save()

                # E-posta gönderimi
                current_site = get_current_site(request)
                from_email = settings.EMAIL_HOST_USER
                to_list = (user.email)
                subject = 'Activate Your Account'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(subject, message, from_email, [user.email])


                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return render(request, "registration/register.html", {
                "error": "Passwords do not match",
                "username": username,
                "email": email
            })
    return render(request, "registration/register.html")

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Hesabınız başarıyla aktif edilmiştir. Giriş yapabilirsiniz.')
        return redirect('main_page')  
    else:
        return HttpResponse('Aktivasyon linki geçersiz!')

def signout(request):
    logout(request)
    return redirect('main_page')

def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        email = request.POST['email']

        if password == repassword:
            if User.objects.filter(username=username).exists():
                return render(request, "registration/register.html", {
                    "error": "Username is already taken",
                    "username": username,
                    "email": email
                })
            elif User.objects.filter(email=email).exists():
                return render(request, "registration/register.html", {
                    "error": "Email is already taken",
                    "username": username,
                    "email": email
                })
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.is_active = False  # Kullanıcıyı hemen aktif hale getirmiyoruz
                user.save()

                # E-posta gönderimi
                current_site = get_current_site(request)
                from_email = settings.EMAIL_HOST_USER #nerden mail atacaksam ordan çektim
                to_list = (user.email) #kullanıcının maili
                subject = 'Activate Your Account'
                message = render_to_string('registration/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                })
                send_mail(subject, message, from_email, [user.email])


                return HttpResponse('Please confirm your email address to complete the registration')
        else:
            return render(request, "registration/register.html", {
                "error": "Passwords do not match",
                "username": username,
                "email": email
            })
    return render(request, "registration/register.html")

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # Kullanıcıyı doğrula
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('main_page')
        else:
            return render(request,"registration/login.html",{
                "error": "Username ya da parola yanlış"
            })    
             

    return render(request, 'registration/login.html')

def mobiluygulama_view(request):
   
    return render(request, 'lessons/Yazılım Courses/mobiluygulama.html')

def nesneyonelimliprg_view(request):
   
    return render(request, 'lessons/Yazılım Courses/nesneyonelimliprg.html')

def temelalgoritma_view(request):
   
    return render(request, 'lessons/Yazılım Courses/temelalgoritma.html')

def webgelistirme_view(request):
   
    return render(request, 'lessons/Yazılım Courses/webgelistirme.html')
    
def yazilimtest_view(request):
   
    return render(request, 'lessons/Yazılım Courses/yazilimtest.html')
    
def elektrikproje_view(request):
   
    return render(request, 'lessons/Elektrik - Elektronik Courses/elektrikproje.html')
    
def temelelektrik_view(request):
   
    return render(request, 'lessons/Elektrik - Elektronik Courses/temelelektrik.html')
    
def excell_view(request):
   
    return render(request, 'lessons/Microsoft365 Courses/excell.html')
    
def onenote_view(request):
   
    return render(request, 'lessons/Microsoft365 Courses/onenote.html')
        
def outlook_view(request):
   
    return render(request, 'lessons/Microsoft365 Courses/outlook.html')
        
def powerpoint_view(request):
   
    return render(request, 'lessons/Microsoft365 Courses/powerpoint.html')
        
def sharepoint_view(request):
   
    return render(request, 'lessons/Microsoft365 Courses/sharepoint.html')

def word_view(request):
   
    return render(request, 'lessons/Microsoft365 Courses/word.html')
    
def iletisimbecerileri_view(request):
   
    return render(request, 'lessons/Kişisel Gelişim Courses/iletisimbecerileri.html')

def motivasyon_view(request):
   
    return render(request, 'lessons/Kişisel Gelişim Courses/motivasyon.html')

def ozguven_view(request):
   
    return render(request, 'lessons/Kişisel Gelişim Courses/ozguven.html')

def zamanyonetimi_view(request):
   
    return render(request, 'lessons/Kişisel Gelişim Courses/zamanyonetimi.html')

def ictasarim_view(request):
   
    return render(request, 'lessons/Tasarım Courses/ictasarim.html')

def mimarlik_view(request):
   
    return render(request, 'lessons/Tasarım Courses/mimarlik.html')

def modatasarim_view(request):
   
    return render(request, 'lessons/Tasarım Courses/modatasarim.html')

def oyuntasarim_view(request):
   
    return render(request, 'lessons/Tasarım Courses/oyuntasarim.html')

def olasilikveistatistik_view(request):
   
    return render(request, 'lessons/Olasılık Courses/olasilikveistatistik.html')

def calender_view(request):
   
    return render(request, 'calender/calender.html')