from cms.models import CMSPlugin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.file import FilerFileField, File
from filer.fields.image import FilerImageField

from . import app_settings


def check_ext(ext, valid_ext: list):
    if not ext.lower() in valid_ext:
        raise ValidationError("%s  (%s)" % (_('Unsupported file extension.'), ", ".join(valid_ext)))


def validate_audio_file(value):
    file = File.objects.get(pk=value)   # type: File
    check_ext(file.extension, app_settings.MEDIAPLAYER_ALLOWED_AUDIO_EXTENSIONS)


def validate_video_file(value):
    file = File.objects.get(pk=value)   # type: File
    check_ext(file.extension, app_settings.MEDIAPLAYER_ALLOWED_VIDEO_EXTENSIONS)


class AudioPlayer(CMSPlugin):
    file = FilerFileField(verbose_name=_('Audio File'), on_delete=models.CASCADE, validators=[validate_audio_file, ])
    not_supported_text = models.TextField(_('Not Supported Text'), default=_('Your browser does not support audio playback.'),
                                          help_text=_('Is shown when browser is not supporting audio files'))

    show_slide = models.BooleanField(_('Allow sliding'), default=True)
    show_skip_controls = models.BooleanField(_('Skip Controls'), default=False)

    PRELOAD_CHOICES = (
        ('auto', 'Auto'),
        ('metadata', 'Metadata'),
        ('none', 'None'),
    )
    preload = models.CharField(null=True, blank=True, max_length=255, choices=PRELOAD_CHOICES, default=PRELOAD_CHOICES[0][0])
    is_autoplay = models.BooleanField(_('Autoplay'), default=False)
    is_loop = models.BooleanField(_('Loop'), default=False)
    is_muted = models.BooleanField(_('Muted'), default=False)

    class Meta:
        verbose_name = _('Audio Player')


class VideoPlayer(CMSPlugin):
    file = FilerFileField(verbose_name=_('Video File'), on_delete=models.CASCADE, validators=[validate_video_file, ])
    not_supported_text = models.TextField(_('Not Supported Text'),
                                          default=_('Your browser does not support video playback.'),
                                          help_text=_('Is shown when browser is not supporting video files'))

    show_controls = models.BooleanField(_('Controls'), default=True)

    show_slide = models.BooleanField(_('Allow sliding'), default=True)
    show_skip_controls = models.BooleanField(_('Skip Controls'), default=False)

    is_autoplay = models.BooleanField(_('Autoplay'), default=False)
    is_loop = models.BooleanField(_('Loop'), default=False)
    is_muted = models.BooleanField(_('Muted'), default=False)
    PRELOAD_CHOICES = (
        ('auto', 'Auto'),
        ('metadata', 'Metadata'),
        ('none', 'None'),
    )
    preload = models.CharField(null=True, blank=True, max_length=255, choices=PRELOAD_CHOICES,
                               default=PRELOAD_CHOICES[0][0])

    poster = FilerImageField(verbose_name=_('Thumbnail'), on_delete=models.SET_NULL, null=True, blank=True,
                             related_name='video_poster')

    class Meta:
        verbose_name = _('Video Player')
