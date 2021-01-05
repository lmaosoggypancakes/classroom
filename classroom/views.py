from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth import _get_user_session_key
import json
from django.views.decorators.csrf import csrf_exempt
from .models import *
from django.core.paginator import Paginator
import random
from django.http import HttpResponseForbidden
from django.shortcuts import render
from .forms import *
from django.contrib.auth.decorators import login_required
from .emails import reset_pw
from .ip import get_ip
import datetime as date
import pytz

utc=pytz.UTC
# Create your views here.
def index(request): 
    if request.user.is_authenticated:
        if not request.user.is_teacher:
            classrooms = Classroom.objects.filter(student=request.user)
        elif request.user.is_teacher:
            classrooms = Classroom.objects.filter(teacher=request.user)
        return render(request, "classroom/index.html", {
            "classrooms": classrooms
        })
    else:
        return HttpResponseRedirect(reverse('new'))

@csrf_exempt
def new(request):
    if request.method == "POST":
        first = request.POST.get('first')
        last = request.POST.get('last')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_type = request.POST.get('user')
        if user_type == "Student":
            user_type = False
        else:
            user_type = True
        try:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first, last_name=last, is_teacher=user_type)
            user.save()
        except IntegrityError:
            return render(request, "classroom/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "classroom/new.html")
@login_required
def new_classroom(request):
    if request.method == "POST":
        if request.user.is_teacher:
            name = request.POST.get('name')
            icon = request.POST.get('icon')
            code = random.randint(100000, 999999)
            classroom = Classroom(name=name, teacher=request.user, join_code=code, picture=icon)
            classroom.save()
            return render(request, "classroom/create.html", {
                "class": classroom,
                "message": f"You're all set! You can invite students with the access code {code}."
            })
    else:
        default_icons = [
            'https://www.pngkit.com/png/detail/449-4495513_download-math-icon-png-clipart-mathematics-computer-clipart.png',
            'https://img.favpng.com/22/21/16/science-icon-png-favpng-ScW1Ma2iTE8npYLYPrRYyagkQ.jpg',
            'https://cpng.pikpng.com/pngl/s/89-893168_subject-icon-png-english-icon-transparent-background-clipart.png',
            'https://img2.pngio.com/download-free-png-social-studies-standards-ogden-city-school-school-social-studies-png-512_512.png'
        ]
        return render(request, "classroom/create.html", {
            "icons": default_icons
        })
@login_required
def join(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            code = int(request.POST["code"])
            classrooms = Classroom.objects.values_list('join_code', flat=True)
            if code in classrooms:
                classroom = Classroom.objects.get(join_code=code)
                classroom.student.add(request.user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "classroom/join.html", {"message": "Classroom code does not exist"})
    else:
        return render(request, "classroom/join.html")
def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "classroom/new.html", {
                "message": "Invalid username and/or password."
            })
    elif request.method == "GET":
        return render(request, "classroom/login.html")


def search(request):
    pass

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("new"))
@login_required
def class_view(request, id):
    if not request.user.is_authenticated:
        return render(request, "classroom/new.html")
    else:
        user_class = Classroom.objects.get(id=id)
        classmates = user_class.student.all()
        assigments = request.user.assignments.all()
        if request.user.is_teacher: 
            # get hw that's filled out
            completed_hw = Assignment.objects.filter(in_class=user_class).exclude(body="")
        else:
            completed_hw = None
        if not assigments.exists():
            assigments = "Congrats! You have no assignments for this class! ;)"
        if request.user in classmates or request.user.username == user_class.teacher.username:
            return render(request, "classroom/class.html", {
                "classmates": classmates,
                "class": user_class,
                "assignments": assigments,
                "submissions": completed_hw
                #"assignments": User.assignments.all,
                
            })
        else:
            return HttpResponseForbidden("Not allowed!")
def get_user(request): 
    return JsonResponse(request.user.serialize(), safe=False)
@login_required
def create_assignment(request, id):
    if request.user.is_teacher:
        if request.method == "POST":
            # unpack the JSON
            data = json.loads(request.body)
            # first, get the data from the unpacked JSON
            q = str(data.get("question", ""))
            day = int(data.get("day", ""))
            month = int(data.get("month", ""))
            year = int(data.get("year", ""))
            due_date = date.datetime(year, month, day)
            classroom = Classroom.objects.get(id=id)
            students = classroom.student.all()
            print(list(students))
            for h in list(students):
                print(h)
                if q == "":
                    return JsonResponse({"message": "question cannot be blank."})
                # answer will be left empty for now, students will submit via a fetch 
                body = ""
                # create one assignment for each student in the classroom
                hw = Assignment(question=q, body=body, assigned_to=h, in_class=classroom, due_date=due_date)
                hw.save()
            return JsonResponse({"message": "Assignment successfully created!"})
        else: 
            return JsonResponse({"message": "whatever you did, it was wrong"})

def reset_email(request, email): 
        users = []
        for user in User.objects.all():
            users.append(user.email)
        if email in users: 
            reset_pw(request, email)
            return JsonResponse({"message": "email sent! please check your inbox."})
        else: 
            return JsonResponse({"message": "error: email does not exist in our database."})

def reset_view(request, hash):
        # logged in users cannot access this page
        if request.method == "GET":
            # use the hash to check if the request exists
            pw_req = PasswordReset.objects.get(hashed_code=hash)
            return render(request, "classroom/reset.html", {
                "pw": pw_req
            })
            return HttpResponseRedirect(reverse("index"))


        elif request.method == "POST": 
            new_pw = request.POST.get('password')
            password_request = PasswordReset.objects.get(hashed_code=hash)
            user = password_request.for_user
            user.password = new_pw
            user.save()
            # log the user back in 
            login(request, user)
            # once it's saved delete the request
            password_request.delete()
            return HttpResponseRedirect(reverse('index'))
def work(request, class_id, hw_id):
    classroom = Classroom.objects.get(id=int(class_id))
    hw = Assignment.objects.get(id=hw_id)
    if not hw.assigned_to == request.user:
        return HttpResponseRedirect(reverse('index'))
    if request.method == "POST":
        body = request.POST["body"]
        if body == "":
            return render(request, "classroom/class.html", {
                "message": "body must not be blank."
            })
        else:
            
            hw.body = body
            hw.date_turned_in = date.datetime.now()
            hw.save()
            print(hw.due_date)
            print(utc.localize(hw.date_turned_in))
            lmao = hw.date_turned_in.strftime("%B %d, %Y")
            if (hw.due_date) > utc.localize(hw.date_turned_in):
                message = f"assignment submitted on time on {lmao}"
                late = False
            else: 
                message = f"assignment submitted late on {lmao}"
                late = True
            hw.late = late
            hw.save()
            return render(request, "classroom/index.html", {
                "message": message
            })
    elif request.method == "GET":
        return render(request, "classroom/work.html", {
            "class": classroom,
            "hw": hw
        })

def leave_or_delete(request, id):
    classroom = Classroom.objects.get(id=id)
    if request.user.is_authenticated:
        if request.user.is_teacher:
            classroom.delete()
            return JsonResponse({
                "message": "classroom succesfully deleted"
            })
        else:
            if request.user in classroom.student.all():
                classroom.student.remove(request.user)
                return JsonResponse({
                    "message": "you have left the classroom."
                })
    else:
        return JsonResponse({
            "message": "you are not logged in."
        })

def handler404(request, exception):
    return render(request, "classroom/404.html", {
        "error": exception
    })