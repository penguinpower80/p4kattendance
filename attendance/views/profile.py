from decouple import config
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from social_django.models import UserSocialAuth


# Adapted mostly from here: https://simpleisbetterthancomplex.com/tutorial/2016/10/24/how-to-add-social-login-to-django.html


@login_required
def profile(request):
    user = request.user
    message = ''

    if request.method == 'POST':

        errors = []
        post_data = request.POST
        if post_data['first_name']:
            user.first_name = post_data['first_name']
        else:
            errors.append('Please provide a first name.')

        if request.POST['last_name']:
            user.last_name = request.POST['last_name']
        else:
            errors.append('Please provide a last name.')

        if request.POST['email']:
            user.email = request.POST['email']
        else:
            errors.append('Please provide an email.')

        if len(errors) == 0:
            user.save()
            message = 'Profile saved.'

    google_configured = config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', default='') != '' and config(
        'SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', default='') != ''

    twitter_configured = config('SOCIAL_AUTH_TWITTER_KEY', default='') != '' and config('SOCIAL_AUTH_TWITTER_SECRET',
                                                                                        default='') != ''

    facebook_configured = config('SOCIAL_AUTH_FACEBOOK_KEY', default='') != '' and config('SOCIAL_AUTH_FACEBOOK_SECRET',
                                                                                          default='') != ''

    try:
        google_login = user.social_auth.get(provider='google-oauth2')
    except UserSocialAuth.DoesNotExist:
        google_login = None

    try:
        linkedin_login = user.social_auth.get(provider='linkedin')
    except UserSocialAuth.DoesNotExist:
        linkedin_login = None

    try:
        twitter_login = user.social_auth.get(provider='twitter')
    except UserSocialAuth.DoesNotExist:
        twitter_login = None

    try:
        facebook_login = user.social_auth.get(provider='facebook')
    except UserSocialAuth.DoesNotExist:
        facebook_login = None

    can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())

    return render(request, 'attendance/profile.html', {
        "user": user,
        'google_login': google_login,
        'linkedin_login': linkedin_login,
        'twitter_login': twitter_login,
        'facebook_login': facebook_login,
        'can_disconnect': can_disconnect,
        'google': google_configured,
        'facebook': facebook_configured,
        'twitter': twitter_configured,
        'message': message,
        'has_social': (google_configured or twitter_configured or facebook_configured)
    })

# @login_required
# def password(request):
#     if request.user.has_usable_password():
#         PasswordForm = PasswordChangeForm
#     else:
#         PasswordForm = AdminPasswordChangeForm
#
#     if request.method == 'POST':
#         form = PasswordForm(request.user, request.POST)
#         if form.is_valid():
#             form.save()
#             update_session_auth_hash(request, form.user)
#             messages.success(request, 'Your password was successfully updated!')
#             send_mail(
#                 'User Account Change',
#                 'Your password has been changed.  If this was not you, please contact support@ltr.com immediately.',
#                 'notifications@lrt.com',
#                 [form.user.email],
#                 fail_silently=False,
#             )
#             return redirect('password')
#         else:
#             messages.error(request, 'Please correct the error below.')
#     else:
#         form = PasswordForm(request.user)
#     return render(request, 'password.html', {'form': form})
