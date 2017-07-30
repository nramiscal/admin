from django.shortcuts import render, redirect
from django.contrib import messages
from models import User, UserManager
from models import Wish, WishManager, Join
from django.contrib import messages
from datetime import datetime
import bcrypt


def index(request):
    # User.objects.all().delete()
    # Wish.wishManager.all().delete()
    # Join.objects.all().delete()
    return render(request, 'wl_app/index.html')


def register(request):
    print request.POST
    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag,error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        print errors
        return redirect('/')
    else:
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        User.objects.create(name = request.POST['name'], username = request.POST['username'], password = pwhash, date_hired = request.POST['date_hired'])
        request.session['name'] = request.POST['name']
        request.session['id'] = User.objects.last().id
        # print request.session['id']
        return redirect('/my_page')
    return redirect('/')


def login(request):
    print request.POST
    errors = User.objects.loginvalidator(request.POST)
    print errors
    if len(errors):
        for tag,error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        print errors
        return redirect('/')
    else:
        request.session['id'] = User.objects.get(username = request.POST['username']).id
        request.session['name'] = User.objects.get(username = request.POST['username']).name
        return redirect('/my_page')

def my_page(request):

    wishes = Wish.wishManager.all()

    #all wishes this user has
    joins = Join.objects.filter(user_id=request.session['id'])
    #remove wishes that also are in joins
    for join in joins:
        wishes = wishes.exclude(id = join.wish_id)

    context = {
        "wishes" : wishes,
        "joins" : joins,
        # "user" : user,
    }

    return render(request, 'wl_app/my_page.html', context)

def add(request):
    return render(request, 'wl_app/create.html')

# def create(request):
#     print request.POST
#     return redirect('my_page')


def create(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['id'])
        wish = Wish.wishManager.validator(request.POST['item'], request.session['id'])
        if wish[0]:
            # print wish
            return redirect('/my_page')
        else:
            for error in wish[1]:
                messages.add_message(request, messages.ERROR, error)
            return render(request, 'wl_app/create.html')




def logout(request):
    request.session.clear()

    return redirect('/')

def home(request):
    return redirect('/my_page')


def join(request, wish_id):
    # print trip_id
    user = User.objects.get(id=request.session['id'])
    wish = Wish.wishManager.get(id = wish_id)

    Join.objects.create(user_id=request.session['id'], wish_id=wish_id)
    return redirect('/my_page')

def delete(request, wish_id):
    wish = Wish.wishManager.get(id = wish_id)
    # print wish.item
    wish.delete()
    return redirect('/my_page')

def remove(request, wish_id):
    join = Join.objects.filter(user_id = request.session['id']).get(wish_id = wish_id).delete()
    return redirect('/my_page')


def wish_item(request, wish_id):
    user = User.objects.get(id=request.session['id'])
    wish = Wish.wishManager.get(id=wish_id)
    wisher_id = Wish.wishManager.get(id=wish_id).wisher_id
    wisher = User.objects.get(id = wisher_id)
    joins = Join.objects.filter(wish_id = wish_id)

    context = {
        "wish" : wish,
        "wisher" : wisher,
        "joins" : joins,
    }

    return render(request, 'wl_app/item.html', context)
