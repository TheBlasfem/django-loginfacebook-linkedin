from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     url(r'^user/password/reset/$',
         'registration.views.my_password_reset', name='password_reset'),
         #{'post_reset_redirect': '/user/password/reset/done/'},
         #'django.contrib.auth.views.password_reset',
         #{'post_reset_redirect': '/user/password/reset/done/'},
         #name="password_reset"),
     (r'^user/password/reset/done/$',
      #'registration.views.my_password_reset_done'),
      'django.contrib.auth.views.password_reset_done'),
    (r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/'}),
    (r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete'),
    # Examples:
    # url(r'^$', 'cunuc.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', 'registration.views.index', name='index'),
    url(r'^register_email/','registration.views.register_email', name='register_email'),
    url(r'^register/','registration.views.register', name='register'),
    #url(r'^profile/(?P<code>[.]+)$','registration.views.profile', name='profile'),
    url(r'^profile/','registration.views.profile', name='profile'),
    url(r'^edit_profile/','registration.views.edit_profile', name='edit_profile'),
    url(r'^login_email/','registration.views.login_user_email', name='login_email'),
    url(r'^login/','registration.views.login_user', name='login'),
    url(r'^logout/','registration.views.logout_user', name='logout'),
    url(r'^authfacebook/','registration.views.authfacebook', name='authfacebook'),
    url(r'^authlinkedin/','registration.views.authlinkedin', name='authlinkedin'),

    url(r'^admin/', include(admin.site.urls)),
)
