from django.conf import settings


MEDIAPLAYER_ALLOWED_AUDIO_EXTENSIONS = getattr(settings, 'MEDIAPLAYER_ALLOWED_AUDIO_EXTENSIONS', [
    'mp3', 'ogg', 'wav',
])
MEDIAPLAYER_ALLOWED_VIDEO_EXTENSIONS = getattr(settings, 'MEDIAPLAYER_ALLOWED_VIDEO_EXTENSIONS', [
    'mp4', 'webm', 'ogg'
])
