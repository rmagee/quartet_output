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
from quartet_capture import models
from io import BytesIO
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth, HTTPProxyAuth
from quartet_output.models import EndPoint, EPCISOutputCriteria
from quartet_capture.rules import Step, RuleContext


class HttpTransportMixin:
    '''
    Add to steps that need to support sending http messages.
    '''

    def post_data(self, data: bytes, rule_context: RuleContext,
                  output_criteria: EPCISOutputCriteria,
                  content_type='application/xml',
                  file_exension='xml'):
        '''
        :param data: The data to post.
        :param output_criteria: The output criteria containing the connection
        info.
        :return: The response.
        '''
        data_stream = BytesIO.read(data)
        file_name = '{0}.{1}'.format(rule_context.task_name, file_exension)
        files = {'file': (file_name, data_stream)}
        response = requests.post(
            output_criteria.end_point.urn,
            files,
            auth=self.get_auth(output_criteria),
            headers={'content-type': content_type}
        )
        return response

    def put_data(self, data: bytes, rule_context: RuleContext,
                 output_criteria: EPCISOutputCriteria,
                 content_type='application/xml',
                 file_exension='xml'
                ):
        '''
        :param data: The data to PUT.
        :param output_criteria: The output criteria containing the connection
        info.
        :return: The response.
        '''
        data_stream = BytesIO.read(data)
        file_name = '{0}.{1}'.format(rule_context.task_name, file_exension)
        files = {'file': (file_name, data_stream)}
        response = requests.put(
            output_criteria.end_point.urn,
            files,
            auth=self.get_auth(output_criteria),
            headers={'content-type': content_type}
        )
        return response

    def get_auth(self, output_criteria):
        auth_info = output_criteria.authentication_info
        auth = None
        if auth_info:
            auth_type = auth_info.type or ''
            if 'digest' in auth_type.lower():
                auth = HTTPBasicAuth
            elif 'proxy' in auth_type.lower():
                auth = HTTPProxyAuth
            else:
                auth = HTTPBasicAuth
            auth = auth(auth_info.username, auth_info.password)
        return auth
