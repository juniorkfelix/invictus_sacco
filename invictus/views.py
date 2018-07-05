from django.shortcuts import render
from django.shortcuts import redirect
from .models import Contact
from .models import reg_members
from .models import Profile
from .models import Accounts
from .models import Transact
from .models import Jipange_Acc
from .models import Timiza_Acc
from .models import Fixed_Acc
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.db.models import Avg, Max, Min, Sum
from .forms import DocumentForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import MySQLdb

# Create your views here.
def index(request):
    return render(request, 'invictus/home.html')

def about(request):
    return render(request, 'invictus/about.html')

def loan_dev(request):
    return render(request, 'invictus/loan_dev.html')

def loan_biz(request):
    return render(request, 'invictus/loan_biz.html')

def salary_adv(request):
    return render(request, 'invictus/salary_adv.html')

def biz_fix(request):
    return render(request, 'invictus/biz_fix.html')

def timiza(request):
    return render(request, 'invictus/timiza.html')

def jipange(request):
    return render(request, 'invictus/jipange.html')


def open_acc(request):
    return render(request, 'invictus/open_acc.html')


def statuary(request):
    return render(request, 'invictus/statuary.html')



def investment(request):
    return render(request, 'invictus/investment.html')



def sacco_dep(request):
    return render(request, 'invictus/sacco_dep.html')


@csrf_exempt
def contact(request):
        if request.method == 'POST':
            if request.POST.get('name') and request.POST.get('email') and request.POST.get('phone')  and request.POST.get('message'):
                post=Contact()
                post.name= request.POST.get('name')
                post.email= request.POST.get('email')
                post.phone= request.POST.get('phone')
                post.message= request.POST.get('message')
                post.save()
                
                return render(request, 'invictus/contact.html')

        else:
                return render(request, 'invictus/contact.html')


@csrf_exempt
def member_regi(request):
        if request.method == 'POST':
             if request.POST.get('fullname') and request.POST.get('dob') and request.POST.get('idno') and request.POST.get('mobile') and request.POST.get('email') and request.POST.get('employer') and request.POST.get('address') and request.POST.get('county') and request.POST.get('religion') and request.POST.get('month_cont') and request.POST.get('kin_fullname') and request.POST.get('kin_ID') and request.POST.get('kin_phone') and request.POST.get('kin_relation') and request.POST.get('transaction_reference'):       	
                post=reg_members()
                post.fullname= request.POST.get('fullname')
                post.dob= request.POST.get('dob')
                post.idno= request.POST.get('idno')
                post.mobile= request.POST.get('mobile')
                post.email= request.POST.get('email')
                post.employer= request.POST.get('employer')
                post.address = request.POST.get('address')
                post.county = request.POST.get('county')
                post.religion = request.POST.get('religion')
                post.month_cont = request.POST.get('month_cont')
                post.kin_id = request.POST.get('kin_ID')
                post.kin_phone = request.POST.get('kin_phone')
                post.kin_relation = request.POST.get('kin_relation')
                post.kin_fullname = request.POST.get('kin_fullname')
                post.datestamp = datetime.datetime.now()
                post.transaction_reference = request.POST.get('transaction_reference')
                maxid = reg_members.objects.order_by('-id')[0] 
                p = maxid.id
                post.member_no = p + 10000
                post1=Accounts()
                post1.member_no = p + 10000
                post1.phone = request.POST.get('mobile')
                post1.email= request.POST.get('email')
                post1.acc_balance = 0
                post1.save()
                

                if post.save():
                    

                    return render(request, 'invictus/member_reg.html')               
                   
                else:

                	request.session['post.fullname'] = post.fullname
                	request.session['post.idno'] = post.idno
                	request.session['post.member_no'] = post.member_no
                	request.session['post.email'] = post.email
                	return redirect('upload')            

               


        else:
                return render(request, 'invictus/member_reg.html')


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            if form.save():
             member_no = request.session['post.member_no']
             request.session['post.member_no'] = member_no                  
             return redirect('signup')

               
    else:
        form = DocumentForm(initial = {'idno':request.session['post.idno']})
        fullname = request.session['post.fullname']
        return render(request, 'invictus/upload.html', {'form': form , 'names' : fullname })

def signup(request):
    fname = request.session['post.fullname']
    member_n = request.session['post.member_no']
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your Invictus account.'
            message = render_to_string('invictus/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            if email.send():
                return HttpResponse('Please confirm your email address to complete the registration into Invictus Sacco.')
            else:
                form = SignupForm(initial = {'username':request.session['post.member_no']})
                messages.info(request, 'Unsuccesful!!.Please try again.')
                return render(request, 'invictus/signup.html', {'form': form , 'names' : fname , 'member_n' : member_n})

    else:
        form = SignupForm(initial = {'username':request.session['post.member_no']})

    return render(request, 'invictus/signup.html', {'form': form , 'names' : fname , 'member_n' : member_n})

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('index')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)

        if user is not None and user.is_active:
            request.session['user_name'] = username
            auth.login(request, user)
            return redirect('/')
        else:
            return render(request, 'invictus/login.html', {'error': 'Your username or password is invalid.' })
    else:
        return render(request, 'invictus/login.html')

