Change Log
----------

1.3.2
~~~~~
- Fix - unicode key

1.3.1
~~~~~
- Get rid of brackets in decorator
- Bugfix: valid signature for resticted view passed validation

1.3.0
~~~~~
- Merge validation of multiple and single signature to single method
- Replace middleware classes to one single class HmacMiddleware

1.2.0
~~~~~
- Decorators

1.0.5
~~~~~
- Fix: Django HTTP headers

1.0.4
~~~~~
- Fix: use base64.b64encode instead of base64.urlsafe_b64encode

1.0.2
~~~~~
- Fix: HMAC_SECRET should be optional
- `GlobalHmacMiddleware` and `MultipleHmacMiddleware`

0.0.1
~~~~~
- Initial release including the core feature set
