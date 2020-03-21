from django.urls import path
from myapp.views import filtering


urlpatterns = [
    path(r'mailfilter/', filtering, name='filtering')
]