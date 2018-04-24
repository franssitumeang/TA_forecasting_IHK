from django.conf.urls import url
from .controllers import index

urlpatterns = [
    url(r'^$', index.index),
    url(r'^/plot_original_data', index.plot_original_data),
    url(r'^/plot_decomposition_data', index.plot_decomposition_ts),
    url(r'^/plot_stationary_data', index.plot_stationarity_ts),
    url(r'^/plot_acf_pacf_data', index.plot_acf_pacf_ts),
    url(r'^/modeling', index.modeling),
    url(r'^/test_1', index.test_1),
]