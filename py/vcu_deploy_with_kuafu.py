import re
import sys
import argparse

from sessionbase import SSHConnection
from timer import Timer

class VCU_Kuafu_Operator(object):
    def __init__(self, host, username, password, kuafu_version, namespace):
        self.child = SSHConnection()
        # self.child.logfile_read = None
        self.child.logfile_read = sys.stdout
        self.host = host
        self.username = username
        self.password = password
        self.kuafu_version = kuafu_version
        self.namespace = namespace
        self.cli_prompt = r"\$ "

    def __enter__(self):
        self.login()
        return self

    def __exit__(self,exc_type,exc_value,traceback):
        self.logout()

    def prompt(self, timeout=-1):
        self.child.expect(self.cli_prompt,timeout)

    def login(self):
        self.child.spawn(self.host,self.username,self.password)
        self.prompt()

    def logout(self):
        self.child.close()

    def modify_package_version(self, package_version):
        self.child.sendline(f"cd ~/{self.kuafu_version}/artifacts")
        self.prompt()
        self.child.sendline("grep --color=never -nE ^build_version= vcu_config.ini")
        self.prompt()
        search_obj = re.search(r"(\d+):build_version=([\w.]+)",self.child.before)
        line_index = search_obj.group(1)
        current_version = search_obj.group(2)

        # print(f"line_index: {line_index}")
        # print(f"current_version: {current_version}")
        if current_version != package_version:
            self.child.sendline(f"sed -i \"{line_index} s/^/#/\" vcu_config.ini")
            self.prompt()
            self.child.sendline(f"sed -i \"{line_index}a build_version={package_version}\" vcu_config.ini")
            self.prompt()


    def change_work_directory(self):
        self.child.sendline(f"cd ~/{self.kuafu_version}/scenarios/vcu_l3call/")
        self.prompt()
        self.child.sendline("ls --color=never")
        self.prompt()

    def onboard_image(self):
        self.child.sendline("./16-onboard-vcu.sh")
        idx = self.child.expect(["error", self.cli_prompt],900)
        if idx == 0:
            raise Exception(f"[Error] Onboard failure")
        else:
            return

    def deploy_vcu(self):
        self.child.sendline("./21-create-vcu.sh")
        idx = self.child.expect(["vCU creation successful",r"Create vCU chart \w+ failure"], 900)
        if idx == 0:
            return
        else:
            if idx == 1:
                raise Exception("[Error] vCU deploy failure!")

    def delete_vcu(self):
        self.child.sendline(f"helm list -n {self.namespace}")
        idx = self.child.expect([r"VERSION\s+\w", "Error", self.cli_prompt])
        if idx == 0:
            self.prompt()
        elif idx == 1:
            raise Exception("[Error] OCP platform broken!")
        elif idx == 2:
            self.child.sendline(f"kubectl get pods -n {self.namespace}")
            idx = self.child.expect(["No resources found",self.cli_prompt])
            if idx == 0:
                self.prompt()
                return
            else:
                raise Exception("[Error] Helm chart has deleted, but Pod resources still exist!")

        self.child.sendline(f"kubectl get pods -n {self.namespace}")
        self.prompt()

        self.child.sendline("./20-delete-vcu-and-pvc.sh")
        idx = self.child.expect(["vCU deletion successful","vCU deletion failure"], 600)
        if idx == 1:
            raise Exception("[Error] vCU deletion failure!")

        self.prompt()
        self.child.sendline(f"kubectl get pods -n {self.namespace}")
        self.prompt()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process vCU installation.')
    parser.add_argument("--pkgname",required=True)
    parser.add_argument("--vcuip",required=True)
    parser.add_argument("--vcuuser",required=True)
    parser.add_argument("--vcupswd",required=True)
    parser.add_argument("--kuafu_version",default="kuafu-v5.20.0")
    parser.add_argument("--namespace",required=True)
    parser.add_argument("--need_onboard",choices=["Yes","No"])
    args = parser.parse_args()
    # args = parser.parse_args([
    #             "--pkgname","0.250.3888",
    #             "--vcuip","10.107.115.18",
    #             "--vcuuser","cranuser1",
    #             "--vcupswd","systeM!23",
    #             "--namespace","cran1",
    #             "--need_onboard","Yes"
    #     ])

    package_name = args.pkgname
    vcu_ip = args.vcuip
    vcu_user = args.vcuuser
    vcu_pswd = args.vcupswd
    kuafu_version = args.kuafu_version
    namespace = args.namespace
    need_onboard = args.need_onboard

    print(package_name)
    print(vcu_ip)
    print(vcu_user)
    print(vcu_pswd)
    print(kuafu_version)
    print(namespace)
    print(need_onboard)
    with VCU_Kuafu_Operator(vcu_ip,vcu_user,vcu_pswd,kuafu_version,namespace) as vcu_session:
        vcu_session.modify_package_version(package_name)
        vcu_session.change_work_directory()
        vcu_session.delete_vcu()
        if need_onboard == "Yes":
            vcu_session.onboard_image()
        vcu_session.deploy_vcu()