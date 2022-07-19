"""
$description localhost webcams
$url localhost.com
$type live
"""

import re

from requests import Response

from streamlink.plugin import Plugin, pluginmatcher
from streamlink.stream.hls import HLSStream, HLSStreamWorker, HLSStreamReader

class MyHLSStreamWorker(HLSStreamWorker):
    def _fetch_playlist(self) -> Response:
        print('fetching m3u8 url', self.stream.url)
        return super()._fetch_playlist()

class MyHLSStreamReader(HLSStreamReader):
    __worker__ = MyHLSStreamWorker

class MyHLSStream(HLSStream):
    __reader__ = MyHLSStreamReader

@pluginmatcher(re.compile(
    "http://localhost:3000/"
))
class LocalHost(Plugin):
    def _get_streams(self):
      return MyHLSStream.parse_variant_playlist(self.session, "http://localhost:3000/playlist")
      body = self.session.http.get(self.url).text
      mrl = None
      match = re.search(r"""<source src="(.*)" type="application\/x-mpegURL">""", body)
      if match:
        mrl = match.group(1)
      if mrl:
        return MyHLSStream.parse_variant_playlist(self.session, mrl)


    # def _get_streams(self):
    #     re_streams = re.compile(r"""<source src="(?P<url>.*)" type="application\/x-mpegURL">""")
    #     # re_streams = re.compile(r"""https://\w+\.streamlock\.net\/live\/.+playlist.m3u8[a-zA-Z0-9_?&+=]+""")
    #     res = self.session.http.get(self.url, schema=validate.Schema(
    #         validate.transform(re_streams.findall)
    #     ))
    #     for _, stream_url in res:
    #         return HLSStream.parse_variant_playlist(self.session, stream_url)


__plugin__ = LocalHost
