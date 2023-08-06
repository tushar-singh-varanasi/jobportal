"""
URL configuration for jobportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from App import views
from django.conf import settings
from django.conf.urls.static import static 
from django.contrib.auth import views as auth_views 
from App.forms import MypasswordresetForm,MySetpassword


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('Signup-Candidate/',views.Signupform_cand,name='signup_candidate'),
    path('otp-candidate/',views.OTPFunction_can,name='otp_candidate'),
    path('signuphr/',views.Signupform_HR,name='signuphr'),
    path('otphr/',views.OTPFunction_HR,name='otphr'),
    path('job-post/',views.job_post,name='jop_posting'),
    path('login-hr/',views.loginfunctionHR,name='login'),
    path('logout/',views.logout_view,name='logout'),
    path('profile-hr/',views.Profile,name='profile'),
    path('job-post-update/<int:pk>/',views.JOB_Post_update.as_view(),name='job-post-update'),
    path("job-edit/",views.Job_edit, name="job_edit"),
    path("login-Candidate/",views.loginfunction_Candidate, name="login_Candidate"),
    path("Profile-Candidate/",views.Profile_candidate, name="profile_candidate"),
    path("candidate-personal-details/",views.Candidate_detail, name="Candidate_detail"),
    path("apply/<int:id>",views.Applyfunction, name="apply"),
    path("candidate-personal-details-update/",views.Candidate_detail_update, name="candidate_personal_details_update"),
    path("delete/<int:id>/",views.Job_delete, name="Job_delete"),
    path("job-filter/<str:data>/",views.Job_filter, name="job_filter_data"),
    path("candidate-apply-list/<int:id>/",views.Apply_details_fun, name="candidate_apply"),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='auth/password_reset.html',form_class=MypasswordresetForm),name='password_reset'),
    path('password-reset-done/',auth_views.PasswordResetDoneView.as_view(template_name='auth/password_reset_done.html'),name='password_reset_done'),
    path("password-reset-confirm/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name='auth/password_reset_confirm.html',form_class=MySetpassword),name='password_reset_confirm'),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view(template_name='auth/password_reset_complete.html'), name="password_reset_complete"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
 