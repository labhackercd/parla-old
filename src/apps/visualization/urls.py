from django.urls import path
from apps.visualization import views

urlpatterns = [
    path('tokens/', views.tokens, name="tokens"),
    path('authors/<str:token>/', views.token_authors, name="token_authors"),
    path('authors/<str:token>/<int:author_id>/',
         views.token_author_manifestations, name="token_authors"),
    path('manifestation/<int:speech_id>/<str:token>/',
         views.manifestation, name="vis_manifestation"),
]
