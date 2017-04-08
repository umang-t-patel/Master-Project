from django.conf.urls import url,include
from django.contrib import admin
from pvd import views

urlpatterns = [
    url(r'^annotations',views.annotations,name='buckets'),
    url(r'^runvision',views.runvision,name='runvision'),
    url(r'^storage',views.uploadstorage,name='uploadstorage'),
    url(r'^uploadimage',views.uploadimage,name='uploadimage'),
    url(r'^$',views.index,name='index'),
    url(r'^admin/', admin.site.urls),
]
