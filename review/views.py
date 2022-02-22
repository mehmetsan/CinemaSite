from django.shortcuts import render, HttpResponseRedirect
from .forms import CreateReviewForm, SortForm, UserSearchForm, RatingSortForm
from movie.models import Movie
from .models import Review
from django.contrib.auth.models import User


# Used for creating a review for a movie
# Parameter: movie_id is used for referencing the correct movie
def rate_movie(request, movie_id):
    form = CreateReviewForm(request.POST or None)
    movie = Movie.objects.get(id=movie_id)

    if form.is_valid():
        user = request.user
        review = form.save(commit=False)
        review.user = user
        review.movie = movie
        review.save()
        return render(request, template_name="result.html", context={'message': "Success"})

    return render(request, template_name="review.html", context={'form': form, 'movie': movie})


# Used for displaying a user's reviews page
# Parameter: user_id is used for referencing the correct user
def user_reviews(request, user_id):
    user = User.objects.get(id=user_id)
    reviews = Review.objects.filter(user=user)
    sort_form = SortForm(request.POST or None)

    # Handling the correct sorting for display
    if sort_form.is_valid():
        sort_param = sort_form.cleaned_data.get('sort_param')
        if sort_param == "platform":
            reviews = reviews.order_by("movie__platform")
        elif sort_param == "rating":
            print(reviews)
            reviews = reviews.order_by("-rating")
        elif sort_param == "unseen":
            unseen_movies = []
            for review in reviews:
                if not review.movie.viewer.filter(id=request.user.id).exists():
                    unseen_movies.append(review)
            reviews = unseen_movies
        else:
            reviews = reviews.order_by("id")
    print(reviews)
    return render(request, template_name="user_reviews.html", context={'name': user.first_name,
                                                                       'reviews': reviews,
                                                                       'sort_form': sort_form})


# Used for displaying a user search page
def search_user(request):
    form = UserSearchForm(request.POST or None)

    # If a filled form is sent
    if form.is_valid():
        username = form.cleaned_data.get('username')
        user_id = User.objects.get(username=username).id

        return HttpResponseRedirect("/review/user/{}".format(user_id))
    return render(request, template_name="search_user.html", context={'form': form})


# Used for displaying the reviews made on a movie by all the users
# Parameter: movie_id is used for referencing the correct movie
def movie_reviews(request, movie_id):
    movie = Movie.objects.get(id=movie_id)
    reviews = Review.objects.all().filter(movie__id=movie_id)
    sort_form = RatingSortForm(request.POST or None)

    # If form is filled
    if sort_form.is_valid():
        sort_param = sort_form.cleaned_data.get('sort_param')
        if sort_param == "rating":
            reviews = reviews.order_by("-rating")
        else:
            reviews = reviews.order_by("id")

    return render(request, template_name="movie_reviews.html", context={'movie': movie, 'sort_form': sort_form,
                                                                        'reviews': reviews})
