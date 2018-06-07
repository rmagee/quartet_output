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
import io
from django.core.files.base import File
from quartet_output.models import EPCISOutputCriteria
from quartet_output.parsing import OutputCriteriaParser
from quartet_capture import models
from quartet_epcis.parsing.steps import EPCISParsingStep


class OutputParsingStep(EPCISParsingStep):
    '''
    A Step that can invokes the `quartet_output.EPCISOutputCriteria`
    parser.  This parser looks for matches between the Step's configured
    *EPCIS Output Criteria* model and any inbound EPCIS events to determine
    if subsequent outbound rule processing is necessary.
    '''

    def __init__(self, db_task: models.Task, **kwargs):
        super().__init__(db_task, **kwargs)
        self.declared_parameters['EPCIS Output Criteria'] = (
            'The name value of an EPCIS Output Criteria configuration.'
        )
        self.epc_output_criteria = self.get_output_criteria()

    def get_output_criteria(self):
        output_criteria = self.get_parameter('EPCIS Output Criteria',
                                             raise_exception=True)
        try:
            return EPCISOutputCriteria.objects.get(
                name=output_criteria
            )
        except EPCISOutputCriteria.DoesNotExist:
            exc = EPCISOutputCriteria.DoesNotExist(
                'EPCISOutputCriteria with name %s could not be found in the '
                'database.' % output_criteria
            )
            raise exc

    def execute(self, data, rule_context: dict):
        '''
        Calls the OutputCriteriaParser which looks for any matches
        between the output criteria and any inbound events.
        :param data: The data to parse.
        :param rule_context: Any context supplied by the Rule.
        :return: None
        '''
        try:
            if isinstance(data, File):
                parser = OutputCriteriaParser(data,
                                              self.epc_output_criteria)
            else:
                parser = OutputCriteriaParser(io.BytesIO(data),
                                              self.epc_output_criteria)
        except TypeError:
            parser = OutputCriteriaParser(io.BytesIO(data.encode()),
                                          self.epc_output_criteria)
        parser.parse()
