from django.conf.urls import patterns, include, url
from Interface.views import HomePageView, LocalAnalysisView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^local/', LocalAnalysisView.as_view(), name='local'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
