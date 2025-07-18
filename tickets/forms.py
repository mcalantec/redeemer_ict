from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import *

#This is d validator for the matric number
matric_validator = RegexValidator(
    regex=r'^RUN/[A-Z]{3}/\d{2}/\d{4,5}$',
    message='Matric number must follow this format: RUN/ABC/21/12345'
)


class UserRegistrationForm(UserCreationForm):
    matric_number = forms.CharField(
        max_length=20,
        required=True,
        label='Matric Number',
        validators=[matric_validator],
        help_text='Format: RUN/CMP/21/10847'
    )
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES, required=True)
    department = forms.CharField(max_length=100, required=False)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2'
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.is_bound:
            matric = self.data.get('matric_number', '').strip().upper()
            record = StudentRecord.objects.filter(matric_number=matric).first()
            if record:
                self.fields['first_name'].initial = record.first_name
                self.fields['last_name'].initial = record.surname  
                self.fields['department'].initial = record.programme
                
                self.fields['first_name'].widget.attrs['readonly'] = True
                self.fields['last_name'].widget.attrs['readonly'] = True  
                self.fields['department'].widget.attrs['readonly'] = True

    def clean_matric_number(self):
        matric = self.cleaned_data['matric_number'].strip().upper()
        if not StudentRecord.objects.filter(matric_number=matric).exists():
            raise forms.ValidationError("ID not found in university records.")
        return matric
    
    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username


    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                department=self.cleaned_data['department'],
                phone_number=self.cleaned_data['phone_number']
            )
        return user
    
    def clean_email(self):
        email = self.cleaned_data['email']

        if not email.lower().endswith('@run.edu.ng'):
            raise forms.ValidationError("Please use your institutional email address (e.g., yourname@run.edu.ng).")
        
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        
        return email

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of the issue'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Detailed description of the problem'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'priority': forms.Select(attrs={'class': 'form-control'}),
        }

class TicketCommentForm(forms.ModelForm):
    class Meta:
        model = TicketComment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Add a comment...'
            }),
        }

