http://httpbin.org/

A simple HTTP Request & Response Service. 

| Endpoint                                 | Description                              |
| ---------------------------------------- | ---------------------------------------- |
| [/](http://httpbin.org/)                 | This page.                               |
| [/ip](http://httpbin.org/ip)             | Returns Origin IP.                       |
| [/user-agent](http://httpbin.org/user-agent) | Returns user-agent.                      |
| [/headers](http://httpbin.org/headers)   | Returns header dict.                     |
| [/get](http://httpbin.org/get)           | Returns GET data.                        |
| /post                                    | Returns POST data.                       |
| /patch                                   | Returns PATCH data.                      |
| /put                                     | Returns PUT data.                        |
| /delete                                  | Returns DELETE data                      |
| [/gzip](http://httpbin.org/gzip)         | Returns gzip-encoded data.               |
| [/deflate](http://httpbin.org/deflate)   | Returns deflate-encoded data.            |
| [/status/:code](http://httpbin.org/status/418) | Returns given HTTP Status code.          |
| [/response-headers](http://httpbin.org/response-headers?Content-Type=text/plain;%20charset=UTF-8&Server=httpbin) | Returns given response headers.          |
| [/redirect/:n](http://httpbin.org/redirect/6) | 302 Redirects *n* times.                 |
| [/redirect-to?url=foo](http://httpbin.org/redirect-to?url=http://example.com/) | 302 Redirects to the *foo* URL.          |
| [/relative-redirect/:n](http://httpbin.org/relative-redirect/6) | 302 Relative redirects *n* times.        |
| [/cookies](http://httpbin.org/cookies)   | Returns cookie data.                     |
| [/cookies/set?name=value](http://httpbin.org/cookies/set?k1=v1&k2=v2) | Sets one or more simple cookies.         |
| [/cookies/delete?name](http://httpbin.org/cookies/delete?k1&k2) | Deletes one or more simple cookies.      |
| [/basic-auth/:user/:passwd](http://httpbin.org/basic-auth/user/passwd) | Challenges HTTPBasic Auth.               |
| [/hidden-basic-auth/:user/:passwd](http://httpbin.org/hidden-basic-auth/user/passwd) | 404'd BasicAuth.                         |
| [/digest-auth/:qop/:user/:passwd](http://httpbin.org/digest-auth/auth/user/passwd) | Challenges HTTP Digest Auth.             |
| [/stream/:n](http://httpbin.org/stream/20) | Streams *n* – 100 lines.                 |
| [/delay/:n](http://httpbin.org/delay/3)  | Delays responding for *n* – 10 seconds.  |
| [/drip](http://httpbin.org/drip?numbytes=5&duration=5&code=200) | Drips data over a duration after an optional initial delay, then (optionally) returns with the given status code. |
| [/range/:n](http://httpbin.org/range/1024) | Streams *n* bytes, and allows specifying a *Range* header to select a subset of the data. Accepts a *chunk_size* and request *duration* parameter. |
| [/html](http://httpbin.org/html)         | Renders an HTML Page.                    |
| [/robots.txt](http://httpbin.org/robots.txt) | Returns some robots.txt rules.           |
| [/deny](http://httpbin.org/deny)         | Denied by robots.txt file.               |
| [/cache](http://httpbin.org/cache)       | Returns 200 unless an If-Modified-Since or If-None-Match header is provided, when it returns a 304. |
| [/cache/:n](http://httpbin.org/cache/60) | Sets a Cache-Control header for *n* seconds. |
| [/bytes/:n](http://httpbin.org/bytes/1024) | Generates *n* random bytes of binary data, accepts optional *seed* integer parameter. |
| [/stream-bytes/:n](http://httpbin.org/stream-bytes/1024) | Streams *n* random bytes of binary data, accepts optional *seed*and *chunk_size* integer parameters. |
| [/links/:n](http://httpbin.org/links/10) | Returns page containing *n* HTML links.  |
| [/forms/post](http://httpbin.org/forms/post) | HTML form that submits to */post*        |
| [/xml](http://httpbin.org/xml)           | Returns some XML                         |
| [/encoding/utf8](http://httpbin.org/encoding/utf8) | Returns page containing UTF-8 data.      |