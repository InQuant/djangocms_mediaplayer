from cms.models import CMSPlugin
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _
from filer.fields.file import FilerFileField, File

from djangocms_mediaplayer import app_settings


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
    not_supported_text = models.TextField(default=_('Your browser does not support audio playback.'),
                                          verbose_name=_('Not Supported Text'),
                                          help_text=_('Is shown when browser is not supporting audio files'))

    has_slide = models.BooleanField(default=True, verbose_name=_('Allow sliding'))
    has_skip_controls = models.BooleanField(default=False, verbose_name=_('Skip Controls'))

    PRELOAD_CHOICES = (
        ('auto', 'Auto'),
        ('metadata', 'Metadata'),
        ('none', 'None'),
    )
    preload = models.CharField(null=True, blank=True, max_length=255, choices=PRELOAD_CHOICES, default=PRELOAD_CHOICES[0][0])
    is_autoplay = models.BooleanField(default=False, verbose_name=_('Autoplay'))
    is_loop = models.BooleanField(default=False, verbose_name=_('Loop'))
    is_muted = models.BooleanField(default=False, verbose_name=_('Muted'))

    class Meta:
        verbose_name = _('Audio Player')
        verbose_name_plural = _('Audio Player')


class VideoPlayer(CMSPlugin):
    file = FilerFileField(verbose_name=_('Video File'), on_delete=models.CASCADE, validators=[validate_video_file, ])
    not_supported_text = models.TextField(default=_('Your browser does not support video playback.'),
                                        verbose_name=_('Not Supported Text'),
                                        help_text=_('Is shown when browser is not supporting audio files'))