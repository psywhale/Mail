from django.conf.urls import url
from .views import IndexView,ReplyView, \
    LabelView, ListUnreadView, ArchiveMailView, MarkMailUnreadView,\
    ComposeView

urlpatterns= [
    url(r'^$',IndexView.as_view(), name='IndexView'),
    url(r'^reply/(?P<id>[0-9]+)/$', ReplyView.as_view(), name='reply'),
    url(r'^label/(?P<sn>[0-9Cc]{5}\-[0-9]{3}[sS]+)/$', LabelView.as_view(), name='label'),
    url(r'^listunread/$', ListUnreadView.as_view(), name='listunread'),
    url(r'^audit/$', ListUnreadView.as_view(), name='listunread'),
    url(r'^archive/$', ArchiveMailView.as_view(), name='archivemail'),
    url(r'^munread/$', MarkMailUnreadView.as_view(), name='markunread'),
    url(r'^compose/$', ComposeView.as_view(), name='compose'),
]