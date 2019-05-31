from django.urls import path, re_path
from .views import sendMail, sendMailWithAttachment

urlpatterns = [
    #path("send/", polls_list, name="polls_list"),
    re_path(r'^send/$', sendMail, name='sendMail'),
    re_path(r'^send-mail-with-attachment/$', sendMailWithAttachment, name='sendMailWithAttachment'),
    #re_path(r'^send-queued-mail/$', sendMailUsingCelery, name='sendMailUsingCelery'),
    # path("polls/<int:pk>/", polls_detail, name="polls_detail")
]