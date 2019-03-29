import warnings

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import SuccessURLAllowedHostsMixin
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    authenticate, login)
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm)
from django.urls import reverse_lazy, reverse
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponseRedirect
from django.shortcuts import resolve_url
from django.utils.encoding import force_text
from django.utils.http import is_safe_url, urlsafe_base64_decode
from django.views.generic import TemplateView, FormView
from django.contrib.auth import (
    REDIRECT_FIELD_NAME, get_user_model, login as auth_login,
    logout as auth_logout, update_session_auth_hash,
)
from sales.forms.register import RegisterForm
from django.template.response import TemplateResponse
from django.utils.translation import ugettext as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.decorators import login_required


class IndexView(TemplateView):
    template_name = 'index.html'


class BlogView(TemplateView):
    template_name = 'blog.html'


class PostView(TemplateView):
    template_name = 'post.html'


class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'


class LoginView(SuccessURLAllowedHostsMixin, FormView):
    """
    Display the login form and handle the login action.
    """
    form_class = AuthenticationForm
    authentication_form = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'login.html'
    redirect_authenticated_user = False
    extra_context = None

    # @method_decorator(sensitive_post_parameters())
    # @method_decorator(csrf_protect)
    # @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if self.redirect_authenticated_user and self.request.user.is_authenticated:
            redirect_to = self.get_success_url()
            if redirect_to == self.request.path:
                raise ValueError(
                    "Redirection loop for authenticated user detected. Check that "
                    "your LOGIN_REDIRECT_URL doesn't point to a login page."
                )
            return HttpResponseRedirect(redirect_to)
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        url_is_safe = is_safe_url(
            url=redirect_to,
            allowed_hosts=self.get_success_url_allowed_hosts(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ''

    def get_form_class(self):
        return self.authentication_form or self.form_class

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        """Security check complete. Log the user in."""
        auth_login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context


class LogoutView(SuccessURLAllowedHostsMixin, TemplateView):
    """
    Log out the user and display the 'You are logged out' message.
    """
    next_page = None
    redirect_field_name = REDIRECT_FIELD_NAME
    template_name = 'logout.html'
    extra_context = None

    def post(self, request, *args, **kwargs):
        """Logout may be done via POST."""
        return self.get(request, *args, **kwargs)

    def get_next_page(self):
        if self.next_page is not None:
            next_page = resolve_url(self.next_page)
        elif settings.LOGOUT_REDIRECT_URL:
            # next_page = resolve_url(settings.LOGOUT_REDIRECT_URL)
            next_page = 'logout'
        else:
            next_page = self.next_page

        if (self.redirect_field_name in self.request.POST or
                self.redirect_field_name in self.request.GET):
            next_page = self.request.POST.get(
                self.redirect_field_name,
                self.request.GET.get(self.redirect_field_name)
            )
            url_is_safe = is_safe_url(
                url=next_page,
                allowed_hosts=self.get_success_url_allowed_hosts(),
                require_https=self.request.is_secure(),
            )
            # Security check -- Ensure the user-originating redirection URL is
            # safe.
            if not url_is_safe:
                next_page = self.request.path
        return next_page


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(self.request, user)
        return super(RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('registerOk')


class RegisterOk(TemplateView):
    template_name = 'registerOk.html'

# # For password reset view:
# @csrf_protect
# def password_reset(request, is_admin_site=False,
#                    template_name='registration/password_reset_form.html',
#                    email_template_name='registration/password_reset_email.html',
#                    subject_template_name='registration/password_reset_subject.txt',
#                    password_reset_form=PasswordResetForm,
#                    token_generator=default_token_generator,
#                    post_reset_redirect=None,
#                    from_email=None,
#                    current_app=None,
#                    extra_context=None,
#                    html_email_template_name=None):
#     if post_reset_redirect is None:
#         post_reset_redirect = reverse('password_reset_done')
#     else:
#         post_reset_redirect = resolve_url(post_reset_redirect)
#     if request.method == "POST":
#         form = password_reset_form(request.POST)
#         if form.is_valid():
#             opts = {
#                 'use_https': request.is_secure(),
#                 'token_generator': token_generator,
#                 'from_email': from_email,
#                 'email_template_name': email_template_name,
#                 'subject_template_name': subject_template_name,
#                 'request': request,
#                 'html_email_template_name': html_email_template_name,
#             }
#             if is_admin_site:
#                 # warnings.warn(
#                 #     "The is_admin_site argument to "
#                 #     "django.contrib.auth.views.password_reset() is deprecated "
#                 #     "and will be removed in Django 1.10.",
#                 #     RemovedInDjango110Warning, 3
#                 # )
#                 opts = dict(opts, domain_override=request.get_host())
#             form.save(**opts)
#             return HttpResponseRedirect(post_reset_redirect)
#     else:
#         form = password_reset_form()
#     context = {
#         'form': form,
#         'title': _('Password reset'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     if current_app is not None:
#         request.current_app = current_app
#
#     return TemplateResponse(request, template_name, context)
#
#
# def password_reset_done(request,
#                         template_name='registration/password_reset_done.html',
#                         current_app=None, extra_context=None):
#     context = {
#         'title': _('Password reset sent'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     if current_app is not None:
#         request.current_app = current_app
#
#     return TemplateResponse(request, template_name, context)
#
#
# # Doesn't need csrf_protect since no-one can guess the URL
#
# @sensitive_post_parameters()
# @never_cache
# def password_reset_confirm(request, uidb64=None, token=None,
#                            template_name='registration/password_reset_confirm.html',
#                            token_generator=default_token_generator,
#                            set_password_form=SetPasswordForm,
#                            post_reset_redirect=None,
#                            current_app=None, extra_context=None):
#     """
#     View that checks the hash in a password reset link and presents a
#     form for entering a new password.
#     """
#     UserModel = get_user_model()
#     assert uidb64 is not None and token is not None  # checked by URLconf
#     if post_reset_redirect is None:
#         post_reset_redirect = reverse('password_reset_complete')
#     else:
#         post_reset_redirect = resolve_url(post_reset_redirect)
#     try:
#         # urlsafe_base64_decode() decodes to bytestring on Python 3
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = UserModel._default_manager.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
#         user = None
#
#     if user is not None and token_generator.check_token(user, token):
#         validlink = True
#         title = _('Enter new password')
#         if request.method == 'POST':
#             form = set_password_form(user, request.POST)
#             if form.is_valid():
#                 form.save()
#                 return HttpResponseRedirect(post_reset_redirect)
#         else:
#             form = set_password_form(user)
#     else:
#         validlink = False
#         form = None
#         title = _('Password reset unsuccessful')
#     context = {
#         'form': form,
#         'title': title,
#         'validlink': validlink,
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     if current_app is not None:
#         request.current_app = current_app
#
#     return TemplateResponse(request, template_name, context)
#
#
#
# def password_reset_complete(request,
#                             template_name='registration/password_reset_complete.html',
#                             current_app=None, extra_context=None):
#     context = {
#         'login_url': resolve_url(settings.LOGIN_URL),
#         'title': _('Password reset complete'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     if current_app is not None:
#         request.current_app = current_app
#
#     return TemplateResponse(request, template_name, context)
#
#
#
# @sensitive_post_parameters()
# @csrf_protect
# @login_required
# def password_change(request,
#                     template_name='registration/password_change_form.html',
#                     post_change_redirect=None,
#                     password_change_form=PasswordChangeForm,
#                     current_app=None, extra_context=None):
#     if post_change_redirect is None:
#         post_change_redirect = reverse('password_change_done')
#     else:
#         post_change_redirect = resolve_url(post_change_redirect)
#     if request.method == "POST":
#         form = password_change_form(user=request.user, data=request.POST)
#         if form.is_valid():
#             form.save()
#             # Updating the password logs out all other sessions for the user
#             # except the current one if
#             # django.contrib.auth.middleware.SessionAuthenticationMiddleware
#             # is enabled.
#             update_session_auth_hash(request, form.user)
#             return HttpResponseRedirect(post_change_redirect)
#     else:
#         form = password_change_form(user=request.user)
#     context = {
#         'form': form,
#         'title': _('Password change'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     if current_app is not None:
#         request.current_app = current_app
#
#     return TemplateResponse(request, template_name, context)
#
#
# @login_required
# def password_change_done(request,
#                          template_name='registration/password_change_done.html',
#                          current_app=None, extra_context=None):
#     context = {
#         'title': _('Password change successful'),
#     }
#     if extra_context is not None:
#         context.update(extra_context)
#
#     if current_app is not None:
#         request.current_app = current_app
#
#     return TemplateResponse(request, template_name, context)
