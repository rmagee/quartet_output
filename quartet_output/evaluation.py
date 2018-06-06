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

from EPCPyYes.core.v1_2 import events
from quartet_output.models import EPCISOutputCriteria


class EventEvaluation:

    def evaluate_event(self, event: events.EPCISEvent,
                       epc_output_criteria: EPCISOutputCriteria
                       ):
        '''
        Returns a true or false if the event meets the output criteria.
        :param event: An EPCPyYes event to evaluate.
        :param epc_output_criteria: The criteria to evaluate the event against.
        :return: boolean - True or false.
        '''
        # check the event type
        event_type = self.check_event_type(
            event,
            epc_output_criteria.event_type
        )
        action = self.check_action(
            event, epc_output_criteria.action
        )
        biz_location = self.check_biz_location(
            event,
            epc_output_criteria.biz_location
        )
        disposition = self.__check_string(
            event.disposition,
            epc_output_criteria.disposition
        )

        return (event_type and action and biz_location and disposition)

    def check_event_type(self, event: events.EPCISEvent, event_type: str):
        '''
        Checks the event against the expected event type.
        :param event: The event to check
        :param event_type: The expected type
        :return: True or false
        '''
        ret = False if event_type else True
        if event_type:
            if event_type == events.EventType.Transaction.value:
                ret = isinstance(event, events.TransactionEvent)
            elif event_type == events.EventType.Object.value:
                ret = isinstance(event, events.ObjectEvent)
            elif event_type == events.EventType.Aggregation.value:
                ret = isinstance(event, events.AggregationEvent)
            elif event_type == events.EventType.Transformation.value:
                ret = isinstance(event, events.TransformationEvent)
        return ret

    def check_biz_location(self, event, biz_location: str):
        '''
        Checks the event biz_location against the expected one.
        :param event: The event to check
        :param biz_location: The expected biz_location
        :return: True or False
        '''
        ret = False if biz_location else True
        if biz_location:
            ret = (biz_location == event.biz_location)
        return ret

    def check_action(self, event, action: str):
        '''
        Evaluates the event action vs. the expected action
        :param event: The event to evaluate
        :param action: The expected action
        :return: True or False (bool)
        '''
        ret = False if action else True
        if action:
            try:
                ret = (event.action == action)
            except AttributeError:
                # transformation events will not have an action
                # there is only one attribute call in that code
                # so this handler is safe
                pass
        return ret

    def __check_string(self, event_val, criteria_val):
        '''
        Checks an event value against the expected value. If the criterial
        val was not specified will return True since it's not for
        consideration.
        :param event_val: The event value.
        :param criteria_val: The expected value.
        :return: True or False
        '''
        ret = False if criteria_val else True
        if criteria_val:
            ret = (event_val == criteria_val)
        return ret
