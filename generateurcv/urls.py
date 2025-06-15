from django.contrib import admin
from django.urls import path, include  # Correction ici
from django.conf import settings
from django.conf.urls.static import static
from generateurcv import views
from django.contrib.auth import views as auth_views
from .views import modelecv_view
from . import views 
from .views import generate_pdf


urlpatterns = [
    path('', views.home, name='index'),  # Assurez-vous que la vue "home" existe
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('historique_cvs/', views.historique_cvs, name='historique_cvs'),
    path('api/cv/<int:cv_id>/', views.get_cv_data, name='get_cv_data'),
    path('update_cv/<int:pk>/', views.update_cv, name='update_cv'),
    path('update_cv/<int:pk>', views.update_cv),  # sans slash

    path('login/', views.auth_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('templates/', views.templates_view, name='templates'),
    path('modelecv/', modelecv_view, name='modelecv'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('about/', views.about_view, name='about'),
    path('partials.nav/', views.partials_nav_view, name='partials.nav'),
    path('logout/', views.logout_view, name='logout'),
    
    path('save_cv/', views.save_cv, name='save_cv'),
    path('<str:cv_name>/', views.cv_view, name='cv_dynamic'),
    
     # Vue pour afficher tous les CV de l'utilisateur
    path('liste/', views.liste_cvs, name='liste_cvs'),
    # Vue pour créer, modifier ou afficher un CV
    path('gestion/<int:cv_id>/', views.gestion_cv, name='gestion_cv'),  # Pour modifier ou voir un CV existant
    path('gestion/', views.gestion_cv, name='creation_cv'),  # Pour créer un nouveau CV
    # Vue pour dupliquer un CV
    path('dupliquer/<int:cv_id>/', views.dupliquer_cv, name='dupliquer_cv'),
    
    path('lettre1/', views.lettre1_View, name='lettre1'),    
    path('lettre2/', views.lettre2_View, name='lettre2'),    
    path('lettre3/', views.lettre3_View, name='lettre3'),    
    path('lettre4/', views.lettre4_View, name='lettre4'),    
    path('lettre5/', views.lettre5_View, name='lettre5'),    
    path('lettre6/', views.lettre6_View, name='lettre6'),    
    path('lettre7/', views.lettre7_View, name='lettre7'),    
    path('lettre8/', views.lettre8_View, name='lettre8'),    


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)