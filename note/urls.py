from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_page, name='logout'),
    path('showdairy/', views.showdairy, name='show'),
    path('descriptivedairy/', views.descriptivedairy, name='descriptive'),
    path('adddairy/', views.adddairy, name='add'),
    path('delete/<int:id>', views.deletedairy, name = 'delete'),
    path('edit/<int:id>', views.editdairy, name = 'edit'),
    path('updateddairy/<int:id>', views.updateddairy, name = 'updated'),
    path('view/<int:id>', views.viewingpage, name = 'view'),
    path('photodiary/', views.photodiary, name='photodiary'),
    path('upload/', views.upload, name='upload'),
    path('gallery/', views.showphotos, name='gallery'),
    path('updatephoto/<str:title>', views.updatephotos, name='updatephotodiary'),
    path('deletephoto/<int:id>', views.deletephotos, name='deletephotos'),
    path('verify-otp/', views.checkMail, name = 'checkmail'),
    path('otpreq/', views.otpViewPage, name = 'otpreq'),
    path('passcheck/', views.passCheck, name='passcheck')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)