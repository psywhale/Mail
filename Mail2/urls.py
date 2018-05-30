from django.conf.urls import url
from .views import IndexView,ReplyView, \
    LabelView, ListUnreadView, ArchiveMailView, MarkMailUnreadView,\
    ComposeView, OutboxView, OutboxReplyView,AuditView,AuditViewClass,\
    AuditViewUser, Launch, FileUpload, DownloadView, GetEmailListView

urlpatterns= [
    url(r'^$',IndexView.as_view(), name='IndexView'),
    url(r'^reply/(?P<id>[0-9]+)/$', ReplyView.as_view(), name='reply'),
    url(r'^reply/(?P<id>[0-9]+)/(?P<userid>[0-9]+)/$', ReplyView.as_view(), name='reply'),
    url(r'^label/(?P<sn>[0-9Cc]{5}\-[0-9]{3}[sS]+)/$', LabelView.as_view(), name='label'),
    url(r'^listunread/$', ListUnreadView.as_view(), name='listunread'),
    url(r'^audit/$', AuditView.as_view(), name='audit'),
    url(r'^audit/class$', AuditViewClass.as_view(), name='auditclass'),
    url(r'^audit/class/(?P<termcode>[0-9]{2}[1-3][sS]+)/$', AuditViewClass.as_view(), name='auditclass'),
    url(r'^audit/user$', AuditViewUser.as_view(), name='audituser'),
    url(r'^archive/$', ArchiveMailView.as_view(), name='archivemail'),
    url(r'^munread/$', MarkMailUnreadView.as_view(), name='markunread'),
    url(r'^compose/(?P<sn>[0-9Cc]{5}\-[0-9]{3}[sS]+)/$', ComposeView.as_view(), name='compose'),
    url(r'^download/(?P<pk>[0-9]+)/$', DownloadView.as_view(), name='download'),
    url(r'^upload/', FileUpload.as_view(), name='upload'),
    #TODO: Remove later
    url(r'^compose/$', ComposeView.as_view(), name='compose'),
    url(r'^outbox/$', OutboxView.as_view(), name='outbox'),
    url(r'^or/(?P<id>[0-9]+)/(?P<userid>[0-9]+)/$', OutboxReplyView.as_view(), name='outboxreply'),
    url(r'^or/(?P<id>[0-9]+)/$', OutboxReplyView.as_view(), name='outboxreply'),
    url(r'^launch/', Launch.as_view(), name='launch'),
    url(r'^listEmail/$', GetEmailListView.as_view(), name='listEmail'),
    url(r'^listEmail/(?P<sn>[0-9Cc]{5}\-[0-9]{3}[sS]+)/$', GetEmailListView.as_view(), name='listEmail'),


]