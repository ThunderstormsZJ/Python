from django.conf.urls import patterns, include, url
from django.contrib import admin
import test_schedule
#import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'zj_Gtask.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    #url(r'^sche_list(?P<id>\d{1,3})/', 'test_schedule.views.sche_list'),
    url(r'^sche_list/$', 'test_schedule.views.sche_list'),
    url(r'^sche_add/$', 'test_schedule.views.sche_add'),
    url(r'^sche_add_oper$', 'test_schedule.views.sche_add_oper'),
    url(r'^sche_delby_id/(?P<id>\d+)$', 'test_schedule.views.sche_delby_id'),
    url(r'^sche_delby_ids$', 'test_schedule.views.sche_delby_ids'),
    url(r'^sche_edit/(?P<id>\d+)$', 'test_schedule.views.sche_edit'),
    #url(r'^static/(?P.*)$','django.views.static.server',{'document_root':settings.STATIC_ROOT},name='static'), 
)
