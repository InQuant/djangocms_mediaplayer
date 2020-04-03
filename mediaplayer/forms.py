from cmsplus.fields import PlusModelChoiceField
from cmsplus.forms import PlusPluginBaseForm
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import ManyToOneRel
from django.utils.translation import ugettext_lazy as _
from filer.fields.file import AdminFileWidget, FilerFileField
from filer.fields.file import File
from filer.models.filemodels import File as FilerFileModel
from django.contrib.admin.sites import site as admin_site


from . import app_settings


def check_ext(ext, valid_ext: list):
    if not ext.lower() in valid_ext:
        raise ValidationError("%s  (%s)" % (_('Unsupported file extension.'), ", ".join(valid_ext)))


def get_file(value):
    if isinstance(value, int):
        return File.objects.get(pk=value)   # type: File
    elif isinstance(value, File):
        return value
    else:
        raise AttributeError("value needs to be either int (pk of file) or file itself")


def validate_audio_file(value):
    file = get_file(value)
    check_ext(file.extension, app_settings.MEDIAPLAYER_ALLOWED_AUDIO_EXTENSIONS)


def validate_video_file(value):
    file = get_file(value)
    check_ext(file.extension, app_settings.MEDIAPLAYER_ALLOWED_VIDEO_EXTENSIONS)


class BasePlayerForm(PlusPluginBaseForm):
    not_supported_text = forms.CharField(widget=forms.Textarea, label=_('Not supported text'), initial=_('Not supported'),
                                         help_text=_('Text if player is not supportet by browser'), required=False)
    show_slide = forms.BooleanField(label=_('Allow sliding'), initial=True, required=False)
    show_skip_controls = forms.BooleanField(label=_('Skip Controls'), initial=False, required=False)
    show_controls = forms.BooleanField(label=_('Controls'), initial=True, required=False)
    PRELOAD_CHOICES = (
        ('auto', 'Auto'),
        ('metadata', 'Metadata'),
        ('none', 'None'),
    )
    preload = forms.CharField(widget=forms.Select(choices=PRELOAD_CHOICES),
                              initial=PRELOAD_CHOICES[0][0], required=False)
    is_autoplay = forms.BooleanField(label=_('Autoplay'), initial=False, required=False)
    is_loop = forms.BooleanField(label=_('Loop'), initial=False, required=False)
    is_muted = forms.BooleanField(label=_('Muted'), initial=False, required=False)


class AudioPlayerForm(BasePlayerForm):
    file = PlusModelChoiceField(label=_("Audio File"),
                                queryset=FilerFileModel.objects.all(),
                                widget=AdminFileWidget(ManyToOneRel(FilerFileField, FilerFileModel, 'id'), admin_site),
                                required=True,
                                validators=[validate_audio_file],
                                help_text=_("Audio file for the player"),)


class VideoPlayerForm(BasePlayerForm):
    file = PlusModelChoiceField(label=_("Video File"),
                                queryset=FilerFileModel.objects.all(),
                                widget=AdminFileWidget(ManyToOneRel(FilerFileField, FilerFileModel, 'id'), admin_site),
                                required=True,
                                validators=[validate_video_file],
                                help_text=_("Video file for the player"))

    poster = PlusModelChoiceField(label=_("Video Thumbnail"),
                                  queryset=FilerFileModel.objects.all(),
                                  widget=AdminFileWidget(ManyToOneRel(FilerFileField, FilerFileModel, 'id'), admin_site),
                                  required=False,
                                  help_text=_("Thumbnail on stopped video file "), )