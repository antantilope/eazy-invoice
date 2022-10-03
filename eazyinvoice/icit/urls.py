
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


from . import views

urlpatterns = [
    # HTML views
    path('', views.icit_landing, name="icit-landing"),
    path('toggle/', views.toggle_state, name="icit-toggle-state"),

    # API Views
    path(
        'api/record_messages/',
        csrf_exempt(views.record_messages),
        name="icit-api-record-message",
    ),
    path(
        'api/get_target_states/',
        csrf_exempt(views.get_state),
        name="icit-api-get-target-state",
    ),
]
