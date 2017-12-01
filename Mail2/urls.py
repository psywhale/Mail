from django.conf.urls import url
from .views import IndexView,ReplyView

urlpatterns= [
    url(r'^$',IndexView.as_view(), name='IndexView'),
    url(r'^reply/(?P<id>[0-9]+)/$', ReplyView.as_view(), name='reply')

]