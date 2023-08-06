from django import forms
from .admin import UserCreationForm
from .models import MyUser,Recruiter,Candidate,Apply
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm,SetPasswordForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation




class CustomUsercreationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    class Meta:
        model=MyUser
        fields= [ 'email']
        widgets = {
        # 'date_of_birth':forms.DateInput(attrs={'class':'form-control','id':'datepicker'}),
         'email':forms.EmailInput(attrs={'class':'form-control'}),  }
        

class RecruiterForm(forms.ModelForm):
    class Meta:
        model=Recruiter
        fields=["Company_Name","Position","job_description","Salary","Categories"]
        widgets={
            'Company_Name':forms.TextInput(attrs={'class':'form-control'}),
            'Position':forms.TextInput(attrs={'class':'form-control'}),

            'job_description':forms.Textarea(attrs={'class':'form-control'}),
            'Salary':forms.NumberInput(attrs={'class':'form-control'}),
            'Categories':forms.Select(attrs={'class':'form-control'}),

            
            
            }

class AuthenticationCustomForm(AuthenticationForm):
    class Meta:
        model=MyUser
        fields=['username','password']
      

class CandidateDetailsForm(forms.ModelForm):
    class Meta:
        model=Candidate
        fields=['Name','DOB','mobile','Experience','Location','Resume']
        widgets={
        'Name':forms.TextInput(attrs={'class':'form-control'}),
        'DOB':forms.DateInput(attrs={'class':'form-control','placeholder ':'YYYY-MM-DD'}),
        'mobile':forms.TextInput(attrs={'class':'form-control'}),
        'Experience':forms.NumberInput(attrs={'class':'form-control'}),
        'Location':forms.TextInput(attrs={'class':'form-control'}),




            
        }

class ApplyForm(forms.ModelForm):
   class Meta:
       model=Apply
       fields=['message']
       widgets={
            'message':forms.Textarea(attrs={'class':'form-control'})
        }
       

class MypasswordresetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email",'class':'form-control'}),
    )


class MySetpassword(SetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password",'class':'form-control'}),
    )    