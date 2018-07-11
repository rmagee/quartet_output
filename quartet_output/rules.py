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
from django.utils.translation import gettext as _
from quartet_capture import models

def create_default_rule():
    rule = models.Rule()
    rule.name = _('Shipping Output')
    rule.description = _('The default output rule is an example rule set up '
                         'automatically by the system.')
    rule.save()
    return rule

def create_default_steps(rule: Rule):
    '''

    :param rule:
    :return:
    '''
    pass
