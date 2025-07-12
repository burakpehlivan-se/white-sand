# travel_recommender/urls.py

from django.contrib import admin
# from django.contrib.auth import views as auth_views # Bu satırı kaldırabilirsiniz
from django.urls import path, include
from django.views.generic import TemplateView # Eğer ana sayfanız TemplateView ile tanımlanıyorsa

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),  # django-allauth URL'lerini ekle
    path('', include('recommender.urls')), # recommender uygulamasının URL'lerini dahil et
    # path('admin/login/', auth_views.LoginView.as_view(template_name='login.html'), name='admin_login') # BU SATIRI KALDIRIN
    # Eğer anasayfanız yoksa ve settings.py'de LOGIN_REDIRECT_URL = '/' ise buraya bir TemplateView eklemeniz gerekebilir.
    # path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]