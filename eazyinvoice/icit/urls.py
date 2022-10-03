
from django.urls import path
from . import views

urlpatterns = [
    # HTML views
    path('', views.icit_landing, name="icit-landing"),
    path('toggle/', views.toggle_state, name="icit-toggle-state"),
]
