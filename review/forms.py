from django import forms
from .models import Review

sort_params = [("platform", "Platform"), ("rating", "Rating")]


class CreateReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']


class SortForm(forms.Form):
    sort_param = forms.ChoiceField(label="Sort by", choices=sort_params)


class UserSearchForm(forms.Form):
    username = forms.CharField(label="username", max_length=120)
