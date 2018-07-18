# Splash
SPLASH_URL = 'http://localhost:8050/render.html?url={}'

# Parser
START_KEYWORDS = [
    'IT', 'programming', 'AI', 'machine+learning', 'technologies', 'startup', 'investing',
    'blockchain', 'products+entrepreneurship', 'products', 'design', 'team+making'
    'self+driving+cars', 'robots', 'space', 'tesla', 'electro', 'enery', 'making+desicions',
    'motivation', 'mars+exploration', 'data+science', 'big+data',
]

BLACKLIST_DOMAINS = [
    'google.com.ua/setprefs', 'maps.google.com', 'youtube.com', 'mail.google.com',
    'drive.google.com', 'plus.google.com', 'translate.google.com', 'photos.google.com',
    'docs.google.com', 'hangouts.google.com', 'keep.google.com', 'accounts.google.com',
    'support.google.com', 'webcache.googleusercontent.com', 'api', 'store.google.com',
    'books.google.com',
]

# MongoDB
MONGO_DB_NAME = 'parser_db'

MONGO_PORT = 27017

MONGO_HOST = 'localhost'

MONGO_COLLECTION = 'url-parsing'
