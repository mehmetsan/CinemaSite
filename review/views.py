from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateReviewForm, SortForm, UserSearchForm
from movie.models import Movie
from .models import Review
from django.contrib.auth.models import User


# Create your views here.
def rate_movie(request, movie_id):
    form = CreateReviewForm(request.POST or None)

    if form.is_valid():
        user = request.user
        movie = Movie.objects.get(id=movie_id)
        review = form.save(commit=False)
        review.user = user
        review.movie = movie
        review.save()
        return render(request, template_name="result.html", context={'message': "Success"})

    return render(request, template_name="review.html", context={'form': form})


def user_reviews(request, user_id):
    user = User.objects.get(id=user_id)
    reviews = Review.objects.filter(user=user)
    sort_form = SortForm(request.POST or None)
    if sort_form.is_valid():
        sort_param = sort_form.cleaned_data.get('sort_param')
        if sort_param == "platform":
            reviews = reviews.order_by("movie__platform")
        elif sort_param == "rating":
            reviews = reviews.order_by("rating")

    return render(request, template_name="user_reviews.html", context={'name': user.first_name,
                                                                       'reviews': reviews,
                                                                       'sort_form': sort_form})


def search_user(request):
    form = UserSearchForm(request.POST or None)

    if form.is_valid():
        username = form.cleaned_data.get('username')
        user_id = User.objects.get(username=username).id

        return HttpResponseRedirect("/review/user/{}".format(user_id))
    return render(request, template_name="search_user.html", context={'form': form})