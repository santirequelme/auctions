from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    categories = [
        ('No Category',' No Category'),
        ('Home','Home'),
        ('Toys','Toys'),
        ('Tech','Tech'),
        ('Sport','Sport'),
        ]
    owner        = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title        = models.CharField(max_length= 70)
    category     = models.CharField(choices=categories, blank=True, max_length= 64, default='No Category')
    description  = models.CharField(max_length = 1000)
    image_url    = models.URLField(blank=True)
    initial_bid  = models.IntegerField(default=0)
    listing_date = models.DateTimeField(auto_now_add=True)
    status       = models.BooleanField(default=True)
    max_bid      = models.IntegerField()


    def __str__(self):
        return f"{self.title}"

class Comment (models.Model):
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_owner")
    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment_listing") 
    comment    = models.CharField(max_length=1800)


    def __str__(self):
        return f"{self.user} on {self.listing} say {self.comment}"

class Bid(models.Model):
    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item")
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid        = models.DecimalField(max_digits=7, decimal_places=2)


class Watchlist (models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="own_watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist_item")

    def __str__(self):
        return f"{self.user} {self.listing}"


    
    
    
    