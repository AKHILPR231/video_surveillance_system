import smtplib
from datetime import datetime
from email.mime.text import MIMEText

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from videosurveillance_app.models import *


def login(request):
    return render(request, "loginindex.html")

def logout(request):
    auth.logout(request)
    return render(request, "loginindex.html")



def logincode(request):
    username=request.POST['textfield']
    password = request.POST['textfield2']
    try:
        ob=logintable.objects.get(username=username,password=password)
        if ob.type == 'admin':
            ob1=auth.authenticate(username="admin",password="admin")
            if ob1 is not  None:
                auth.login(request,ob1)
            return HttpResponse('''<script> alert("successfully login");window.location="/admin_home"</script>''')
        elif ob.type == 'police':
            request.session['lid']=ob.id
            ob1 = auth.authenticate(username="admin", password="admin")
            if ob1 is not None:
                auth.login(request, ob1)
            return HttpResponse('''<script>alert("successfully login");window.location="/security_home"</script>''')
        else:
            return HttpResponse('''<script>alert("invalid");window.location="/"</script>''')
    except:
        return HttpResponse('''<script>alert("invalid");window.location="/"</script>''')


@login_required(login_url='/')
def admin_home(request):
    return render(request,"admin1index.html")

@login_required(login_url='/')
def manage_security(request):
    ob=policetable.objects.all()
    return render(request, "html pg/manag securty nd assgn wrk to scrty 1.html",{'val':ob})

@login_required(login_url='/')
def searchsecurity(request):
    name=request.POST['textfield']
    ob=policetable.objects.filter(name__istartswith=name)
    return render(request, "html pg/manag securty nd assgn wrk to scrty 1.html",{'val':ob})


@login_required(login_url='/')
def edit_security(request,id):
    request.session['pp']=id
    ob=policetable.objects.get(id=id)
    return render(request, "html pg/editsecurity.html",{"val":ob})

@login_required(login_url='/')
def editsecurity_code(request):
    try:
        name = request.POST['textfield']
        gender = request.POST['radiobutton']
        idproof = request.FILES['file']
        fs = FileSystemStorage()
        fp = fs.save(idproof.name, idproof)
        phone = request.POST['textfield2']
        email = request.POST['textfield3']
        rank = request.POST['rank']

        ob1 = policetable.objects.get(id=request.session['pp'])

        ob1.name = name
        ob1.address = gender
        ob1.idproof = fp
        ob1.phone = phone
        ob1.email = email
        ob1.rank = rank
        ob1.save()
        return HttpResponse('''<script>alert("successfully edited");window.location="/manage_security#about"</script>''')
    except:
        name = request.POST['textfield']
        gender = request.POST['radiobutton']
        phone = request.POST['textfield2']
        email = request.POST['textfield3']
        rank = request.POST['rank']

        ob1 = policetable.objects.get(id=request.session['pp'])

        ob1.name = name
        ob1.address = gender
        ob1.phone = phone
        ob1.rank = rank
        ob1.email = email
        ob1.save()
        return HttpResponse('''<script>alert("successfully edited");window.location="/manage_security#about"</script>''')

@login_required(login_url='/')
def delete_security(request,id):
    ob=logintable.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted");window.location="/manage_security#about"</script>''')


@login_required(login_url='/')
def add_security(request):
    return render(request, "html pg/manag security 2.html")
@login_required(login_url='/')
def addsecuritycode(request):
    name=request.POST['textfield']
    gender=request.POST['radiobutton']
    idproof=request.FILES['file']
    fs=FileSystemStorage()
    fp=fs.save(idproof.name,idproof)
    phone=request.POST['textfield2']
    email=request.POST['textfield3']
    uname=request.POST['textfield4']
    password=request.POST['textfield5']
    rank=request.POST['rank']

    ob=logintable()
    ob.username=uname
    ob.password=password
    ob.type='police'
    ob.save()

    # try:
    #     gmail = smtplib.SMTP('smtp.gmail.com', 587)
    #     gmail.ehlo()
    #     gmail.starttls()
    #     gmail.login('videosurveillance012@gmail.com', 'pkqo faiz koek axek')
    #     print("login=======")
    # except Exception as e:
    #     print("Couldn't setup email!!" + str(e))
    # msg = MIMEText("Your password id : " + str(password) +"and Username :"+uname)
    # print(msg)
    # msg['Subject'] = 'anzen'
    # msg['To'] = email
    # msg['From'] = 'videosurveillance012@gmail.com'
    #
    # print("ok====")
    #
    # try:
    #     gmail.send_message(msg)
    # except Exception as e:
    #     print("rrrrrrr",e)

    ob1=policetable()
    ob1.LOGIN=ob
    ob1.name=name
    ob1.address=gender
    ob1.idproof=fp
    ob1.phone=phone
    ob1.email=email
    ob1.rank=rank
    ob1.save()

    return HttpResponse('''<script>alert("successfully Added");window.location="/manage_security#about"</script>''')

@login_required(login_url='/')
def assign_work1(request,id):
    request.session['pp']=id
    return render(request, "html pg/assign wrk to security 1.html")
