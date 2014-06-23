# -*- coding: utf-8 -*-


from django.http import HttpRequest, HttpResponse
from django.test import TestCase
try:
    # Django 1.5 check
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

from .middleware import OscarImpersonateMiddleware

# Content from http://www.example.org
CONTENT = b"""<!doctype html>
<html>
<head>
    <title>Example Domain</title>

    <meta charset="utf-8" />
    <meta http-equiv="Content-type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
</head>

<body class="my-body-class">
<div>
    <h1>Example Domain</h1>
    <p>This domain is established to be used for illustrative examples in documents. You may use this
    domain in examples without prior coordination or asking for permission.</p>
    <p><a href="http://www.iana.org/domains/example">More information...</a></p>
</div>
</body>
</html>"""


class OscarImpersonateMiddlewareTestCase(TestCase):

    def setUp(self):
        USERS = (
            # username    is_superuser  is_staff
            ('superuser', True,         True    ),  # noqa
            ('staff',     True,         False   ),  # noqa
            ('user',      False,        False   ),  # noqa
        )

        for username, is_superuser, is_staff in USERS:
            setattr(self, username, User.objects.create(
                username=username, is_superuser=is_superuser, is_staff=is_staff))

        self.request = HttpRequest()
        self.response = HttpResponse(content=CONTENT)
        self.middleware = OscarImpersonateMiddleware()

    def test_empty_response(self):
        processed_response = self.middleware.process_response(request=self.request,
                                                              response=self.response)
        self.assertEqual(processed_response.content, CONTENT)

    def test_non_impersonate_request(self):
        self.request.impersonator = None
        processed_response = self.middleware.process_response(request=self.request,
                                                              response=self.response)
        self.assertEqual(processed_response.content, CONTENT)

    def test_streaming_response(self):
        from django.http import StreamingHttpResponse
        processed_response = self.middleware.process_response(request=self.request,
                                                              response=StreamingHttpResponse())
        self.assertIsInstance(processed_response, StreamingHttpResponse)

    def test_gzip_content_encoding(self):
        self.response['Content-Type'] = 'application/json'
        processed_response = self.middleware.process_response(request=self.request,
                                                              response=self.response)
        self.assertEqual(processed_response.content, CONTENT)
        self.assertEqual(self.response.get('Content-Type'), 'application/json')

    def test_non_html_content_type(self):
        self.response['Content-Encoding'] = 'gzip'
        processed_response = self.middleware.process_response(request=self.request,
                                                              response=self.response)
        self.assertEqual(processed_response.content, CONTENT)
        self.assertEqual(processed_response.get('Content-Encoding'), 'gzip')

    def test_response_content_without_body_open_tag(self):
        content_without_body_open_tag = b'Lorem lipsum'

        self.response.content = content_without_body_open_tag
        processed_response = self.middleware.process_response(request=self.request,
                                                              response=self.response)
        self.assertEqual(processed_response.content, content_without_body_open_tag)

    def test_response_with_impersonation(self):
        self.request.impersonator = self.superuser
        self.request.user = self.user

        processed_response = self.middleware.process_response(request=self.request,
                                                              response=self.response)
        self.assertNotEqual(processed_response.content, CONTENT)
