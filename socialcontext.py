from decouple import config

def socialproviders(request):
    return {
        'google': config('SOCIAL_AUTH_GOOGLE_OAUTH2_KEY') != '' and config('SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET') != '',
        'twitter': config('SOCIAL_AUTH_TWITTER_KEY') != '' and config('SOCIAL_AUTH_TWITTER_SECRET') != ''
    }