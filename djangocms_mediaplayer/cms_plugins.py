from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from django.utils.translation import ugettext_lazy as _

from djangocms_mediaplayer.models import AudioPlayer, VideoPlayer


@plugin_pool.register_plugin
class AudioPlayerPlugin(CMSPluginBase):
    name = _('Audio Player')
    model = AudioPlayer
    render_template = 'djangocms_mediaplayer/audioplayer_plugin.html'


@plugin_pool.register_plugin
class VideoPlayerPlugin(CMSPluginBase):
    name = _('Video Player')
    model = VideoPlayer
    render_template = 'djangocms_mediaplayer/videoplayer_plugin.html'