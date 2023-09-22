from django.shortcuts import render,redirect

from django.http import HttpResponse

from .models import Transactions,Entrepreneurs,Registrations,Investors

# from django.contrib.auth.models import User,auth

from django.db import connection

import re
# Create your views here.


def home(request):
    return render(request,'home.html')
    
def invlogin(request):
    if request.method == 'POST':
        uid = request.POST['uname']
        password = request.POST['password']
        user_exists = Investors.objects.filter(user_name=uid).exists()
        if user_exists:
            user = Investors.objects.get(user_name=uid)
            password_match = (password == user.password)
        else:
            password_match = False
        if not user_exists or not password_match:
            return render(request,'inv_login.html',{'error':True,'name':'Incorrect Username or Password'})
        request.session['user'] = uid
        uname = Investors.objects.get(user_name=uid)
        companies = Entrepreneurs.objects.all()
        return redirect(curcamp)
    else:
        return render(request,"inv_login.html")

def entlogin(request):
    if request.method == 'POST':
        uid = request.POST['uname']
        password = request.POST['password']
        user_exists = Entrepreneurs.objects.filter(e_name=uid).exists()
        if user_exists:
            user = Entrepreneurs.objects.get(e_name=uid)
            password_match = (password == user.e_password)
            print('passed')
        else:
            password_match = False
        print(user_exists,password_match)
        if not user_exists or not password_match:
            return render(request,'ent_login.html',{'error':True,'name':'Incorrect username or password'})
        request.session['entp'] = uid
        ent = Entrepreneurs.objects.get(e_name=request.session['entp'])
        entinfo = Entrepreneurs.objects.filter(reg_no=ent.reg_no)
        return redirect('entprofile')
    else:
        return render(request,"ent_login.html")

