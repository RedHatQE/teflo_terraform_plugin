import os
import subprocess
import uuid
from teflo.exceptions import TefloProvisionerError

class TerraformHelper():
    def get_ip(self,ret, ipretname):
        stdout = str(ret.communicate()[0], encoding="utf-8")
        arr = stdout.split("\n")
        ip = ""
        for item in arr:
            if item.__contains__(ipretname):
                mid = item.split("\"")
                ip = mid[-2]
        return ip

    def build_tf_file(self,hcl):
        import json
        file = open("terraform" + str(uuid.uuid4().hex)[:6] + ".tf.json", "w+")
        tf = json.dumps(hcl, indent=4)
        file.write(tf)

    def terraform_action(self,action):
        if action == "create":
            subprocess.call(["terraform", "init"])
            stdout = subprocess.Popen(["terraform", "apply", "-auto-approve"], stdout=subprocess.PIPE)
            return stdout
        elif action =="destroy":
            subprocess.call(["terraform", "destroy", "-auto-approve"])

    def action(self,cls, path,build_tf,ip_output_name,action):
        pwd = os.getcwd()
        os.chdir(path)
        if build_tf:
            self.build_tf_file(cls._terraform_resource_definition.get("hcl"))
        stdout = self.terraform_action(action)
        if action == "create":
            cls._ip = self.get_ip(stdout, ip_output_name)
        os.chdir(pwd)

    def create_terraform_workspace(self,path):
        if os.path.isdir(path):
            raise TefloProvisionerError(
                "There already exit a terraform workspace under current teflo workspace, please provide this path to workspace_path under terraform_resource_definition")
        os.mkdir(path)
