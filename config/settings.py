# Splash
SPLASH_URL = 'http://localhost:8050/render.html?url={}'

# Parser
START_KEYWORDS = ['IT', 'programming', 'AI', 'machine+learning', 'technologies', 'startup', 'investing',
                  'blockchain']

BLACKLIST_DOMAINS = [
    'google.com.ua/setprefs', 'maps.google.com.ua', 'youtube.com', 'mail.google.com',
    'drive.google.com', 'plus.google.com', 'translate.google.com', 'photos.google.com',
    'docs.google.com', 'hangouts.google.com', 'keep.google.com', 'accounts.google.com',
    'support.google.com'
]

# MongoDB
MONGO_DB_NAME = 'parser_db'

MONGO_PORT = 27017

MONGO_HOST = 'localhost'

MONGO_COLLECTION = 'url-parsing'
