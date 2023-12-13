from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import get_user_model
User = get_user_model()

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name',widget=forms.TextInput(attrs={"name":"first_name","id":"first_name","required":"required","class":"form-control", "placeholder":"First Name",}))
    middle_name = forms.CharField(required=False, max_length=100, help_text='Middle Name',widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Middle Name",}))
    last_name = forms.CharField(max_length=100, help_text='Last Name',widget=forms.TextInput(attrs={"name":"last_name","class":"form-control", "placeholder":"Last Name",}))
    CHOICES = (('', 'Gender'),('M', 'Male'),('F', 'Female'))
    gender = forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={"class":"form-select mb-0"}))
    email = forms.EmailField(required=False, max_length=150, help_text='Email',widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"name@example.com",}))
    phone = forms.CharField(max_length=150, help_text='Phone',widget=forms.TextInput(attrs={"id":"phone","class":"form-control", "placeholder":"eg 0808 000 0000",}))
    phone2 = forms.CharField(max_length=150, help_text='Phone2',widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"eg 0808 000 0000",}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"id":"password","class":"form-control", "placeholder":"Password",}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class":"form-control", "placeholder":"Repeat Password",}))
    username = forms.CharField(widget=forms.TextInput(attrs={"value":uuid.uuid4().hex[:8].upper()}))




    class Meta:
        model = User
        fields = ['username','first_name','middle_name','last_name','gender','email','phone','phone2','password1','password2',]


class AddFollowerForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, help_text='First Name',widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"First Name","style":"border-left:1px solid; padding-left:6px",}))
    middle_name = forms.CharField(required=False, max_length=100, help_text='Middle Name',widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Middle Name","style":"border-left:1px solid; padding-left:6px",}))
    last_name = forms.CharField(max_length=100, help_text='Last Name',widget=forms.TextInput(attrs={"class":"form-control", "placeholder":"Last Name","style":"border-left:1px solid; padding-left:6px",}))
    CHOICES = (('', 'Gender'),('M', 'Male'),('F', 'Female'))
    gender = forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={"class":"form-select mb-0"}))
    phone = forms.CharField(required=False,max_length=100, help_text='Phone',widget=forms.TextInput(attrs={"id": "add-follower-phone", "class":"form-control", "placeholder":"eg 0808 000 0000","style":"border-left:1px solid; padding-left:6px",}))
    username = forms.CharField(widget=forms.TextInput(attrs={"value":uuid.uuid4().hex[:8].upper()}))
    password1 = forms.CharField(widget=forms.HiddenInput(attrs={"value":"pass4pass4"}))
    password2 = forms.CharField(widget=forms.HiddenInput(attrs={"value":"pass4pass4"}))


    class Meta:
        model = User
        fields = ['username','first_name','middle_name','last_name','gender','phone','password1','password2',]

class CustomLoginForm(AuthenticationForm):

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['username'].widget.attrs.update(
      {'class': 'form-control', }
    )
    self.fields['password'].widget.attrs.update(
      {'class': 'form-control'}
    )


class AddMonthYearForm(forms.Form):
    CHOICES = (('', 'Select Month'),('January', 'January'),('February', 'February'),('March', 'March'),('April', 'April'),('May', 'May'),('June', 'June'),('July', 'July'),('August', 'August'),('September', 'September'),('October', 'October'),('November', 'November'),('December', 'December'))
    month = forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={"class":"form-select mb-0","id":"add-month"}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","id":"add-year","placeholder":"Year"}))
    current = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class":"form-check-input","id":"add-current"}))
    open = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class":"form-check-input","id":"add-open"}))
   
class SubmitReportForm(forms.Form):
    CHOICES = (('', 'Select Month'),('January', 'January'),('February', 'February'),('March', 'March'),('April', 'April'),('May', 'May'),('June', 'June'),('July', 'July'),('August', 'August'),('September', 'September'),('October', 'October'),('November', 'November'),('December', 'December'))
    month = forms.ChoiceField(choices=CHOICES,widget=forms.Select(attrs={"class":"form-select mb-0","id":"add-month"}))
    year = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","id":"add-year","placeholder":"Year"}))
    current = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class":"form-check-input","id":"add-current"}))
    open = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={"class":"form-check-input","id":"add-open"}))
   