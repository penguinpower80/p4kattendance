from decouple import config

def socialproviders(request):
    return {
        'google': config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY', default='') != '' and config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET', default='') != '',
        'twitter': config('SOCIAL_AUTH_TWITTER_KEY', default='') != '' and config('SOCIAL_AUTH_TWITTER_SECRET', default='') != '',
        'facebook': config('SOCIAL_AUTH_FACEBOOK_KEY', default='') != '' and config('SOCIAL_AUTH_FACEBOOK_SECRET', default='') != '',
        'message': request.GET.get('message',''),
        'backend': request.GET.get('backend', '')
    }