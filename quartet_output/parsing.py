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

from EPCPyYes.core.v1_2 import events as yes_events
from quartet_output.evaluation import EventEvaluation
from quartet_output.models import EPCISOutputCriteria
from quartet_epcis.parsing.steps import QuartetParser


class OutputCriteriaParser(QuartetParser):
    '''
    Inherits from the `QuartetParser` in `quartet_epcis.parsing.parser`.
    This parser can use an `EPCISOutputDetermination` model instance
    to determine if any inbound messages can be used to create
    and queue up outbound messages.
    '''

    def __init__(self, stream, epc_output_criteria: EPCISOutputCriteria,
                 event_cache_size: int = 1024):
        super().__init__(stream, event_cache_size)
        self.epc_output_criteria = epc_output_criteria
        self.event_evaluation = EventEvaluation()

    def handle_aggregation_event(
        self,
        epcis_event: yes_events.AggregationEvent
    ):
        '''
        Handles any aggregation events as they are found, inserts them into
        the database and then inspects them for output determination.
        :param epcis_event: The event to insert and inspect.
        :return: None
        '''
        super().handle_aggregation_event(epcis_event)
        self.evaluate(epcis_event)

    def handle_transaction_event(
        self,
        epcis_event: yes_events.TransactionEvent
    ):
        '''
        Handles any transaction events as they are found, inserts them into
        the database and then inspects them for output determination.
        :param epcis_event: The event to insert and inspect.
        :return: None
        '''
        super().handle_transaction_event(epcis_event)
        self.evaluate(epcis_event)

    def handle_object_event(self, epcis_event: yes_events.ObjectEvent):
        '''
        Handles any object events as they are found, inserts them into
        the database and then inspects them for output determination.
        :param epcis_event: The event to insert and inspect.
        :return: None
        '''
        super().handle_object_event(epcis_event)
        self.evaluate(epcis_event)

    def handle_transformation_event(
        self,
        epcis_event: yes_events.TransformationEvent
    ):
        '''
        Handles any transformation events as they are found, inserts them into
        the database and then inspects them for output determination.
        :param epcis_event: The event to insert and inspect.
        :return: None
        :param epcis_event:
        :return: None
        '''
        super().handle_transformation_event(epcis_event)
        self.evaluate(epcis_event)

    def evaluate(self, epcis_event):
        if self.event_evaluation.evaluate_event(
            epcis_event,
            self.epc_output_criteria
        ):
            self.queue_task()

    def queue_task(self):
        print('queue task called.')
