from django import forms
from . import models

class LoginForm(forms.Form):

    #email = forms.EmailField()
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

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