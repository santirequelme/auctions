from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("createlisting", views.createlisting, name="createlisting"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("alterwatch/<int:id>", views.alterwatch, name="alterwatch"),
    path("comment/<int:id>", views.comment, name="comment"),
    path("close/<int:id>", views.close, name="close"),
    path("categories", views.categories, name="categories")

]
