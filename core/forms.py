from django import forms
from image_uploader_widget.widgets import ImageUploaderWidget
from users.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column


class ProductForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=None)
    x = forms.FloatField(widget=forms.HiddenInput(), required=False)
    y = forms.FloatField(widget=forms.HiddenInput(), required=False)
    width = forms.FloatField(widget=forms.HiddenInput(), required=False)
    height = forms.FloatField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Only allow producer users to select themselves when adding their products
        if self.user.is_superuser == False:
            self.fields['user'].queryset = User.objects.filter(pk=self.user.pk)
        else:
            self.fields['user'].queryset = User.objects.all()

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
    role = forms.CharField(
        required=True, widget=forms.Select(choices=User.TYPES))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())
    phone = forms.CharField(max_length=14, required=True)
    street = forms.CharField(required=True)
    suburb = forms.CharField(required=True)
    city = forms.CharField(
        required=True, widget=forms.Select(choices=User.CITIES))
    province = forms.CharField(
        required=True, widget=forms.Select(choices=User.PROVINCES))
    house_number = forms.IntegerField(required=True)
    lat = forms.DecimalField(max_digits=30, decimal_places=20, required=True)
    lng = forms.DecimalField(max_digits=30, decimal_places=20, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()

        self.helper.layout = Layout(
            Row(
                Column('role', css_class='form-group col-12 mb-0'),
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                Column('email', css_class='form-group col-md-6 mb-0'),
                Column('password', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
                Column('street', css_class='form-group col-md-6 mb-0'),
                Column('suburb', css_class='form-group col-md-6 mb-0'),
                Column('city', css_class='form-group col-md-6 mb-0'),
                Column('province', css_class='form-group col-md-6 mb-0'),
                Column('house_number', css_class='form-group col-md-6 mb-0'),
                Column('lat', css_class='form-group col-md-6 mb-0'),
                Column('lng', css_class='form-group col-md-6 mb-0')
            ),
            Submit('submit', 'Register', css_class='w-100')
        )


class AcceptDealForm(forms.Form):
    confirm = forms.BooleanField(required=True)


class WithdrawalForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    innbucks_qrcode = forms.ImageField()


class SignoutForm(forms.Form):
    signout = forms.IntegerField()


class PlaceOrderForm(forms.Form):
    quantity = forms.IntegerField(min_value=50, required=True)
    description = forms.CharField(widget=forms.Textarea())
