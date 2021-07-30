from __future__ import unicode_literals
from django.db import models
import re
from datetime import datetime , date

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
DATE_REGEX = re.compile(r"^(0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])[- /.](19|20)\d\d$")

class UsersManager(models.Manager):
    def valid(self, postData):
        errors = {}

        if len(postData["fname"]) < 1:
            errors["nofname"] = "First name is required"
        if len(postData["fname"]) > 0 and len(postData["fname"]) < 2:
            errors["shortfname"] = "First name must be at least 2 characters"
        if len(postData["lname"]) < 1:
            errors["nolname"] = "Last name is required"
        if len(postData["lname"]) > 0 and len(postData["lname"]) < 2:
            errors["shortlname"] = "Last name must be at least 2 characters"
        if len(postData["email"]) < 1:
            errors["noemail"] = "Email is required"
        if len(postData["email"]) > 0 and not EMAIL_REGEX.match(postData["email"]):
            errors["invalidemail"] = "Email is invalid"
        if Users.objects.filter(email = postData["email"]).exists() == True:
            errors["existemail"] = "This email already exists"
        if len(postData["password"]) < 1:
            errors["nopass"] = "Password is required"
        if len(postData["password"]) > 0 and len(postData["password"]) < 8:
            errors["shortpass"] = "Password must be atleast 8 characters"
        if postData["password"] != postData["passconfirm"]:
            errors["matchpass"] = "Password does not match"
        return errors

class TripsManager(models.Manager):
    def valid(self, postData):
        errors = {}

        if len(postData["destination"]) < 1:
            errors["nodestination"] = "Destination is required"
        if len(postData["destination"]) > 0 and len(postData["destination"]) < 3:
            errors["shortdestination"] = "Destination must be at least 3 characters"
        if len(postData["start"]) < 1:
            errors["nostart"] = "Please specify a start date"
        if len(postData["start"]) > 0 and not DATE_REGEX.match(postData["start"]):
            errors["invalidstart"] = "Please match the date format for start date"
        if len(postData["start"]) > 0 and len(postData["end"]) > 0:
            if DATE_REGEX.match(postData["start"]) and DATE_REGEX.match(postData["end"]):
                s = datetime.strptime(postData["start"], "%m/%d/%Y")
                e = datetime.strptime(postData["end"], "%m/%d/%Y")
                today = datetime.today()
                d = today.strftime("%m/%d/%Y")
                date = datetime.strptime(d,"%m/%d/%Y")
                if s < today:
                    errors["paststart"] = "Start date must be in the future"
                if e < s:
                    errors["endbefore"] = "End date must be after start date"
        if len(postData["end"]) < 1:
            errors["noend"] = "Please specify an end date"
        if len(postData["end"]) > 0 and not DATE_REGEX.match(postData["end"]):
            errors["invalidend"] = "Please match the date format for end date"
        if len(postData["plan"]) < 1:
            errors["noplan"] = "Plan is required"
        if len(postData["plan"]) > 0 and len(postData["plan"]) < 3:
            errors["shortplan"] = "Plan must be at least 3 characters"
        return errors



class Users(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now_add = True)
    objects = UsersManager()

class Trips(models.Model):
    destination = models.CharField(max_length = 255)
    start_date = models.CharField(max_length = 10)
    end_date = models.CharField(max_length = 10)
    plan = models.TextField()
    created_by = models.ForeignKey(Users, related_name = "created_trips", on_delete = models.CASCADE)
    users_attending = models.ManyToManyField(Users, related_name = "attending_trips")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = TripsManager()
