from django.urls import path
from . import views
app_name = "chat"
urlpatterns = [
    path("", views.index, name="index"),
    path("api/sessions/", views.session_list, name="session_list"),
    path("api/sessions/new/", views.create_session, name="create_session"),
    path("api/sessions/<int:session_id>/", views.session_detail, name="session_detail"),
    path("api/sessions/<int:session_id>/messages/", views.send_message, name="send_message"),
]
