from django import forms
from . import models

class LoginForm(forms.Form):

    #email = forms.EmailField()
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'password'}))

    """
    views에서 POST 했을때만 clean으로 넘어감
    clean data의 경우 
    def clean_sth 하면 return 값이 sth이어야 하고
    def clean 으로 하면 return 값이 data 여야 함
    """
    
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        try:
            print("user Check")
            user = models.User.objects.get(username=username)
            if user.check_password(password):
                print("password Check")
                return self.cleaned_data
            else:
                self.add_error("password", forms.ValidationError("Password is Wrong"))
        except models.User.DoesNotExist:
            self.add_error("username", forms.ValidationError("User Does Not Exist"))
        return "blabla"

class SignUpForm(forms.ModelForm):
    
    class Meta:
        model = models.User
        fields = ("username", "first_name", "last_name")
        widgets = {
            'first_name' : forms.TextInput(attrs={'placeholder':'First Name'}),
            'username' : forms.TextInput(attrs={'placeholder':'Username'}),
            'last_name' : forms.TextInput(attrs={'placeholder':'Last Name'}),
        }

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}))

    def clean(self):
        username = self.cleaned_data.get("username")
        try:
            models.User.objects.get(username=username)
            raise forms.ValidationError("User already exist", code="existing_user")
            
        except models.User.DoesNotExist:
            pass
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("confirm password is not correct")
        return self.cleaned_data

    def save(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        
        user = super().save(commit=False)
        user.set_password(password)
        user.save()
        print("user created")






class SignUpForm_가내수공업(forms.Form):
    
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        try:
            models.User.objects.get(username=username)
            raise forms.ValidationError("User already exists")
        except models.User.DoesNotExist:
            if password != confirm_password:
                raise forms.ValidationError("confirm password is not correct")
            return self.cleaned_data

    def save(self):
        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        password = self.cleaned_data.get("password")
        
        user = models.User.objects.create_user(username, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
