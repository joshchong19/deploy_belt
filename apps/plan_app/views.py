from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages

def index(request):
    return render(request, "plan_app/index.html")

def dashboard(request):
    if "user" in request.session:
        context = {
            "user" : Users.objects.get(id = request.session["user"]),
            "all_trips" : Trips.objects.all(),
        }
        return render(request, "plan_app/dashboard.html", context)
    else:
        return redirect("/")

def new(request):
    if "user" in request.session:
        context = {
            "user" : Users.objects.get(id = request.session["user"])
        }
        return render(request, "plan_app/new.html",context)
    else:
        return redirect("/")

def show(request,id):
    if "user" in request.session:
        context = {
            "logged_user" : Users.objects.get(id = request.session["user"]),
            "trip" : Trips.objects.get(id = id)
        }
        return render(request, "plan_app/show.html",context)
    else:
        return redirect("/")

def edit(request,id):
    if "user" in request.session:
        context = {
            "user" : Users.objects.get(id = request.session["user"]),
            "trip" : Trips.objects.get(id = id)
        }
        return render(request, "plan_app/edit.html",context)
    else:
        return redirect("/")


def join(request,id):
    join_trip = Trips.objects.get(id = id)
    user = Users.objects.get(id = request.session["user"])
    user.attending_trips.add(join_trip)
    return redirect("/dashboard")

def cancel(request,id):
    cancel_trip = Trips.objects.get(id = id)
    user = Users.objects.get(id = request.session["user"])
    user.attending_trips.remove(cancel_trip)
    return redirect("/dashboard")

def delete(request,id):
    delete_trip = Trips.objects.get(id = id)
    delete_trip.delete()
    return redirect("/dashboard")

def process(request):
    form = request.POST
    if form["form"] == "register":
        errors = Users.objects.valid(form)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect("/")
        else:
            hash_pw = bcrypt.hashpw(form["password"].encode(),bcrypt.gensalt())
            created_user = Users.objects.create(first_name = form["fname"], last_name = form["lname"], email = form["email"], password = hash_pw.decode())
            request.session["user"] = created_user.id
            return redirect("/")

    if form["form"] == "login":
        if len(form["email"]) < 1 or len(form["password"]) < 1:
            messages.error(request,"Please enter email/password")
            return redirect("/")
        else:
            userobj = Users.objects.filter(email = form["email"])
            user = userobj[0]
            print(user)
            if bcrypt.checkpw(form["password"].encode(), user.password.encode()):
                request.session["user"] = user.id
                messages.success(request,"You have been successfully logged in!")
                return redirect("/dashboard")
            else:
                messages.error(request, "You could not be logged in")
                return redirect("/")

def newtrip(request):
    form = request.POST
    errors = Trips.objects.valid(form)
    if "submit" in request.POST:
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value)
            return redirect("/trips/new")
        else:
            creating_user = Users.objects.get(id = request.session["user"])
            new_trip = Trips.objects.create(destination = form["destination"], start_date = form["start"], end_date = form["end"], plan = form["plan"], created_by = creating_user)
            creating_user.attending_trips.add(new_trip)
            return redirect("/dashboard")
    if "cancel" in request.POST:
        return redirect("/dashboard")

def update(request,id):
    form = request.POST
    errors = Trips.objects.valid(form)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request,value)
        return redirect(f"/trips/edit/{id}")
    else:
        update_trip = Trips.objects.get(id = id)
        update_trip.destination = form["destination"]
        update_trip.start_date = form["start"]
        update_trip.end_date = form["end"]
        update_trip.plan = form["plan"]
        update_trip.save()
        return redirect("/dashboard")


def logout(request):
    if "user" in request.session:
        request.session.pop("user")
        return redirect("/")