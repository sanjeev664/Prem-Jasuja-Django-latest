from django.urls import path
from . import views
app_name = 'social_manager'
urlpatterns = [
  path("signup/", views.RegisterAndLoginView.as_view(),name='signup'),
  path("login/", views.LoginView.as_view(),name='login'),
  path("logout/", views.LogoutView.as_view(),name='logout'),
  path("forgot-password", views.ForgotPasswordView.as_view(),name='forgot_pass'),
  # path('forgot-password/',views.PasswordResetView.as_view(), name='password_reset'),
  # path('done/',views.PasswordResetDoneView.as_view(), name='password_reset_done'),
  # path('confirm/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(), name='password_reset_confirm',),
  path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
  # path('confirm/registeration/<uidb64>/<token>/',views.VerifyTokenValidation.as_view(), name='confirm_activation_link',),


]
