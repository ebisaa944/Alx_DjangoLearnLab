from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User

# ... existing imports and forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

class UserProfileForm(UserChangeForm):
    password = None  # Do not allow password change from this form

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
