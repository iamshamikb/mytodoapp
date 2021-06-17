from django.forms import ModelForm
from .models import ToDo

class Todoform(ModelForm):
    class Meta:
        model = ToDo
        fields = ('title', 'memo', 'important')