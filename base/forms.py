from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from .models import Room, User


class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = "__all__"


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "email",
        )
