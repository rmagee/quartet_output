# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2018 SerialLab Corp.  All rights reserved.
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
django.setup()
from rest_framework.test import APITestCase
from django.urls import reverse
from quartet_output import models

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
django.setup()


class ViewTest(APITestCase):

    def test_endpoint(self):
        self._create_endpoint()
        url = reverse('end-points-list')
        # #data = self._get_test_data()
        response = self.client.get(url)
        self.assertIs(response.status_code, 200)

    def _create_endpoint(self):
        ep = models.EndPoint()
        ep.urn = 'http://testhost'
        ep.name = 'Test EndPoint'
        ep.save()
        return ep

    def _get_test_data(self):
        '''
        Loads the XML file and passes its data back as a string.
        '''
        curpath = os.path.dirname(__file__)
        data_path = os.path.join(curpath, 'data/epcis.xml')
        with open(data_path) as data_file:
            return data_file.read()
