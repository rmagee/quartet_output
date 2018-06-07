#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_quartet_output
------------

Tests for `quartet_output` models module.
"""
import os
from django.core.exceptions import ValidationError
from EPCPyYes.core.v1_2.events import EventType, Source, Destination
from EPCPyYes.core.v1_2.CBV.dispositions import Disposition
from EPCPyYes.core.v1_2.CBV.business_steps import BusinessSteps
from quartet_capture.models import Rule, Step, StepParameter, Task
from quartet_capture import rules
from quartet_capture.tasks import execute_rule
from quartet_output.steps import OutputCriteriaParser
from quartet_output.models import EPCISOutputCriteria
from django.test import TestCase

from quartet_output import models


class TestQuartet_output(TestCase):

    def setUp(self):
        pass

    def test_evaluation(self):
        oc = self._create_output_criterion()
        self._parse_data(oc)

    def test_bad_source(self):
        oc = self._create_output_criterion()
        oc.source_id = None
        with self.assertRaises(ValidationError):
            oc.clean()

    def test_bad_destination(self):
        oc = self._create_output_criterion()
        oc.destination_id = None
        with self.assertRaises(ValidationError):
            oc.clean()

    def test_full_rule(self):
        self._create_output_criterion()
        db_rule = self._create_rule()
        self._create_step(db_rule)
        db_task = self._create_task(db_rule)
        curpath = os.path.dirname(__file__)
        data_path = os.path.join(curpath, 'data/epcis.xml')
        with open(data_path, 'r') as data_file:
            execute_rule(data_file.read().encode(), db_task)

    def test_full_bad_rule(self):
        oec = self._create_output_criterion()
        oec.name = "Bad Name"
        oec.save()
        db_rule = self._create_rule()
        self._create_step(db_rule)
        db_task = self._create_task(db_rule)
        curpath = os.path.dirname(__file__)
        data_path = os.path.join(curpath, 'data/epcis.xml')
        with open(data_path, 'r') as data_file:
            try:
                execute_rule(data_file.read().encode(), db_task)
            except EPCISOutputCriteria.DoesNotExist:
                pass

    def _create_output_criterion(self):
        eoc = EPCISOutputCriteria()
        eoc.name = "Test Criteria"
        eoc.action = "ADD"
        eoc.event_type = EventType.Transaction.value
        eoc.disposition = Disposition.in_transit.value
        eoc.biz_step = BusinessSteps.shipping.value
        eoc.biz_location = 'urn:epc:id:sgln:305555.123456.0'
        eoc.read_point = 'urn:epc:id:sgln:305555.123456.12'
        eoc.source_type = 'urn:epcglobal:cbv:sdt:location'
        eoc.source_id = 'urn:epc:id:sgln:305555.123456.12'
        eoc.destination_type = 'urn:epcglobal:cbv:sdt:location'
        eoc.destination_id = 'urn:epc:id:sgln:309999.111111.233'
        eoc.save()
        return eoc

    def _parse_data(self, output_criteria):
        curpath = os.path.dirname(__file__)
        parser = OutputCriteriaParser(
            os.path.join(curpath, 'data/epcis.xml'),
            epc_output_criteria=output_criteria
        )
        parser.parse()
        parser.clear_cache()

    def _create_rule(self):
        rule = Rule()
        rule.name = 'output-test'
        rule.description = 'output test rule'
        rule.save()
        return rule

    def _create_step(self, rule):
        step = Step()
        step.rule = rule
        step.order = 1
        step.step_class = 'quartet_output.steps.OutputParsingStep'
        step.description = 'unit test step'
        step.save()
        step_parameter = StepParameter()
        step_parameter.step = step
        step_parameter.name = 'EPCIS Output Criteria'
        step_parameter.value = 'Test Criteria'
        step_parameter.save()

    def _create_task(self, rule):
        task = Task()
        task.rule = rule
        task.name = 'unit test task'
        task.save()
        return task

    def tearDown(self):
        pass
