from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import CustomUserCreationForm, RoomForm
from .models import Message, Room, Topic, User


def loginPage(request):
    """
    This method checks if the user is trying to login
    The code goes ahead to check if the user with the username already exists in the database via the User model
    """
    page = "login"
    if request.user.is_authenticated:
        return redirect("home")  # if the user is already logged in, redirect to the home page

    if request.method == "POST":
        username = request.POST.get("username").lower()
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
            messages.error(request, "Username or password does not exist")

    context = {"page": page}
    return render(request, "base/login_register.html", context)


def logoutView(request):
    logout(request)
    return redirect("login")


def registerPage(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # this is the data inputed by the user
        if form.is_valid():
            user = form.save(commit=False)  # this gives access to the user data for data manipulation and cleaning
            user.username = user.username.lower()  # this ensures that the username is lowercase
            user.save()  # this saves the user data to the database
            login(request, user)  # this creates a session in the browser with the user details
            return redirect("home")  # takes the logged in user to the home page
        else:
            messages.error(request, "An error occurred during registration")
    return render(request, "base/login_register.html", {"form": form})


def home(request):
    q = (
        request.GET.get("q") if request.GET.get("q") != None else ""
    )  # q is a variable that stores the value of the input field
    # q would be an empty string if the input field is empty which would match all available room
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
    room_messages = room.message_set.all().order_by("-created_at")
    # this is a django built in feature that allows us to access the messages in a room, backward foreign key
    participants = (
        room.participants.all()
    )  # since it's a many-to-many relationship, the .all is more appropriate for a backward foreign key
    if request.method == "POST":
        message = Message.objects.create(user=request.user, room=room, body=request.POST.get("body"))
        room.participants.add(
            request.user
        )  # this is to ensure that any user that sends a message in the room is added to the participants list of the room
        return redirect("room", pk=pk)
    context = {"room": room, "room_messages": room_messages, "participants": participants}
    return render(request, "base/room.html", context)


@login_required(login_url="login")
# this decorator is used to check if the user is logged in. If not, the user will be redirected to the login page
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
        room.delete()
        return redirect("home")  # takes the user back to the home page after the delete is successful
    return render(
        request, "base/delete.html", {"obj": room}
    )  # the 'obj' here references the obj in the delete.html file. For this function, the room is the object


@login_required(login_url="login")
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)  # fetches the message with the unique id

    if request.user != message.user:
        return HttpResponse("You are not authorized to delete this message")

    if request.method == "POST":
        Message.delete()
        return redirect("home")  # takes the user back to the home page after the delete is successful
    return render(request, "base/delete.html", {"obj": message})
