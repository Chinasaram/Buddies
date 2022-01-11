from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RoomForm
from .models import Room, Topic, User


def loginPage(request):
    """
    This method checks if the user is trying to login
    The code goes ahead to check if the user with the username already exists in the database via the User model
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        """
        The try error catcher checks if the user exist and returns an error message if otherwise. 
        If user exists, the view uses the django authenticate method to verify user.
        The error message is rendered by django messages
        """
        try:
            user = User.objects.get(username=username)

        except:
            pass
        user = authenticate(request, username=username, password=password)
        # this checks if the credentials inputed by the user matches the credentials on the database.
        # A user object that matches the credentials will be outputted

        if user is not None:  # if a user object is returned
            login(request, user)  # this creates a session in the browser with the user details
            return redirect("home")  # takes the logged in user to the home page
        else:
            messages.error(request, "Username or password is incorrect")

    context = {}
    return render(request, "base/login_register.html", context)


def logoutView(request):
    logout(request)
    return redirect("home")


def home(request):
    q = (
        request.GET.get("q") if request.GET.get("q") != None else ""
    )  # this checks if the request has a value it's going to be an empty string
    rooms = Room.objects.filter(  # if topic__name is set directly as q, the home page will be empty until a particular topic is selected then a list of rooms bearing that topic will be rendered.
        Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(description__icontains=q)
    )
    """
    the icontains is a non-casesensitive value ensures whatever detail in the topic name is typed in the q variable renders
    rooms that has that value. E.g, if pyt is typed in the search bar, all python related rooms will be rendered even
    if it is not completly spelt out. In summary, icontains act as a wildcard....more info @ https://docs.djangoproject.com/en/3.2/ref/models/querysets/#icontains
    Q in this case is a built in django feature used for filtering data. the | is an 'or' operator.
    """
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {"rooms": rooms, "topics": topics, "room_count": room_count}
    return render(request, "base/home.html", context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {"rooms": room}
    return render(request, "base/room.html", context)


@login_required(login_url="login")
def createRoom(request):
    form = RoomForm()
    if request.method == "POST":
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("home")

    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def updateRoom(request, pk):  # pk is the primary key used in referencing the data.
    room = Room.objects.get(
        id=pk
    )  # you create a variable that would contain the data you are fetching from the database using the ....get(id=pk) which is specific due to the pk you passed in.
    form = RoomForm(
        instance=room
    )  # the instance is passed so the form can contain the values contained in the room variable. If no instance is passed, the form will come empty.

    if request.method == "POST":
        form = RoomForm(
            request.POST, instance=room
        )  # this is to check if the method is a post method so the instance fetched can be updated with the new values instead of creating another data entirely in the database.
        if form.is_valid():
            form.save()
            return redirect("home")
    context = {"form": form}
    return render(request, "base/room_form.html", context)


@login_required(login_url="login")
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)  # fetches the room with the unique id
    if request.method == "POST":
        room.delete()  # deletes the room
        return redirect("home")  # takes the user back to the home page after the delete is successful
    return render(
        request, "base/delete.html", {"obj": room}
    )  # the 'obj' here references the obj in the delete.html file. For this function, the room is the object
