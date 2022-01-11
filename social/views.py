from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.db.models import Q
from .models import Messages, Room, Topic
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .form import RoomForm
# Create your views here.



def topics(request):
    topics = Topic.objects.all()
    context = {'topics': topics}
    return render(request, 'topics_all.html', context)

def loginUser(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.warning(request, 'Invalid Credentials')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Invalid Credentials')
    context = {'page' : page}                      
    return render(request, 'login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    page = 'register'
    if request.user.is_authenticated:
        return redirect('home')
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            return redirect('login')
        else:
            messages.error(request, 'Invalid Credentials')
    context = {'form' : form}
    return render(request, 'login_register.html',context)

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
                                Q(topic__name__icontains = q) |
                                Q(name__icontains = q)
                                )
    topics = Topic.objects.all()[:5]
    room_count = rooms.count()
    activity_messages = Messages.objects.all()[:4]
    context = {'rooms':rooms, 'topics':topics, 'room_count' : room_count,
               'activity_messages' : activity_messages}
    return render(request, 'home.html', context)

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    topics = Topic.objects.all()
    rooms = user.room_set.all()
    activity_messages = Messages.objects.all()
    context = {'user':user, 'rooms':rooms, 'topics':topics, 'activity_messages' : activity_messages}
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def room(request, pk):
    room = Room.objects.get(id=pk)
    count_messages = room.messages_set.all()
    participants = room.paticipants.all()
    if request.method == 'POST':
        message = Messages.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )
        room.paticipants.add(request.user)
        return redirect('room', pk=room.id)
    context = {'room' : room, 'count_messages' : count_messages,'participants' : participants }
    return render(request, 'room.html', context)

@login_required(login_url='login')
def createroom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topics')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        
        return redirect('home')
        
        
        """
            We can Also use this but form
        """
        # form = RoomForm(request.POST)
        # if form.is_valid():
        #     room = form.save(commit=False)
        #     room.host = request.user
        #     room.save()
              # return redirect('home')
    context = {'form':form,'topics' : topics}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('<h1><b>404</h1> Not Allowed')
    if request.method == 'POST':
        topic_name = request.POST.get('topics')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        # form = RoomForm(request.POST, instance=room)
        # if form.is_valid():
        #     form.save()
        #     return redirect('home')
    context = {'form':form,'topics':topics,'room':room}
    return render(request, 'room_form.html', context)

@login_required(login_url='login')
def deleteroom(request, pk):
    room = Room.objects.get(id=pk)
    if request.method == 'POST':
        room.delete()
        return redirect('home')
    context = {'room' : room}
    return render(request, 'delete.html', context)