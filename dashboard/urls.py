from django.urls import path
from . import views

urlpatterns = [
	path('', views.home, name = 'home'),
	path('<int:limit>', views.home, name = 'limiter'),
	path('accepted/<str:id>/<int:limit>', views.accepted, name = 'accepted'),
	path('rejected/<str:id>/<int:limit>', views.rejected, name = 'rejected'),
]
