import tornado.httpclient
request = tornado.httpclient.HTTPRequest(url='http://httpbin.org/get', method='GET', headers={'Content-Type': 'application/json'}, body=None, auth_username=None, auth_password=None, connect_timeout=20, request_timeout=20, if_modified_since=None, follow_redirects=True, max_redirects=5, user_agent='MyUserAgent', use_gzip=True, network_interface=None, streaming_callback=None, header_callback=None, auth_mode=None)