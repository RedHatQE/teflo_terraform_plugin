# -*- coding: utf-8 -*-
#
# Copyright (C) 2020 Red Hat, Inc.
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

    :copyright: (c) 2020 Red Hat, Inc.
    :license: GPLv3, see LICENSE for more details.
"""


import os
import subprocess
import uuid
import logging
from teflo.core import ProvisionerPlugin
from teflo.exceptions import TefloProvisionerError
from teflo.helpers import schema_validator


class TerraformProvisionerPlugin(ProvisionerPlugin):
    # Give your plugin name property here. This will be the name that will be used in the scenario descriptor file
    __plugin_name__ = 'teflo_terraform_plugin'

    __schema_file_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                            "files/schema.yml"))
    __schema_ext_path__ = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                       "files/schema_extensions.py"))
    _ip = ""

    def __init__(self, asset):
        # your plugin init method which takes in teflo asset resource object as input

        super(TerraformProvisionerPlugin, self).__init__(asset)
        self._terraform_workspace_default = self.workspace + \
            "/" + str(uuid.uuid4().hex)[:6] + "teflo_terraform_workspace"
        self._terraform_resource_definition = self.asset.allparameters.get("terraform_resource_definition", None)
        self._terraform_workspace = self._terraform_resource_definition.get("workspace_path", None)
        self._ip_output_name = self._terraform_resource_definition.get("ip_output_name", "ip_output_name")
        # print(self._terraform_resource_definition)
        # this is the terraform input

        # creating logger for this plugin to get added to teflo loggers. create_logger is teflo method
        self.create_logger(name=self.__plugin_name__, data_folder=self.config.get('DATA_FOLDER'))  # OR use teflo logger
        # self.logger = logging.getLogger(self.__plugin_name__)

    def _get_ip(self, ret, ipretname):
        stdout = str(ret.communicate()[0], encoding="utf-8")
        arr = stdout.split("\n")
        ip = ""
        for item in arr:
            if item.__contains__(ipretname):
                mid = item.split("\"")
                ip = mid[-2]
        return ip

    def _path_provided(self):
        return self._terraform_workspace is not None

    def _path_valid(self, path):
        return os.path.isdir(path)

    # def build_result(self):
    #     ret = []
    #     res = {'name':self.asset}
    def _create_terraform_workspace(self, path):
        os.mkdir(path)

    def _build_tf_file(self):
        import json
        file = open("terraform" + str(uuid.uuid4().hex)[:6] + ".tf.json", "w+")
        tf = json.dumps(self._terraform_resource_definition.get("hcl"),indent=4)
        file.write(tf)

    def create(self):
        # print(self.asset.profile())
        if not self._path_provided():
            print(self._terraform_workspace_default)
            self._create_terraform_workspace(self._terraform_workspace_default)
            pwd = os.getcwd()
            os.chdir(self._terraform_workspace_default)
            self._build_tf_file()
            subprocess.call(["terraform", "init"])
            stdout = subprocess.Popen(["terraform", "apply", "-auto-approve"], stdout=subprocess.PIPE)
            self._ip = self._get_ip(stdout, self._ip_output_name)
            os.chdir(pwd)
            res = {'name': self.asset.name, 'ip': self._ip}
            self.logger.info(res)
            return [res]
        else:
            if self._path_valid(self._terraform_workspace):
                pwd = os.getcwd()
                os.chdir(self.path)
                subprocess.call(["terraform", "init"])
                stdout = subprocess.Popen(["terraform", "apply", "-auto-approve"], stdout=subprocess.PIPE)
                self._ip = self._get_ip(stdout, self._ipname)
                os.chdir(pwd)
                res = {'name': self.asset.name, 'ip': self._ip}
                self.logger.info(res)
                return [res]
            else:
                raise TefloProvisionerError("The terraform worspace path is invalid")

    def delete(self):
        raise NotImplementedError

    def authenticate(self):
        raise NotImplementedError

    def validate(self):
        print("success validate")
