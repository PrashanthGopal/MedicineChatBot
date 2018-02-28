from django.conf.urls import url
from django.contrib import admin
from orders import views as my_order
from django.contrib.auth import views as auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^admin/', admin.site.urls),
	url(r'chat/$', csrf_exempt(my_order.chat_view), name='chat'),
    url(r'^$', my_order.index, name='index'),
    url(r'^orders$', my_order.index, name='home'),
    url(r'^order/alternativeMedicine/(?P<medicine_name>\w+)/$', my_order.show, name='alternativeMedicine'),
    url(r'^order/new/$', my_order.new, name='new'),
    url(r'^users/login/$', auth.login, {'template_name': 'login.html'}, name='login'),
    url(r'^users/logout/$', auth.logout, {'next_page': '/'}, name='logout'),
    url(r'^users/change_password/$', login_required(auth.password_change), {'post_change_redirect' : '/','template_name': 'change_password.html'}, name='change_password'),
]
