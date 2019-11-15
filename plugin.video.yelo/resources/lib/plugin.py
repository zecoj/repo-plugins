import routing
from resources.lib.helpers import UAHelper
from resources.lib.enums.enums import protocols

routing = routing.Plugin()
UAHelper.set_UA()

from resources.lib.kodiwrapper import kodiwrapper
from resources.lib.yelo import yelo

kodi_wrapper = kodiwrapper.KodiWrapper(globals())
yelo_player = yelo.YeloPlay(kodi_wrapper, protocols.DASH)


@routing.route('/')
def main_menu():
    if yelo_player.login():
        yelo_player.display_main_menu()


@routing.route('/listing/livestreams')
def list_channels():
    data = yelo_player.fetch_channel_list()
    if data:
        yelo_player.list_channels(data)


@routing.route('/info/<channel_name>/<logo>/<channel>/<channelId>')
def channel_info(channel_name, logo, channel, channelId):
    import base64

    if channel_name and logo and channel:
        yelo_player.show_info_stream(
            base64.b64decode(channel_name),
            base64.b64decode(logo), channel, channelId)


@routing.route('/livestream/<channel>')
def play_livestream(channel):
    stream_url = yelo_player.select_manifest_url(channel)
    if stream_url:
        yelo_player.play_live_stream(stream_url)


def run(params):
    routing.run(params)
