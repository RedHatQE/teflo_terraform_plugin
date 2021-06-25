# -*- coding: utf-8 -*-
#
# Copyright (C) 2021 Red Hat, Inc.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    tests.test_linchpin_wrapper_plugin
    Unit tests for testing teflo LinchpinWrapperProvisionerPlugin class.
    :copyright: (c) 2021 Red Hat, Inc.
    :license: GPLv3, see LICENSE for more details.
"""

import pytest
import mock
from teflo.resources import Asset
from teflo.utils.config import Config
from teflo.exceptions import TefloProvisionerError
from teflo_terraform_plugin import TerraformProvisionerPlugin

class TestHelper():

    @staticmethod
    def test_get_ip():
        assert 1