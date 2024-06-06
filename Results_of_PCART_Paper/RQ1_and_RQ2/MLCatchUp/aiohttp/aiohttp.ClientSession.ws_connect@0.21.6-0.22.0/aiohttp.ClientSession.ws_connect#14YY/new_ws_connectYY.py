import aiohttp
session = aiohttp.ClientSession()
url = 'ws://example.com/socket'
protocols = ('chat',)
timeout = 10.0
autoclose = False
autoping = True
auth = aiohttp.BasicAuth('username', 'password')
origin = 'http://example.com'
websocket = session.ws_connect(protocols=protocols, url=url, headers=None)