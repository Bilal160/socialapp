from django.db import models
from django.forms import ModelForm, fields
from .models import Room,Topic,Messages

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host', 'paticipants']

