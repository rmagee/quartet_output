# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.urls import re_path, include

from quartet_output.urls import urlpatterns as quartet_output_urls

urlpatterns = [
    re_path(r"^", include(quartet_output_urls)),
]
