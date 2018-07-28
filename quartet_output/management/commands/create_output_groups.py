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
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.db.models import Q


class Command(BaseCommand):
    help = _(
        'Creates the default QU4RTET output group.'
    )

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(
            name='Output Access'
        )
        if created:
            permissions = Permission.objects.filter(
                Q(codename__endswith='_epsisoutputcriteria') and
                Q(codename__endswith='_authenticationinfo') and
                Q(codename__endswith='_endpoint')
            )
            group.permissions.set(
                permissions
            )
            group.save()
