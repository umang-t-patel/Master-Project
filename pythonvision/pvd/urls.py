from django.conf.urls import url
from pvd import views

urlpatterns=[
    url(r'^$',views.index,name='index'),
]
