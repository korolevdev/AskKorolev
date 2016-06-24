"""ask_korolev URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app Importport views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from ask_app import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^hot/?', views.hot, name='hot'),
    url(r'^ask/?', views.ask, name='ask'),
    url(r'^base/?', views.base, name="base"),
    url(r'^login/?', views.form_login, name='login'),
    url(r'^logout/?$', views.logout, name = 'logout'),
    url(r'^signup/?', views.form_signup, name='signup'),
    url(r'^(/)?(?P<page>\d+)?$', views.new, name='/'),
    url(r'^params/', views.get_post_params, name="params"),
    url(r'^question/(?P<question_id>[0-9]+)?/?$', views.question, name='question'),
    url(r'^tag/(?P<htag>[a-zA-Z0-9+#.]+)/(?P<page>[0-9]+)?/?$', views.tag, name='tag'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
