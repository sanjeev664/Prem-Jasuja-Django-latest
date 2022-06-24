from json import JSONDecodeError
import random
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,View
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin

from helpers import checkUser, password_validate
from .forms import PasswordResetForm
from django.urls import reverse, reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.template.response import TemplateResponse
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.forms import PasswordChangeForm
from .utils import username_validation, CommonClass
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.http import (
    url_has_allowed_host_and_scheme, urlsafe_base64_decode,
)
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()


class RegisterAndLoginView(TemplateView):
    """ 
            This class belongs to the registration functionality.
    """
    template_name = 'signup.html'
    subject_template_name = 'signup/email_subject.txt'
    email_template_name = 'signup/activation_email.txt'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('social_manager:index')
        return render(request, self.template_name)

    def post(self, request):
        response = {}
        username = request.POST.get('username')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        page_type = request.POST.get('page_type')
        
        try:
            if page_type == 'sign_up_page':
                is_username_valid = username_validation(username)

                if not is_username_valid.get('valid'):
                    response['status'] = False
                    response['msg'] = is_username_valid.get('message')
                    return JsonResponse(response)

                if password != confirm_password:
                    response['status'] = False
                    response['msg'] = 'Passwords do not match.'
                    return JsonResponse(response)
                
                pass_validate = password_validate(password)
                if pass_validate != True:
                    response['status'] = False
                    response['msg'] = pass_validate
                    return JsonResponse(response)

                user = User(username=username, email=email, dob=dob,
                            phone=phone, fullname=fullname, is_active=False)
                user.set_password(password)
                user.save()
                if user and user.email is not None:
                    # login(request, user)
                    response['status'] = True
                    response['msg'] = 'Link has been sent to your email. Please activate your account.'
                    current_site = get_current_site(request)
                    CommonClass.key_utils(
                        user, self.subject_template_name, self.email_template_name, current_site)
                    response['html'] = render_to_string(
                        'password_reset/done.html')
                if user and user.phone is not None:
                    # login(request, user)
                    response['status'] = True
                    response['msg'] = 'Link has been sent to your phone. Please activate your account.'
                    current_site = get_current_site(request)
                    CommonClass.key_utils_phone(
                        user, self.subject_template_name, self.email_template_name, current_site)
                    response['html'] = render_to_string(
                        'password_reset/done.html')
                else:
                    response['status'] = False
                    response['msg'] = 'Something went wrong. Please try again later.'
            else:

                try:
                    user_data = checkUser(email)
                    user = User.objects.get(**user_data)
                    email =  user.email
                except User.DoesNotExist:
                    response['status'] = False
                    response['msg'] = 'Given credentials are wrong.'

                user = authenticate(email=email, password=password)

                if user:
                    login(request, user)
                    print(user,"*********")
                    response['status'] = True
                    response['msg'] = 'You have been login successfully.'
                    response['html'] = False
                else:
                    response['status'] = False
                    response['msg'] = 'Given credentials are wrong.'
        except Exception as e:
            response['status'] = False
            if 'UNIQUE constraint' in str(e.args):
                if 'accounts_user.email' in str(e.args):
                    response['msg'] = 'Given email is already exists.'
                elif 'accounts_user.username' in str(e.args):
                    response['msg'] = 'Given username is already exists.'
            else:
                response['msg'] = str(e)
        return JsonResponse(response)


class LoginView(TemplateView):

    # This class belongs to the render login HTML page.
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('social_manager:index')
        is_token_valid = True
        return render(request, self.template_name, locals())
    
    # def post(self ,request):
        # phone = request.POST.get('phone', '')
        # password = request.POST.get('password', '')
        # user =  authenticate(username=phone, password=password)
        # user.save()
        
    def post(self ,request):
        response = {}
        # email = request.POST.get('email', '')
        password = request.POST.get('password', '') 
        try:
            user_data = checkUser(email)
            user = User.objects.get(**user_data)
            email =  user.email
        except User.DoesNotExist:
            response['status'] = False
            response['msg'] = 'Given credentials are wrong.'

        user = authenticate(email=email, password=password)

        if user:
            login(request, user)
            print(user,"*****Login****")

            response['status'] = True
            response['msg'] = 'You have been login successfully.'
            response['html'] = False
        else:
            response['status'] = False
            response['msg'] = 'Given credentials are wrong.'
    
    # def post(self ,request):
    #     response = {}
    #     email = request.POST.get('email', '')
    #     password = request.POST.get('password', '')
    #     user = authenticate(username=email, password=password)
    #     if user:
    #         login(request, user)
    #         response['status'] = True
    #         response['msg'] = 'You have been login successfully.'
    #         response['html'] = False
    #         return redirect('social_manager:index')
    #     else:
    #         response['status'] = False
    #         response['msg'] = 'Given credentials are wrong.'
        

