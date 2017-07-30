from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import bcrypt
import re


now = datetime.now()

class WishManager(models.Manager):
    def validator(self, item, id):
        errors = []
        if len(item) < 1:
            errors.append("Item name is required.")
        elif len(item) < 3:
            errors.append("Item name must be more than 3 characters.")

        if len(errors) > 0:
            return (False, errors)
        else:
            wish = Wish.wishManager.create(item = item, wisher_id = id)
            #
            # user = User.objects.get(id = id)
            Join.objects.create(user_id=id, wish_id=wish.id)

            return (True, wish)



class UserManager(models.Manager):
    def validator(self, postData):
        errors = {}

        if len(postData['name']) < 3:
            errors['namelen'] = "Name must be at least 3 characters."
        elif not re.match('[A-Za-z]+', postData['name']):
            errors['namevalid'] = "Name must only contain letters."

        if len(postData['username']) < 3:
            errors['unamelen'] = "Username must be at least 3 characters."
        elif User.objects.filter(username=postData['username']):
            errors['unametaken'] = "Username is taken."

        # if len(postData['password']) < 1:
        #     errors['passlen'] = "Password is required."
        if len(postData['password']) < 8:
            errors['passlen'] = "Password must be at least 8 characters."

        if len(postData['confirm_pw']) < 1:
            errors['pass2len'] = "Password confirmation is required."
        elif postData['confirm_pw'] != postData['confirm_pw']:
            errors['passconpass'] = "Passwords do not match."

        if len(postData['date_hired']) < 1:
            errors['dhiredlen'] = "Date hired is required."
        elif datetime.strptime(postData['date_hired'], '%Y-%m-%d') > now:
            errors['dhiredinval'] = "Invalid hired date. Date cannot be in the future."

        return errors

    def loginvalidator(self, postData):
        errors = {}
        username = postData['username']
        password = postData['password']

        if len(username) < 1:
            errors['no_uname'] = "Please input a username."
        if len(password) < 1:
            errors['no_pass'] = "Please input a password."
        if not User.objects.filter(username=username):
            errors['uname_exist'] = "This username is not registered in our database."

        if User.objects.filter(username=username):
            user = User.objects.get(username = username)
            if not bcrypt.hashpw(str(password), str(user.password)) == user.password:
                errors['incorrect_pass'] = "Incorrect password: does not match password stored in database."
        return errors



class User(models.Model):
    name = models.CharField(max_length = 255)
    username = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    date_hired = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User object: {} {} {} {}>".format(self.id, self.name, self.username, self.date_hired)

class Wish(models.Model):
    item = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    wisher = models.ForeignKey(User, related_name = "wishes")
    wishManager = WishManager()
    def __repr__(self):
        return "<Wish object: {} {}>".format(self.name, self.date_added)

class Join(models.Model):
    user = models.ForeignKey(User, related_name = "users")
    wish = models.ForeignKey(Wish, related_name = "wishes")
    def __repr__(self):
        return "<Join object: User_id = {} Wish_id = {}>".format(self.user_id, self.wish_id)
