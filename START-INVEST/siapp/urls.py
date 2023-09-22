from django.urls import path
from django.conf.urls.static import static
# from django.conf.urls.media import media
from django.conf import settings
from siapp import views
 
urlpatterns = [
    path('',views.home,name='home'),
    path('invlogin/',views.invlogin,name='invlogin'),
    path('entlogin/',views.entlogin,name='entlogin'),
    path('investor_reg/',views.inreg,name='inreg'),
    path('entrepreneur_reg/',views.entreg,name='entreg'),
    path('current_campaigns/',views.curcamp,name='curr_campaign'),
    path('portfolio/',views.portfolio,name='portfolio'),
    path('aboutus/',views.aboutus,name='aboutus'),
    path('entrep_investors/',views.enttable,name='enttable'),
    path('entrep_profile/',views.entprofile,name='entprofile'),
    path('payment/',views.payment,name='payment'),
    path('transfer/',views.transfer,name='transfer'),
    path('invlogout/',views.invlogout,name='invlogout'),
    path('entlogout/',views.entlogout,name='entlogout'),
    path('success/',views.success,name='success'),

]

urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)