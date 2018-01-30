from django import forms
from . import models


ID_TYPE_CHOICES = (
    ('', 'Id Proof Type'),
    ('Aadhar', 'Aadhar'),
    ('Voter ID', 'Voter ID'),
    ('Driving Licence', 'Driving Licence')
)

GENDER_CHOICES = (
        ('', 'Select Gender'),
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others')
    )


class ExploreForm(forms.Form):
    level = forms.CharField()
    course = forms.CharField()
    city = forms.CharField()


class SelectedForm(forms.Form):
    college = forms.CharField()
    course_name = forms.CharField()
    fee = forms.CharField()
    final_fee = forms.CharField()
    scholarship = forms.CharField()


class Screen4Form(forms.Form):
    name = forms.CharField(label="Name", max_length=120, required=True)
    # id_type = forms.ChoiceField(label="ID Proof Type", choices=ID_TYPE_CHOICES, required=True)
    # id_type_no = forms.CharField(label="Id No.", max_length=80, required=True)
    dob = forms.CharField()
    gender = forms.ChoiceField(label="Gender", choices=GENDER_CHOICES, required=True)
    email = forms.EmailField(max_length=80, required=True)
    parent_email = forms.EmailField(max_length=80, required=True)
    # otp = forms.CharField(max_length=10, required=False)
    # verify_email_otp = forms.CharField(max_length=10, required=False)
    # verify_sms_otp = forms.CharField(max_length=10, required=False)
    address = forms.CharField(widget=forms.Textarea)
    phone = forms.CharField(max_length=80, required=True)
    # house = forms.CharField(max_length=80, required=True)
    # street = forms.CharField(max_length=80, required=True)
    # district = forms.CharField(max_length=80, required=True)
    # city = forms.CharField(max_length=80, required=True)
    # pin = forms.CharField(max_length=64, required=True)
    # state = forms.CharField(max_length=20, required=True)
    # country = forms.CharField(max_length=80, required=True)
    college_name = forms.CharField(max_length=180, required=False)
    college_location = forms.CharField(max_length=180, required=False)
    school = forms.CharField(max_length=180, required=False)
    school_location = forms.CharField(max_length=180, required=False)
    graduation_year = forms.CharField(max_length=10, required=False)
    class_12_year = forms.CharField(max_length=10, required=False)
    tnc = forms.BooleanField()
    # notInCollege = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(Screen4Form, self).__init__(*args, **kwargs)
        try:
            search_id =  self.data.get('search_id')
            search_obj = models.Selection.objects.get(id=search_id).search.level
            if search_obj == "PG":
                self.fields['parent_email'].required = False
        except:
            pass

        # try:
        #     user_obj = models.User.objects.get(username=self.data.get("email"))
        #     profile_obj = models.Profile.objects.get(user=user_obj)
        #     if profile_obj.mobile_verified:
        #         self.fields['verify_sms_otp'].required=False
        #     else:
        #         self.fields['verify_sms_otp'].required=True
        #
        #     if profile_obj.email_verified:
        #         self.fields['verify_email_otp'].required=False
        #     else:
        #         self.fields['verify_email_otp'].required=True
        #
        # except:
        #     pass
        self.fields['name'].widget.attrs.update({'class': 'form-control-1 name', 'placeholder': 'Name'})
        # self.fields['id_type'].widget.attrs.update({'class': 'form-control-1 id_type', 'placeholder': 'Id Type'})
        # self.fields['id_no'].widget.attrs.update({'class': 'form-control-1 id_no', 'placeholder': 'ID No'})
        self.fields['dob'].widget.attrs.update({'class': 'form-control-1 dob', 'placeholder': 'Date of Birth'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control-1 gender', 'placeholder': 'Date of Birth'})
        self.fields['email'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'Email',
                                                  'data-toggle': "popover",
                                                  'data-trigger': "hover",
                                                  'data-content': "This is essential for delivery of documents like voucher.",
                                                  'data-placement': "top" })
        # self.fields['otp'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'OTP Sent to Mobile'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'Mobile Phone',
                                                  'data-toggle': "popover",
                                                  'data-placement': "top",
                                                  'data-trigger': "hover",
                                                  'data-content': "Needed for smooth service delivery"})
        
        # self.fields['verify_email_otp'].widget.attrs.update({'class': 'form-control-1 otp', 'placeholder': 'OTP Sent to Email'})
        # self.fields['verify_sms_otp'].widget.attrs.update({'class': 'form-control-1 otp-mobile', 'placeholder': 'OTP Sent to Mobile'})
        # self.fields['house'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'House'})
        # self.fields['street'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'Street'})
        # self.fields['district'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'District'})
        # self.fields['city'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'City'})
        # self.fields['pin'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'Pincode'})
        # self.fields['state'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'State'})
        # self.fields['country'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'Country'})
        self.fields['address'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'Address'})
        self.fields['college_name'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'College name (graduation)'})
        self.fields['college_location'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'College location'})
        self.fields['graduation_year'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'Graduation year'})
        self.fields['school'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'School Name'})
        self.fields['class_12_year'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'Class 12 Year'})
        self.fields['school_location'].widget.attrs.update({'class': 'form-control-1', 'placeholder': 'School Location'})
        self.fields['parent_email'].widget.attrs.update({'class': 'form-control-1', 'placeholder': "Parent's Email"})
        # self.fields['notInCollege'].widget.attrs.update({'placeholder': "I agree"})
        self.fields['tnc'].widget.attrs.update({'placeholder': "I agree"})


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})


class SignupForm(forms.Form):
    signup_email = forms.EmailField(required=True)
    signup_password = forms.CharField(widget=forms.PasswordInput, required=True)
    signup_confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['signup_email'].widget.attrs.update({'placeholder': "Email (Don't worry we don't spam)"})
        self.fields['signup_password'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['signup_confirm_password'].widget.attrs.update({'placeholder': 'Confirm Password'})

    def clean_signup_confirm_password(self):
        if self.cleaned_data.get('signup_password') and self.cleaned_data.get('signup_password'):
            if self.cleaned_data.get('signup_password') != self.cleaned_data.get('signup_confirm_password'):
                raise forms.ValidationError("The two password fields must match.")
        return self.cleaned_data['signup_confirm_password']


class ForgotPassword(forms.Form):
    email = forms.EmailField()


class ForgotPasswordVerifyOTP(forms.Form):
    otp = forms.CharField()


class ForgotPasswordNewPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    repeat_password = forms.CharField(widget=forms.PasswordInput)


class NewsletterForm(forms.Form):
    email = forms.EmailField()

