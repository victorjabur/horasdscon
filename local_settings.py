from settings import util

#GOOGLE_CONSUMER_KEY               = util.getEntry('google_oauth2','GOOGLE_CONSUMER_KEY')
#GOOGLE_CONSUMER_SECRET            = util.getEntry('google_oauth2','GOOGLE_CONSUMER_SECRET')
GOOGLE_OAUTH2_CLIENT_ID           = util.getEntry('google_oauth2','CLIENT_ID')
GOOGLE_OAUTH2_CLIENT_SECRET       = util.getEntry('google_oauth2','CLIENT_SECRET')
SOCIAL_AUTH_CREATE_USERS          = True
SOCIAL_AUTH_FORCE_RANDOM_USERNAME = False
SOCIAL_AUTH_DEFAULT_USERNAME      = 'socialauth_user'
SOCIAL_AUTH_COMPLETE_URL_NAME     = 'socialauth_complete'
LOGIN_ERROR_URL                   = '/login/error/'
#SOCIAL_AUTH_USER_MODEL            = 'app.CustomUser'
SOCIAL_AUTH_ERROR_KEY             = 'socialauth_error'
