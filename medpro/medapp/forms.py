from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import PharmacyUser,Feedback,Payment,Medicine,Booking

class PharmacySignupForm(UserCreationForm):
    pharmacy_name = forms.CharField(max_length=255)
    address = forms.CharField(widget=forms.Textarea)
    contact_number = forms.CharField(max_length=15)

    class Meta:
        model = PharmacyUser
        fields = ['username', 'email', 'pharmacy_name', 'address', 'contact_number', 'password1', 'password2']

def save(self, commit=True):
    user = super().save(commit=False)
    user.pharmacy_name = self.cleaned_data['pharmacy_name']
    user.address = self.cleaned_data['address']
    user.contact_number = self.cleaned_data['contact_number']
    if commit:
        user.save()
    return user

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['name', 'email','message']



class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['name', 'card_number', 'expiry_date', 'cvv', 'amount']
        widgets = {
            'card_number': forms.PasswordInput(),
            'cvv': forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['readonly'] = True



class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['name', 'type', 'dosage', 'expiry_date', 'description','price','image']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['quantity']