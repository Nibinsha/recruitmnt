"""recruitment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', UserLogin.as_view(), name="login"),
    path('client_list/', ClientList.as_view(), name="client_view"),
    path('about/', login_required(TemplateView.as_view(template_name="secret.html"))),
  #  path('client_save/', clientSave.as_view(), name="client_save"),


    path('candidate_list/', CandidateList.as_view(), name="candidate_list"),
    path('candidate/add', CandidateAdd.as_view(), name="candidate_add"),
    path('candidate/<int:candidate_id>/edit', CandidateEditView.as_view(), name="candidate_edit"),
    path('candidate/<int:candidate_id>/delete', CandidateDeleteView.as_view(), name="candidate_delete"),
    
    path('home/', Home.as_view(), name="home"),
    # path('candidate_save/', CandidateSave.as_view(), name="candidate_save"),

    #nibinsha
    path('subuser_list/', SubuserList.as_view(), name="subuser_list"),
    path('subuser_save/', SubuserSave.as_view(), name="subuser_save"),
    # path('subuser/<int:subuser_id>/edit', SubuserEditView.as_view(), name="subuser_edit"),
    path('subuser/<int:subuser_id>/delete', SubuserDelete.as_view(), name="subuser_delete"),

    path('logout/', LogoutView.as_view(), name="logout"),

    path('company_list/', CompanyList.as_view(), name="company_list"),
    path('company/add', CompanyAdd.as_view(), name="company_add"),
    path('company/<int:company_id>/edit', CompanyEditView.as_view(), name="company_edit"),
    path('company/<int:company_id>/delete', CompanyDelete.as_view(), name="company_delete"),

    path('mailing/', MailingView.as_view(), name="mailing"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
