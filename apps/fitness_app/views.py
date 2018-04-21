# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from .models import User, Activity, Workout
from django.contrib import messages

def index(request):
    return render(request, "fitness_app/index.html")

def register(request):
    check = User.objects.register(
        request.POST["name"],
        request.POST["username"],
        request.POST["email"],
        request.POST["dob"],
        request.POST["height"],
        request.POST["weight"],
        request.POST["password"],
        request.POST["confirm"]
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Welcome to Dojo Fitness, {}".format(request.POST["username"]))
        return redirect("/dashboard")

def login(request):
    check = User.objects.login(
        request.POST["email"],
        request.POST["password"]
    )

    if not check["valid"]:
        for error in check["errors"]:
            messages.add_message(request, messages.ERROR, error)
        return redirect("/")
    else:
        request.session["user_id"] = check["user"].id
        messages.add_message(request, messages.SUCCESS, "Welcome back, {}".format(check["user"].username))
        return redirect("/dashboard")

def dashboard(request):
    # BMI: height in meters divided by weight in kilograms squared

    user = User.objects.get(id=request.session["user_id"])
    user_workouts = Workout.objects.filter(user_id=request.session["user_id"])
    other_workouts = Workout.objects.all().exclude(user_id=request.session["user_id"]).order_by("-start")
    followed_users = user.followed_users.all()

    for u in followed_users:
        other_workouts = other_workouts.exclude(user_id = u.id)

    h = user.height*0.0254
    w = user.weight/2.2

    data = {
        "user": user,
        "user_workouts": user_workouts,
        "other_workouts": other_workouts[:3],
        "bmi": "{}".format(w / h**2)[0:4]
    }

    return render(request, "fitness_app/dashboard.html", data)

def logout(request):
    request.session.clear()
    messages.add_message(request, messages.SUCCESS, "See you later")
    return redirect("/")

def new_workout(request):
    return render(request, "fitness_app/new_workout.html", {"activities": Activity.objects.all()})

def add_workout(request):
    check = Workout.objects.addWorkout(
        request.POST["duration"],
        request.POST["units"],
        request.POST["start_date"] + " " + request.POST["start_time"],
        request.POST["activity"],
        request.session["user_id"]
    )
    print check
    return redirect("/dashboard")

def follow(request, user_id):
    user = User.objects.get(id=request.session["user_id"])
    followed_user = User.objects.get(id=user_id)
    user.followed_users.add(followed_user)
    return redirect("/dashboard")