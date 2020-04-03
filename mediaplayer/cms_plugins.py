from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from cmsplus.plugin_base import PlusPluginBase
from django.utils.translation import ugettext_lazy as _

from .forms import AudioPlayerForm, VideoPlayerForm


@plugin_pool.register_plugin
class VideoPlayerPlugin(PlusPluginBase):
    name = _('Video Player')
    form = VideoPlayerForm
    render_template = 'djangocms_mediaplayer/videoplayer_plugin.html'


@plugin_pool.register_plugin
class AudioPlayerPlugin(PlusPluginBase):
    name = _('Audio Player')
    form = AudioPlayerForm
    render_template = 'djangocms_mediaplayer/audioplayer_plugin.html'
