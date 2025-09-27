from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Petition, Signature
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    search_term = request.GET.get('search')
    if search_term:
        movies = Movie.objects.filter(name__icontains=search_term)
    else:
        movies = Movie.objects.all()

    template_data = {}
    template_data['title'] = 'Movies'
    template_data['movies'] = movies
    return render(request, 'movies/index.html', {'template_data': template_data})

def show(request, id):
    movie = Movie.objects.get(id=id)
    reviews = Review.objects.filter(movie=movie)

    template_data = {}
    template_data['title'] = movie.name
    template_data['movie'] = movie
    template_data['reviews'] = reviews
    return render(request, 'movies/show.html', {'template_data': template_data})

@login_required
def create_review(request, id):
    if request.method == 'POST' and request.POST['comment'] != '':
        movie = Movie.objects.get(id=id)
        review = Review()
        review.comment = request.POST['comment']
        review.movie = movie
        review.user = request.user
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def edit_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user != review.user:
        return redirect('movies.show', id=id)
    if request.method == 'GET':
        template_data = {}
        template_data['title'] = 'Edit Review'
        template_data['review'] = review
        return render(request, 'movies/edit_review.html', {'template_data': template_data})
    elif request.method == 'POST' and request.POST['comment'] != '':
        review = Review.objects.get(id=review_id)
        review.comment = request.POST['comment']
        review.save()
        return redirect('movies.show', id=id)
    else:
        return redirect('movies.show', id=id)

@login_required
def delete_review(request, id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    review.delete()
    return redirect('movies.show', id=id)

@login_required
def petitions(request):
    if request.method == 'POST':
        petition = Petition()
        petition.name = request.POST['name']
        petition.likes = 0
        petition.save()
        return redirect('movies.petitions')

    petitions = Petition.objects.all()

    template_data = {}
    template_data['title'] = 'Petitions'
    template_data['petitions'] = petitions

    return render(request, 'movies/petitions.html', {'template_data': template_data})

@login_required
def view_petition(request, id):
    if request.method == 'POST':
        petition = Petition.objects.get(id=id)
        petition.likes = petition.likes + 1
        petition.save()
        signature = Signature()
        signature.petition = petition
        signature.signer = request.user
        signature.save()
        return redirect('movies.view_petition', id=id)

    petition = Petition.objects.get(id=id)
    hasSignature = False
    signatures = Signature.objects.filter(petition=petition)
    signatures = signatures.filter(signer=request.user)
    if len(signatures) > 0:
        hasSignature = True

    template_data = {}
    template_data['title'] = 'Petitions'
    template_data['petition'] = petition
    template_data['hasSignature'] = hasSignature

    return render(request, 'movies/view_petition.html', {'template_data': template_data})
