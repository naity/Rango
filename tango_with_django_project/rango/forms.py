from django import forms
from django.contrib.auth.models import User
from rango.models import Category, Page, UserProfile

class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128, 
                help_text="Please enter the catetory name: ")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ["name", "views", "likes"]

class PageForm(forms.ModelForm):
    category = forms.ModelChoiceField(widget=forms.HiddenInput(),
                                                                queryset=Category.objects.all())
    title = forms.CharField(max_length=128,
                help_text="Please enter the page title: ")
    url = forms.URLField(help_text="Please enter page URL: ")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    
    class Meta:
        model = Page
        fields = ["category", "title", "url", "views"]

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get("url")

        if url and not url.startswith("http://"):
            url = "http://" + url
            cleaned_data["url"] = url

        return cleaned_data

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ["username", "password", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs['class'] = "form_field"
        self.fields['password'].widget.attrs['class'] = "form_field"
        self.fields['email'].widget.attrs['class'] = "form_field"
        self.fields["first_name"].widget.attrs['class'] = "form_field"
        self.fields["last_name"].widget.attrs['class'] = "form_field"

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["website", "picture"]

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs) 
        self.fields['website'].widget.attrs['class'] = "form_field"