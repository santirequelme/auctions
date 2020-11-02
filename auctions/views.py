from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from .models import User, Listing, Comment, Bid, Watchlist
from django.contrib.auth.decorators import login_required
from .forms import listing_form
from django.utils import timezone
from django.views.decorators.http import require_http_methods


def index(request):
    listings = Listing.objects.all()
    if listings is None:
        return render(request, "auctions/index.html",{
        "active":False
    })
    return render(request, "auctions/index.html",{
        "active":listings
    })
    

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/')
def createlisting(request):
    if request.method == "POST":
        form = listing_form(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.listing_date = timezone.now()
            listing.max_bid = listing.initial_bid
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        return HttpResponseRedirect(reverse('createlisting'))
    else:
        form = listing_form()
        return render (request, "auctions/createlisting.html",
         {'form':form})

@login_required(login_url='/')
def listing(request, id):
    listing = Listing.objects.get(id=id)
    userwatching = Watchlist.objects.filter(user=request.user).values('listing_id')

    watchlist = []
    for content in userwatching:
        watchlist.append(content['listing_id'])
    if id in watchlist:
        boolean = True
    else:
        boolean = False
    comments = Comment.objects.filter(listing=listing).values('id')
    comment_list = []
    for content in comments:
        comment = Comment.objects.get(id=content['id'])
        comment_list.append(comment)
    

    if request.method == "POST":
        bid = request.POST.get("newbid")
        newbid = Bid(listing = listing, user = request.user, bid = bid)
        newbid.save()
        listing.max_bid = bid
        listing.save()
        
    if listing.status:
        return render(request, "auctions/listing.html",{
            "listing":listing,
            "user":request.user,
            "watchlist":boolean,
            "comments":comment_list
        })
    else:
        count = Bid.objects.filter(listing = listing).count()
        if count==0:
            winner = None
        else:
            price = Bid.objects.filter(listing = listing).aggregate(Max('bid'))
            price = price.get('bid__max')
            user = Bid.objects.filter(listing = listing, bid=price).first()
            winner = user.user
        
        return render(request, "auctions/listing.html",{
            "listing":listing,
            "user":request.user,
            "watchlist":boolean,
            "comments":comment_list,
            "winner":winner
        })

@login_required(login_url='/')
def watchlist(request):
    user = request.user
    listings =Watchlist.objects.filter(user=user).values('listing_id')
    watchlist= []
    for listing in listings:
            watch = Listing.objects.get(id = listing['listing_id'])
            watchlist.append(watch)
    if watchlist is None:
        return render(request, "auctions/watchlist.html", {
            "watchlist":False
        })
    return render(request, "auctions/watchlist.html",{
        "watchlist": watchlist
    })

@login_required(login_url='/')
def alterwatch(request,id):
    user = request.user
    listing = Listing.objects.get(id=id)
    if Watchlist.objects.filter(user=user,listing=listing).exists():
        watch = Watchlist.objects.get(user=user,listing=listing)
        watch.delete()
        return HttpResponseRedirect(reverse("listing", args=(),
            kwargs={'id': id}))
    else:
        watch = Watchlist(user=user, listing=listing)
        watch.save()
        return HttpResponseRedirect(reverse("listing", args=(),
            kwargs={'id': id}))

@login_required(login_url='/')
def comment(request, id):
    user= request.user
    listing= Listing.objects.get(id =id)
    if request.method == "POST":
        comment = request.POST.get("comment")
        new_comment= Comment (user = user, listing =listing, comment=comment)
        new_comment.save()

    return HttpResponseRedirect(reverse("listing", args=(), kwargs={'id':id}))

@login_required(login_url='/')
def close(request,id):
    listing = Listing.objects.get(id=id)
    listing.status = False
    listing.save()
    return HttpResponseRedirect(reverse("listing", args=(), kwargs={'id':id}))

@login_required(login_url='/')
def categories(request):
    if request.method == "GET":
        return render(request, "auctions/categories.html")
    else:
        category = request.POST["category"]
        listings = Listing.objects.filter(category = category)
        if len(listings) > 0:
            boolean = True
        else:
            boolean = False
        return render(request, "auctions/categories.html", {
            "active":listings,
            "boolean" : boolean
            })

        
