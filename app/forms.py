
from django import forms
from django.contrib.auth.models import User
from .models import LostItemReport


class ItemForm(forms.ModelForm):
    class Meta:
        model = LostItemReport
        fields = [
            'item_name',
            'category',
            'description',
            'date_found',
            'location',
            'image',
        ]
        widgets = {
            'item_name': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full p-2 border rounded'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded',
                'rows': 3
            }),
            'date_found': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full p-2 border rounded'
            }),
            'location': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded'
            }),
        }


class EditProfileForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

