
import re

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_text

HTML_CONTENT_TYPES = ('text/html', 'application/xhtml+xml')


class OscarImpersonateMiddleWare:

    def process_response(self, request, response):
        """
        Replace ``<body>`` open tag with partial/toolbar.html template.
        (*highly* inspired from Django Debug Toolbar's middleware)
        """

        if request.impersonator is None:
            """
            No impersonification session, return response
            """
            return response

        content_encoding = response.get('Content-Encoding', '')
        content_type = response.get('Content-Type', '').split(';')[0]
        if any((getattr(response, 'streaming', False),
                'gzip' in content_encoding,
                content_type not in HTML_CONTENT_TYPES)):
            """
            Either the response is streaming, or it's gzipped, or it's not even HTML
            """
            return response

        html = force_text(response.content, encoding=settings.DEFAULT_CHARSET)

        body_open_tag_pattern = '<body[^>]*>'
        matches = re.findall(body_open_tag_pattern, html)

        if not len(matches) > 0:
            """
            ``<body>`` open tag is not found.
            """
            return response

        body_open_tag = matches[0]
        bits = re.split(body_open_tag_pattern, html, flags=re.IGNORECASE)

        if len(bits) > 1:
            context = {'impersonator': request.impersonator, 'user': request.user}
            toolbar = render_to_string('oscar_impersonate/partials/toolbar.html', context)

            bits[-1] = body_open_tag + toolbar + bits[-1]
            response.content = ''.join(bits)

        if response.get('Content-Length', None):
            response['Content-Length'] = len(response.content)
        return response