class LogoutView(LoginRequiredMixin, TemplateView):
    """ 
            This class belongs to the logout functionality.
    """
    login_url = 'login'
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            return redirect('accounts:login')
        return render(request, self.template_name)
    
    
from django.core.mail import send_mail
from django.conf import settings
from .models import OTP

class ForgotPasswordView(View):
    """ 
            This class belongs to the forgot passsword functionality.
    """
    def get(self, request, *args, **kwargs):
        return render(request, 'forgotpass.html')
    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.POST.get('step') == "step1":
            email = request.POST.get("email")
            if request.POST.get('otpfeild'):
                user = User.objects.get(email = email)
                user_otp = OTP.objects.filter(user=user)
                user_otp=user_otp.last()
                if user_otp.otp == request.POST.get('otpfeild'):
                    response={"status":200,"msg":"Please enter password to reset"}
                    return JsonResponse(response)
                else:
                    response={"status":400,"msg":"Please enter valid otp"}
                    return JsonResponse(response)
            if not User.objects.filter(email=email):
                response = {"msg":"Emai Not exists."}
                return JsonResponse(response)
            else:
                user = User.objects.filter(email=email)
                user = user[0]
            otpsent = OTP.objects.create(
                        user=user,
                        otp = random.randint(10000, 99999),
                        ip = request.META.get('REMOTE_ADDR'),
                        status = 3,
                        counter = 3,
                        )
            s = send_mail(
                subject='OTP to RESET Password',
                message = f"You have request forgot password from ip {otpsent.ip}.\
                    to reset password {otpsent.otp}" ,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email,])
            print(s)
            response= {"status":200,"msg":"otp sent to mail","otp":otpsent.otp}
            return JsonResponse(response)
        
        return render(request, 'forgotpass.html')

# class PasswordResetView(auth_views.PasswordResetView):
#     template_name = 'password_reset/form.html'
#     email_template_name = 'password_reset/email.txt'
#     subject_template_name = 'password_reset/email_subject.txt'
#     form_class = PasswordResetForm
#     success_url = reverse_lazy('accounts:password_reset_done')


# class PasswordResetDoneView(auth_views.PasswordResetDoneView):
#     template_name = 'password_reset/done.html'


# class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
#     template_name = 'password_reset/confirm.html'
#     # after forget password success redirct login!
#     success_url = reverse_lazy('accounts:login')


class ChangePasswordView(LoginRequiredMixin, TemplateView):
    """ 
            This class belongs to the logout functionality.
    """
    login_url = 'login'
    template_name = 'change_password.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return render(request, self.template_name)
        return redirect('accounts:login')

    def post(self, request):
        response = {}
        try:
            user = User.objects.get(email=request.user.email)
        except Exception as e:
            print(e)
            response['status'] = False
            response['msg'] = 'Something went wrong. Please try again later.'
        else:
            if request.POST.get('old_password') and request.POST.get('confirm_password'):
                if user.check_password(request.POST.get('old_password')):
                    if request.POST.get('new_password') != request.POST.get('confirm_password'):
                        response['status'] = False
                        response['msg'] = 'New Password and Confirm Password did not match.'
                    else:
                        user.set_password(request.POST.get('confirm_password'))
                        user.save()
                        update_session_auth_hash(request, user)
                        response['msg'] = 'Successfully changed password.'
                        response['status'] = True
                else:
                    response['status'] = False
                    response['msg'] = 'Old password is incorrect.'
            else:
                response['status'] = False
                response['msg'] = 'Something went wrong. Please try again later.'
        return JsonResponse(response)


# class VerifyTokenValidation(TemplateView):
#     template_name = 'login.html'
#     token_generator = default_token_generator

#     def get(self, request, *args, **kwargs):
#         is_token_valid = False
#         self.user = self.get_user(kwargs['uidb64'])
#         if self.user is not None:
#             token = kwargs['token']
#             if self.token_generator.check_token(self.user, token):
#                 if not self.user.is_active:
#                     self.user.is_active = True
#                     self.user.save()
#                     is_token_valid = True
#                 return render(request, self.template_name, locals())
#         return render(request, self.template_name, locals())

#     def get_user(self, uidb64):
#         try:
#             # urlsafe_base64_decode() decodes to bytestring
#             uid = urlsafe_base64_decode(uidb64).decode()
#             user = User._default_manager.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None
#         return user
    
    
# def post(self ,request):
#         response = {}
#         email = request.POST.get('email', '')
#         password = request.POST.get('password', '')
#         user = authenticate(username=email, password=password)
#         if user:
#             login(request, user)
#             response['status'] = True
#             response['msg'] = 'You have been login successfully.'
#             response['html'] = False
#             return redirect('social_manager:index')
#         else:
#             response['status'] = False
#             response['msg'] = 'Given credentials are wrong.
