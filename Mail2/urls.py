from django.conf.urls import url
from .views import IndexView,ReplyView, LabelView, ListUnreadView

urlpatterns= [
    url(r'^$',IndexView.as_view(), name='IndexView'),
    url(r'^reply/(?P<id>[0-9]+)/$', ReplyView.as_view(), name='reply'),
    url(r'^label/(?P<sn>[0-9Cc]{5}\-[0-9]{3}s+)/$', LabelView.as_view(), name='label'),
    url(r'^listunread/$', ListUnreadView.as_view(), name='listunread'),
]