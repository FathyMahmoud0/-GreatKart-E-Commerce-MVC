from django import forms
from .models import Accounts



class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
    class Meta:
        
        model = Accounts
        fields = ['first_name','last_name','email','phone','password']
        
        
        def password_not_match(self,*args,**kwargs):
            
            cleaned_data = super(RegistrationForm,self).clean()
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')
            
            if password != confirm_password:
                raise forms.ValidationError("passwords is not match")
            
            
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = ['first_name','last_name','email','phone']
        
# class ChangePasswordForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
#     confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))
#     new_password = forms.CharField(widget=forms.PasswordInput(attrs={'class' : 'form-control'}))

#     class Meta:
#         model = Accounts
#         fields = ['password','new_password','confirm_password']
        
            
            

        
        
            