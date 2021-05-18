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

    Actual code for the plugin should go here. What the plugin does etc.

    :copyright: (c) 2021 Red Hat, Inc.
    :license: GPLv3, see LICENSE for more details.
"""


import os
from teflo.core import ProvisionerPlugin
from teflo.exceptions import TefloProvisionerError
from teflo.helpers import schema_validator

from .terraform_helper import TerraformHelper


class TerraformProvisionerPlugin(ProvisionerPlugin):
    __plugin_name__ = 'teflo_terraform_plugin'

    __schema_file_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                            "files/schema.yml"))
    __schema_ext_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                       "files/schema_extensions.py"))
    _ip = ""

    def __init__(self, asset):

        super(TerraformProvisionerPlugin, self).__init__(asset)
        self._terraform_workspace_default = self.workspace + \
            "/" + "teflo_terraform_workspace"
        self._terraform_resource_definition = self.asset.terraform_resource_definition
        self._terraform_workspace = self.workspace + "/" + \
            self._terraform_resource_definition.get("workspace_path", None) if self._terraform_resource_definition.get(
                "workspace_path", None) is not None else None
        self._ip_output_name = self._terraform_resource_definition.get("ip_output_name", "ip_output_name")

        self.create_logger(name=self.__plugin_name__, data_folder=self.config.get('DATA_FOLDER'))  # OR use teflo logger
        self._terraform_engine = TerraformHelper()

    def _path_provided(self):
        return self._terraform_workspace is not None

    def _path_valid(self, path):
        return os.path.isdir(path)

    def create(self):
        if not self._path_provided():
            if self._path_valid(self._terraform_workspace_default):
                build_tf = False
            else:
                build_tf = True
            self._terraform_engine.action(self, self._terraform_workspace_default,
                                          build_tf, self._ip_output_name, "create")
            res = {'name': self.asset.name, 'ip': self._ip, "asset_id": 1}
            self.asset.asset_id = 1
            self.logger.info(res)
            return [res]
        else:
            if self._path_valid(self._terraform_workspace):
                build_tf = False
                self._terraform_engine.action(self, self._terraform_workspace, build_tf, self._ip_output_name, "create")
                res = {'name': self.asset.name, 'ip': self._ip}
                self.logger.info(res)
                return [res]
            else:
                raise TefloProvisionerError("The terraform worspace path %s is invalid" % self._terraform_workspace)

    def delete(self):
        self.asset.asset_id = 1
        if not self._path_provided():
            build_tf = False
            self._terraform_engine.action(self, self._terraform_workspace_default,
                                          build_tf, self._ip_output_name, "destroy")
        else:
            if self._path_valid(self._terraform_workspace):
                build_tf = False
                self._terraform_engine.action(self, self._terraform_workspace,
                                              build_tf, self._ip_output_name, "destroy")

    def authenticate(self):
        raise NotImplementedError

    def validate(self):
        if self._path_provided():
            terraform_validate_res, terraform_validate_res_stdout = self._terraform_engine.validate(
                self._terraform_workspace)
        else:
            if not self._path_valid(self._terraform_workspace_default):
                self._terraform_engine.create_terraform_workspace(self._terraform_workspace_default)
                os.chdir(self._terraform_workspace_default)
                self._terraform_engine.build_tf_file(self._terraform_resource_definition.get("hcl"))
            os.chdir(self._terraform_workspace_default)
            self._terraform_engine.terraform_action(action="init")
            terraform_validate_res, terraform_validate_res_stdout = self._terraform_engine.validate(
                self._terraform_workspace_default)

        if not terraform_validate_res:
            raise TefloProvisionerError(terraform_validate_res_stdout)
        else:
            import yaml
            schema_validator(schema_data=self._terraform_resource_definition,
                             schema_files=[self.__schema_file_path__],
                             schema_ext_files=[self.__schema_ext_path__])
            self.logger.info('successfully validated scenario Asset with Terraform!')
