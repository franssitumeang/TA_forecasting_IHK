from django.conf.urls import url, include

urlpatterns = [
    url(r'^simulatorforecasting', include('Forecasting_IHK.urls')),
]