def inreg(request):
    details = {"name":"","uname":"","email":"","mobile":""}
    if request.method == 'POST':
        try:
            details['name'] = request.POST['name']
            details['uname'] = request.POST['uname']
            details['email'] = request.POST['email']
            details['mobile'] = request.POST['mobile']
            if not re.match(r'^[a-zA-Z]+( {0,1}[a-zA-Z])*$',details['name']):
                raise Exception('Full name not proper')
            if not re.match(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{6,15}(?<![-._])$',details['uname']):
                raise Exception('username not proper')
            if Investors.objects.filter(user_name=details['uname']).count() == 1:
                return render(request,'e_reg.html',{'error': True,'msg':'Username already exists','details':details})
            if validateEmail(details['email']):
                if Investors.objects.filter(email=details['email']).count() == 1:
                    return render(request,'e_reg.html',{'error': True,'msg':'Email already exists','details':details})
            else:
                return render(request,'e_reg.html',{'error': True,'msg':'Invalid Email','details':details})
            if not validateMobile(details['mobile']):
                return render(request,'e_reg.html',{'error': True,'msg':'Invalid Mobile Number','details':details})
            if Investors.objects.filter(mobile_no=details['mobile']).count() == 1:
                return render(request,'e_reg.html',{'error': True,'msg':'Mobile no already exists','details':details})
            password = request.POST['password']
            cnfpassword = request.POST['cnfpassword']
            if password != cnfpassword:
                return render(request,'e_reg.html',{'error': True,'msg':'conform password not matched','details':details})
            tup = Investors(name=details['name'],user_name=details['uname'],email=details['email'],password=password,mobile_no=details['mobile'])
            tup.save()
            details['name'] = details['uname'] = details['email'] = details['mobile'] = ""
            return render(request,"e_reg.html",{"valid":True})
        except Exception as e:
            print(str(e))
            return render(request,"e_reg.html",{"invalid":True,'details':details})
    else:
        return render(request,'e_reg.html',{'details':details})

def entreg(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        if Entrepreneurs.objects.filter(e_name=uname).count() == 1:
            return render(request,'ent_reg.html',{'error': True,'name':'Username  already exists'})
        email = request.POST['email']
        if validateEmail(email):
            if Entrepreneurs.objects.filter(email=email).count() == 1:
                return render(request,'ent_reg.html',{'error': True,'name':'Email already exists'})
        else:
            return render(request,'ent_reg.html',{'error': True,'name':'Invalid Email'})
        company_name = request.POST['company_name']
        if Entrepreneurs.objects.filter(company_name=company_name).count() == 1:
            return render(request,'ent_reg.html',{'error': True,'name':'Company Name already exists'})
        reg_no = request.POST['reg_no']
        if Entrepreneurs.objects.filter(reg_no=reg_no).count() == 1:
            return render(request,'ent_reg.html',{'error': True,'name':'Reg No already exists'})
        mobile_no = request.POST['mobile_no']
        try:
            mn = int(mobile_no)
        except(Exception):
            return render(request,'ent_reg.html',{'error': True,'name':'Invalid Mobile Number '})
        if Entrepreneurs.objects.filter(mobile_no=mobile_no).count() == 1:
            return render(request,'ent_reg.html',{'error': True,'name':'Phone Number already exists'})
        category = request.POST['category']
        target_amt = request.POST['target_amt']
        try:
            ta = int(target_amt)
        except(Exception):
            return render(request,'ent_reg.html',{'error': True,'name':'Invalid Target Amount'})
        acc_no = request.POST['acc_no']
        try:
            mn = int(acc_no)
        except(Exception):
            return render(request,'ent_reg.html',{'error': True,'name':'Invalid Account Number '})
        if Entrepreneurs.objects.filter(acc_no=acc_no).count() == 1:
            return render(request,'ent_reg.html',{'error': True,'name':'Account no already exists'})
        acc_holder_name = request.POST['acc_holder_name']
        ifsc_code = request.POST['ifsc_code']
        password = request.POST['password']
        cnfpassword = request.POST['cnfpassword']
        if password != cnfpassword:
            return render(request,'ent_reg.html',{'error': True,'name':'conform password not matched'})
        description = request.POST['description']
        image = request.FILES['image']
        if Entrepreneurs.objects.filter(logo=image).count() == 1:
            return render(request,'ent_reg.html',{'error': True,'name':'Logo already exists'})
        try:
            tup = Registrations(reg_no=reg_no,company_name=company_name,category=category,description=description,user_name=uname,email=email,
            target_amt=target_amt,acc_no=acc_no,acc_holder_name=acc_holder_name,ifsc_code=ifsc_code,password=password,mobile_no=mobile_no,logo=image)
            tup.save()
            return render(request,"ent_reg.html",{"valid":True})
        except Exception as e: 
            return render(request,"ent_reg.html",{"invalid":True})
    else:
        return render(request,'ent_reg.html')

def curcamp(request):
    companies = Entrepreneurs.objects.all()
    if request.session.has_key("user"):
        x = Investors.objects.get(user_name=request.session['user']).name
        return render(request,'curr_pub.html',{'loggedin':True,'name':x,'companies':companies})
    else :
        return render(request,'curr_pub.html',{'companies':companies})

def portfolio(request):
    if request.session.has_key("user"):
        with connection.cursor() as cursor:
            cursor.execute('SELECT t.reg_no,e.company_name,t.invested_amt from transactions t inner join entrepreneurs e on e.reg_no = t.reg_no where t.user_name=%s',(request.session['user'],))
            investments = cursor.fetchall()
        return render(request,'portfolio.html',{'loggedin':True,'investments':investments})
    else:
        return redirect('invlogin')

def aboutus(request):
    return render(request,'aboutus.html')

def enttable(request):
    if request.session.has_key('entp'):
        regno = Entrepreneurs.objects.get(e_name = request.session['entp']).reg_no
        investors = Transactions.objects.filter(reg_no = regno)
        return render(request,'entrep_invstrs.html',{'loggedin':True,'investors':investors})
    else:
        return redirect('entlogin')

def entprofile(request):
    if request.session.has_key('entp'):
        newMail = ""
        newMobileno = ""
        if request.method == 'POST':
            uid = request.POST['username']
            password = request.POST['password']
            newMail = request.POST['email']
            newMobileno = request.POST['mobileno']
            entinfo = Entrepreneurs.objects.filter(e_name=request.session['entp'])[0]
            if not Entrepreneurs.objects.filter(e_name=uid).count() or not Entrepreneurs.objects.filter(e_password=password).count():
                return render(request,'entrep_profile.html',{'entinfo':entinfo,'mail_val':newMail,'mobileno_val':newMobileno, 'display':True,'msg':'Incorrect Username or password'})
            VALIDMAIL = VALIDMOBILE = True   # previous info
            if newMail != "" and not validateEmail(newMail):
                VALIDMAIL = False
                return render(request,'entrep_profile.html',{'entinfo':entinfo,'mail_val':newMail,'mobileno_val':newMobileno,'display':True,'msg':'Invalid Email'})
            if newMobileno != "" and not validateMobile(newMobileno):
                VALIDMOBILE = False
                return render(request,'entrep_profile.html',{'entinfo':entinfo,'mail_val':newMail,'mobileno_val':newMobileno,'display':True,'msg':'Invalid Mobileno'})
            if newMobileno != "" and newMail != "" and VALIDMAIL and VALIDMOBILE:
                Entrepreneurs.objects.filter(e_name=uid).update(email=newMail,mobile_no=newMobileno)
                newMail = newMobileno = ""
                entinfo = Entrepreneurs.objects.filter(e_name=request.session['entp'])[0]
                return render(request,'entrep_profile.html',{'entinfo':entinfo,'mail_val':newMail,'mobileno_val':newMobileno,'display':True,'msg':'Mail and Mobile no updated successfully'})
            elif newMail != "" and VALIDMAIL:
                Entrepreneurs.objects.filter(e_name=uid).update(email=newMail)
                newMail = ""
                entinfo = Entrepreneurs.objects.filter(e_name=request.session['entp'])[0]
                return render(request,'entrep_profile.html',{'entinfo':entinfo,'mail_val':newMail,'mobileno_val':newMobileno,'display':True,'msg':'Mail updated successfully'})
            elif newMobileno != "" and VALIDMOBILE:
                Entrepreneurs.objects.filter(e_name=uid).update(mobile_no=newMobileno)
                newMobileno = ""
                entinfo = Entrepreneurs.objects.filter(e_name=request.session['entp'])[0]
                return render(request,'entrep_profile.html',{'entinfo':entinfo,'mail_val':newMail,'mobileno_val':newMobileno,'display':True,'msg':'Mobile no updated successfully'})
        entinfo = Entrepreneurs.objects.filter(e_name=request.session['entp'])[0]
        return render(request,'entrep_profile.html',{'entinfo':entinfo,'mail_val':newMail,'mobileno_val':newMobileno})
    else:
        return redirect('entlogin')

def invlogout(request):
    try:
        del request.session["user"] 
    except KeyError:
        pass
    return redirect('home')

def entlogout(request):
    try:
        del request.session['entp']
        print('ent logout')
    except KeyError:
        pass
    return redirect('home')


def transfer(request):
    if request.session.has_key('user'):
        if request.method == "POST":
            regno = request.POST['regno']
            x = Entrepreneurs.objects.get(reg_no=regno).company_name
            return render(request,'payment.html',{'companyname':x})
        else:
            return redirect("curr_campaign")
    else:
        return redirect("invlogin")
        

def payment(request):
    if request.session.has_key('user'):
        inv_username = request.session['user']
        if request.method == 'POST':
            name = request.POST['cname']
            try:
                amount = int(request.POST['amt'])
            except(Exception):
                return render(request,"payment.html",{'message':'True','value':'Amount should be a number'})
            x = Entrepreneurs.objects.get(company_name=name)
            bal = x.target_amt - x.amt_collected
            if amount > bal or amount < 1:
                return render(request,"payment.html",{'message':True,'value':f'Amount should be less than or equal to {bal}'})
            if Transactions.objects.filter(user_name = inv_username, reg_no = x.reg_no).count():
                with connection.cursor() as cursor:
                    cursor.execute('UPDATE transactions SET invested_amt = invested_amt+%s where user_name=%s and reg_no=%s',(amount,inv_username,x.reg_no))
                    cursor.execute('UPDATE ENTREPRENEURS SET amt_collected = amt_collected+%s where reg_no=%s',(amount,x.reg_no))
                    return redirect('success')
            else:
                with connection.cursor() as cursor:
                    print("New Transaction")
                    cursor.execute('INSERT INTO transactions values (%s,%s,%s)',(inv_username,amount,x.reg_no))
                    cursor.execute('UPDATE ENTREPRENEURS SET amt_collected = amt_collected+%s where reg_no=%s',(amount,x.reg_no))
                    return redirect('success')
        else:
            return render(request,"payment.html")
    else:
        return redirect('invlogin')  

def success(request):
    return render(request,'success.html')

def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
def validateMobile(number):
    if not number.isnumeric():
        return False
    if len(number) != 10:
        return False
    if number[0] == "0":
        return False
    return True