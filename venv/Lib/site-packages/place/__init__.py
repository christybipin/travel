"""
Place python library
------------------------

Documentation: https://developer.placepay.com

:copyright: (c) 2017 Place (http://placepay.com)
:license: MIT License
"""

from .__about__ import __version__

PROD_URL = 'https://api.placepay.com'
TEST_URL = 'https://test-api.placepay.com'

api_key = None
api_url = PROD_URL

from place.client import Client
default_client = Client()

from place.exceptions import *
from place.resources import *
