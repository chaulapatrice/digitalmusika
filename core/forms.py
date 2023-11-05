from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget
from users.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
        }
        fields = '__all__'


class ProductRequestForm(forms.ModelForm):
    class Meta:
        widgets = {
            'image': ImageUploaderWidget(),
        }
        fields = '__all__'

class AdminWithdrawalForm(forms.ModelForm):
    class Meta:
        widgets = {
            'innbucks_qrcode': ImageUploaderWidget(),
        }
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True)

class CheckIfUserExistsForm(forms.Form):
    email = forms.EmailField(required=True)

class SignupForm(forms.Form):
    role = forms.CharField(required=True, widget=forms.Select(choices=User.TYPES))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    phone = forms.CharField(max_length=14, required=True)
    street = forms.CharField(required=True)
    suburb = forms.CharField(required=True)
    city = forms.CharField(required=True, widget=forms.Select(choices=User.CITIES))
    province = forms.CharField(required=True, widget=forms.Select(choices=User.PROVINCES))
    house_number = forms.IntegerField(required=True)


class AcceptDealForm(forms.Form):
    confirm= forms.BooleanField(required=True)

class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    innbucks_qrcode = forms.ImageField()

class SignoutForm(forms.Form):
    signout = forms.IntegerField()

class DealFilterForm(forms.Form):
    task = forms.CharField(required=False, 
                            widget=forms.TextInput(
                                attrs={'placeholder': 'Eg. Tengesa Huku'}))
    
    # minimum_value = forms.IntegerField(required=False, 
    #                                     widget=forms.TextInput(
    #                                         attrs={'placeholder': '$'}))
    
    # maximum_value = forms.IntegerField(required=False, 
    #                                    widget=forms.TextInput(
    #                                        attrs={'placeholder': '$'}))

class AddDealBidForm(forms.Form):
    offer_description = forms.CharField(required=True, widget=forms.Textarea())




