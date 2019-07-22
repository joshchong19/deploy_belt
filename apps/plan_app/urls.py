from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^$", views.index),
    url(r"^trips/new$", views.new),
    url(r"^trips/(?P<id>\d+)$", views.show),
    url(r"^trips/edit/(?P<id>\d+)$", views.edit),
    url(r"^dashboard$", views.dashboard),

    url(r"^join/(?P<id>\d+)$", views.join),
    url(r"cancel/(?P<id>\d+)$", views.cancel),
    url(r"^delete/(?P<id>\d+)$", views.delete),

    url(r"^process$", views.process),
    url(r"^addtrip$", views.newtrip),
    url(r"^update/(?P<id>\d+)$", views.update),
        
    url(r"^logout$", views.logout),
]