def logout_view(request):
    auth.logout(request)
    # Redirect to a success page.
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return redirect("/")

def member_portal(request):
    if request.user.is_authenticated():
        reg = request.session['user_name']
        try:
            details = reg_members.objects.get(member_no=reg)
        except reg_members.DoesNotExist:
            raise Http404("Question does not exist")
        return render(request, 'invictus/member_portal.html', {'reg': reg , 'details' : details})
    else:
        messages.info(request, 'You must be logged in to access the portal!')
        return redirect('login')

@csrf_exempt
def accounts(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if 'pay' in request.POST:
                if request.POST.get('account') and request.POST.get('amount'):
                    post=Accounts()
                    post.member_no= request.POST.get('account')
                    #cash = Accounts.objects.filter(Q(member_no=request.POST.get('account')) | Q(somefield='bar'))
                    details = Accounts.objects.get(member_no=request.POST.get('account'))
                    p = details.acc_balance
                    q = 0
                    q += int(request.POST.get('amount')) 
                    post.acc_balance = p + q
                    Accounts.objects.filter(member_no=request.POST.get('account')).update(acc_balance= post.acc_balance)
                    post1=Transact()
                    post1.member_no= request.POST.get('account')
                    post1.deposit = request.POST.get('amount')
                    post1.acc_balance = post.acc_balance
                    post1.save() 
                    reg = request.session['user_name']
                    try:
                        details = reg_members.objects.get(member_no=reg)
                        acc = Accounts.objects.get(member_no=reg)            
                    except reg_members.DoesNotExist:
                        raise Http404("Member Does Not Exist.")
                    return render(request, 'invictus/accounts.html', {'reg': reg , 'details' : details ,'acc' : acc})
            elif 'mini' in request.POST:
                if request.POST.get('email'):
                    post=Accounts()
                    reg = request.session['user_name']
                    try:
                        details = reg_members.objects.get(member_no=reg)
                        acc = Accounts.objects.get(member_no=reg)            
                    except reg_members.DoesNotExist:
                        raise Http404("Member Does Not Exist.")
                    return render(request, 'invictus/accounts.html', {'reg': reg , 'details' : details ,'acc' : acc})


        else:
            reg = request.session['user_name']
            try:
                details = reg_members.objects.get(member_no=reg)
                acc = Accounts.objects.get(member_no=reg)            
            except reg_members.DoesNotExist:
                raise Http404("Member Does Not Exist.")
            return render(request, 'invictus/accounts.html', {'reg': reg , 'details' : details ,'acc' : acc})
    else:
        messages.info(request, 'You must be logged in to access the portal!')
        return redirect('login')

def help(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            reg = request.session['user_name']
            if 'help' in request.POST:
                if request.POST.get('account') and request.POST.get('question'):
                    post.Help()
                    post.member_no = request.POST.get('account')
                    post.question = request.POST.get('question')
                    post.save()
                    return redirect('help')

        else:
            reg = request.session['user_name']
            try:
                details = reg_members.objects.get(member_no=reg)
                acc = Accounts.objects.get(member_no=reg)            
            except reg_members.DoesNotExist:
                raise Http404("Member Does Not Exist.")
            return render(request, 'invictus/help.html', {'reg': reg , 'details' : details ,'acc' : acc})
    else:        
        messages.info(request, 'You must be logged in to access the portal!')
        return redirect('login')

def loans(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            reg = request.session['user_name']
            if 'help' in request.POST:
                if request.POST.get('account') and request.POST.get('question'):
                    post.Help()
                    post.member_no = request.POST.get('account')
                    post.question = request.POST.get('question')
                    post.save()
                    return redirect('loans')

        else:
            reg = request.session['user_name']
            try:
                details = reg_members.objects.get(member_no=reg)
                acc = Accounts.objects.get(member_no=reg)            
            except reg_members.DoesNotExist:
                raise Http404("Member Does Not Exist.")
            return render(request, 'invictus/loans.html', {'reg': reg , 'details' : details ,'acc' : acc})
    else:        
        messages.info(request, 'You must be logged in to access the portal!')
        return redirect('login')

@csrf_exempt
def savings(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            if 'create' in request.POST:
                reg = request.session['user_name']
                if request.POST.get('account') == 'Jipange_Acc':
                    if Jipange_Acc.objects.filter(member_no=reg).exists():                        
                        return redirect('savings')
                    else:
                        post=Jipange_Acc()
                        post.member_no = reg
                        post.acc_balance = 0
                        post.save()
                        return redirect('savings')
                elif request.POST.get('account') == 'Timiza_Acc':
                    if Timiza_Acc.objects.filter(member_no=reg).exists():                        
                        return redirect('savings')
                    else:
                        post=Timiza_Acc()
                        post.member_no = reg
                        post.acc_balance = 0
                        post.save()
                        return redirect('savings')
                elif request.POST.get('account') == 'Fixed_Acc':
                    if Fixed_Acc.objects.filter(member_no=reg).exists():                        
                        return redirect('savings')
                    else:
                        post=Fixed_Acc()
                        post.member_no = reg
                        post.acc_balance = 0
                        post.save()
                        return redirect('savings')
                else:
                    return redirect('savings')
            elif 'deposit' in request.POST:
                reg = request.session['user_name']
                if request.POST.get('account') == 'Jipange_Acc' and request.POST.get('amount'):
                    if Jipange_Acc.objects.filter(member_no=reg).exists():
                        post=Jipange_Acc()
                        post.member_no = reg
                        account = Jipange_Acc.objects.get(member_no=reg)
                        p = 0
                        p += int(account.acc_balance)
                        q = 0
                        q += int(request.POST.get('amount'))
                        post.acc_balance = p + q
                        Jipange_Acc.objects.filter(member_no=reg).update(acc_balance= post.acc_balance)
                        return redirect('savings')
                    else:
                        return redirect('savings')
                elif request.POST.get('account') == 'Timiza_Acc' and request.POST.get('amount'):
                    if Timiza_Acc.objects.filter(member_no=reg).exists():
                        post=Timiza_Acc()
                        post.member_no = reg
                        account = Timiza_Acc.objects.get(member_no=reg)
                        p = 0
                        p += int(account.acc_balance)
                        q = 0
                        q += int(request.POST.get('amount'))
                        post.acc_balance = p + q
                        Timiza_Acc.objects.filter(member_no=reg).update(acc_balance= post.acc_balance)
                        return redirect('savings')
                    else:
                        return redirect('savings')
                elif request.POST.get('account') == 'Fixed_Acc' and request.POST.get('amount'):
                    if Timiza_Acc.objects.filter(member_no=reg).exists():
                        post=Fixed_Acc()
                        post.member_no = reg
                        account = Fixed_Acc.objects.get(member_no=reg)
                        p = 0
                        p += int(account.acc_balance)
                        q = 0
                        q += int(request.POST.get('amount'))
                        post.acc_balance = p + q
                        Fixed_Acc.objects.filter(member_no=reg).update(acc_balance= post.acc_balance)
                        return redirect('savings')
                    else:
                        return redirect('savings')
                else:
                    return redirect('savings')

        else:
            reg = request.session['user_name']
            try:
                details = reg_members.objects.get(member_no=reg)
                acc = Accounts.objects.get(member_no=reg)
                if Jipange_Acc.objects.filter(member_no=reg).exists():
                   jip = Jipange_Acc.objects.get(member_no=reg)
                   acco = 'Your account balance is: Ksh.'
                else:
                    acco = 'You do not have an account yet.'
                    jip = 'Please Create an account.'
                if Timiza_Acc.objects.filter(member_no=reg).exists():
                   tim = Timiza_Acc.objects.get(member_no=reg)
                   acco1 = 'Your account balance is: Ksh.'
                else:
                    acco1 = 'You do not have an account yet.'
                    tim = 'Please Create an account.'
                if Fixed_Acc.objects.filter(member_no=reg).exists():
                   fix = Fixed_Acc.objects.get(member_no=reg)
                   acco2 = 'Your account balance is: Ksh.'
                else:
                    acco2 = 'You do not have an account yet.'
                    fix = 'Please Create an account.'
            except reg_members.DoesNotExist:
                raise Http404("Member Does Not Exist.")
            return render(request, 'invictus/jipange_acc.html', {'reg': reg , 'details' : details ,'acc' : acc , 'jip' : jip , 'acco' : acco, 'tim' : tim ,'acco1' : acco1 ,'fix' :fix ,'acco2' : acco2})
    else:
        messages.info(request, 'You must be logged in to access the portal!')
        return redirect('login')


def invictusadmin(request):
    return render(request, 'invictus/admin.html')

def invictusmembers(request):
    members_list = reg_members.objects.all()
    paginator = Paginator(members_list, 5)

    page = request.GET.get('page')
    try:
        members = paginator.page(page)
    except PageNotAnInteger:
        members = paginator.page(1)
    except EmptyPage:
        members = paginator.page(paginator.num_pages)

    return render(request, 'invictus/invictus_members.html', {'members':members})

def invictusapprovemembers(request):
    members_list = reg_members.objects.all()
    paginator = Paginator(members_list, 1)

    page = request.GET.get('page')
    try:
        member_details = paginator.page(page)
    except PageNotAnInteger:
        member_details = paginator.page(1)
    except EmptyPage:
        member_details = paginator.page(paginator.num_pages)

    return render(request, 'invictus/invictus_member_approve.html', {'member_details':member_details})
