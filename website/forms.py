from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record, Quarry, Truck_no, Material

class SignUpForm(UserCreationForm):
	email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
	first_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
	last_name = forms.CharField(label="", max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))


	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(SignUpForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['username'].widget.attrs['placeholder'] = 'User Name'
		self.fields['username'].label = ''
		self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['placeholder'] = 'Password'
		self.fields['password1'].label = ''
		self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

		self.fields['password2'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
		self.fields['password2'].label = ''
		self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'	

# Create Add Record Form
class AddRecordForm(forms.ModelForm):
    date = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "Date", "class": "form-control", "type": "date"}), 
        label=""
    )
    challan_no = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "challan No", "class": "form-control"}), 
        label=""
    )
    quarry = forms.ModelChoiceField(
        queryset=Quarry.objects.all(),
        widget=forms.Select(attrs={"class": "form-control dropdown-toggle"}),
        initial=lambda: Quarry.objects.first() if Quarry.objects.exists() else None,
        label=""
    )
    material = forms.ModelChoiceField(
        queryset=Material.objects.all(),
        widget=forms.Select(attrs={"class": "form-control dropdown-toggle"}),
        initial=lambda: Material.objects.first() if Material.objects.exists() else None,
        label=""
    )
    truck_no = forms.ModelChoiceField(
        queryset=Truck_no.objects.all(),
        widget=forms.Select(attrs={"class": "form-control dropdown-toggle"}),
        initial=lambda: Truck_no.objects.first() if Truck_no.objects.exists() else None,
        label=""
    )
    weight = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "Weight", "class": "form-control"}), 
        label=""
    )
    royalty_pass = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={"placeholder": "Royalty Pass", "class": "form-control"}), 
        label=""
    )
    site = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Site", "class": "form-control"}), 
        label=""
    )
    
    
    # Applying the same styling to the dropdown
    # color = forms.ChoiceField(
    #     choices=COLOR_CHOICES, 
    #     widget=forms.Select(attrs={"class": "form-control"}), 
    #     label=""
    # )

    class Meta:
        model = Record
        exclude = ("user",)
        fields = [
            "date",
            "challan_no",
            "quarry",
            "material",
            "truck_no",
            "weight",
            "royalty_pass",
            "site",
        ]