@login_required(login_url='/')
def add_assignworkcode(request):
    work = request.POST['textfield2']
    # details = request.POST['textfield3']
    # date=request.POST['textfield4']

    ob=emergencytable()
    ob.police=policetable.objects.get(id=request.session['pp'])
    ob.message=work
    ob.response='pending'
    ob.date=datetime.now()
    ob.time=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("successfully Added");window.location="/manage_security#about"</script>''')





def assign_work2(request):
    ob = assignworktable.objects.all()
    return render(request, "html pg/assign wrk to secty 2.html",{'val':ob})

def view_report(request):
    ob = reporttable.objects.all()
    return render(request, "html pg/view daily report.html",{'val':ob})
@login_required(login_url='/')
def view_feedback(request):
    ob = feedbacktable.objects.all()
    return render(request, "html pg/view feedback.html",{'val':ob})


def view_complaint(request):
    ob = complainttable.objects.all()
    return render(request, "html pg/view complaint nd reply 1.html",{'val':ob})

def searchcomplaint(request):
    date=request.POST['textfield']
    ob=complainttable.objects.filter(date=date)
    return render(request, "html pg/view complaint nd reply 1.html",{'val':ob})
@login_required(login_url='/')
def send_reply(request,id):
    request.session['rpl']=id
    return render(request, "html pg/send reply 2.html")

def sdrply(request):
    reply=request.POST['textfield']
    ob=complainttable.objects.get(id=request.session['rpl'])
    ob.reply=reply
    ob.date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("successfully replied");window.location="/view_complaint#about"</script>''')

@login_required(login_url='/')
def add_camera1(request):
    ob = cameratable.objects.all()
    return render(request, "html pg/manage camera 1.html",{'val':ob})


@login_required(login_url='/')
def delete_camera(request,id):
    ob = cameratable.objects.get(id=id)
    ob.delete()
    return HttpResponse('''<script>alert("Deleted");window.location="/add_camera1#about"</script>''')

@login_required(login_url='/')
def add_camera2(request):
    return render(request, "html pg/manage camera 2.html")

@login_required(login_url='/')
def add_cameracode(request):
    cameranumber = request.POST['textfield']
    latitude = request.POST['textfield2']
    longitude = request.POST['textfield3']

    ob=cameratable()
    ob.camera_no=cameranumber
    ob.latitude=latitude
    ob.longitude=longitude
    ob.save()
    return HttpResponse('''<script>alert("successfully Added");window.location="/add_camera1#about"</script>''')


def view_notification(request):
    ob = alerttable.objects.all()
    return render(request, "html pg/view notification.html",{'val':ob})
@login_required(login_url='/')
def security_home(request):
    return render(request, "security1index.html")

@login_required(login_url='/')
def viewassign_work(request):
    ob=emergencytable.objects.filter(police__LOGIN__id=request.session['lid'])
    return render(request, "html pg/view assigned work.html",{'val':ob})

@login_required(login_url='/')
def updatework_status(request,id):
    request.session['nid']=id
    return render(request, "html pg/update work status.html")


def updt(request):
    a=request.POST['textfield']
    ob=assignworktable.objects.get(id= request.session['nid'])
    ob.status=a
    ob.date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("successfully updated");window.location="/viewassign_work#about"</script>''')


@login_required(login_url='/')
def add_report(request,id):
    request.session['oo']=id
    return render(request, "html pg/add daily report.html")

@login_required(login_url='/')
def add_reportcode(request):
    report = request.POST['textfield']
    # description = request.POST['textfield2']

    ob = emergencytable.objects.get(id=request.session['oo'])
    ob.response = report
    ob.save()
    return HttpResponse('''<script>alert("Report Added");window.location="/viewassign_work#about"</script>''')

@login_required(login_url='/')
def send_feedback(request):
    return render(request, "html pg/send feedback.html")


@login_required(login_url='/')
def sdfeedback(request):
    comments=request.POST['textfield']
    ob=feedbacktable()
    ob.security = policetable.objects.get(LOGIN__id=request.session['lid'])
    ob.comments = comments
    ob.date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("feedback added");window.location="/security_home"</script>''')

@login_required(login_url='/')
def viewnotification(request):
    ob=notificationtable.objects.all()
    return render(request,"html pg/view notification_admin.html",{"val":ob})



def view_reply(request):
    ob = complainttable.objects.all()
    return render(request, "html pg/view reply.html",{'val':ob})


def searchreply(request):
    date=request.POST['textfield']
    ob=complainttable.objects.filter(date=date)
    return render(request, "html pg/view reply.html",{'val':ob})

def send_complaint(request):
    return render(request, "html pg/send complaint and view reply.html")

def sdcmpt(request):
    complaint=request.POST['textfield']
    ob=complainttable()
    ob.security=securitytable.objects.get(LOGIN__id=request.session['lid'])
    ob.complaint=complaint
    ob.reply="pending"
    ob.date=datetime.now()
    ob.save()
    return HttpResponse('''<script>alert("complaint added");window.location="/view_reply#about"</script>''')

@login_required(login_url='/')
def camera_info(request):
    obj = cameratable.objects.all()
    return render(request, "html pg/view camera info.html",{'val':obj})


@login_required(login_url='/')
def view_alert(request):
    ob = notificationtable.objects.all()
    return render(request, "html pg/view alert.html",{'val':ob})

