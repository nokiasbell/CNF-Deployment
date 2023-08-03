import re
import sys
import argparse

from sessionbase import SSHConnection

class VDU_Kuafu_Operator(object):
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
        self.child.sendline("grep --color=never -nE ^build_version= vdu_config.ini")
        self.prompt()
        search_obj = re.search(r"(\d+):build_version=([\w.]+)",self.child.before)
        line_index = search_obj.group(1)
        current_version = search_obj.group(2)

        # print(f"line_index: {line_index}")
        # print(f"current_version: {current_version}")
        if current_version != package_version:
            self.child.sendline(f"sed -i \"{line_index} s/^/#/\" vdu_config.ini")
            self.prompt()
            self.child.sendline(f"sed -i \"{line_index}a build_version={package_version}\" vdu_config.ini")
            self.prompt()


    def change_work_directory(self):
        self.child.sendline(f"cd ~/{self.kuafu_version}/scenarios/vdu_l3call/")
        self.prompt()
        self.child.sendline("ls --color=never")
        self.prompt()

    def onboard_image(self):
        self.child.sendline("./16-onboard-vdu.sh")
        idx = self.child.expect(["error", self.cli_prompt],900)
        if idx == 0:
            raise Exception(f"[Error] Onboard failure")
        else:
            return

    def deploy_vdu(self):
        self.child.sendline("./21-create-vdu.sh")
        idx = self.child.expect(["vDU creation successful",r"Create vDU chart \w+ failure"], 900)
        if idx == 0:
            return
        else:
            if idx == 1:
                raise Exception("[Error] vDU deploy failure!")

    def delete_vdu(self):
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

        self.child.sendline("./20-delete-vdu.sh")
        idx = self.child.expect(["vDU deletion successful","vDU deletion failure"], 600)
        if idx == 1:
            raise Exception("[Error] vDU deletion failure!")

        self.prompt()
        self.child.sendline(f"kubectl get pods -n {self.namespace}")
        self.prompt()
        self.clean_pv()

    def clean_pv(self):
        self.child.sendline(f"kubectl get pv -n {self.namespace} | grep {self.namespace} --color=never")
        idx = self.child.expect(["Released","Bound",self.cli_prompt])
        print(f"idx: {idx}")
        if idx == 0:
            self.prompt()
            self.child.sendline(f"kubectl get pv -n {self.namespace} | grep Released | awk -F ' ' '{{print $1}}' | xargs kubectl delete pv")
            self.prompt(60)
        elif idx == 1:
            raise Exception("[WARN] PV state is Bound, please handle it manually!")

        self.child.sendline(f"kubectl get pv -n {self.namespace}")
        self.prompt()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process vDU installation.')
    parser.add_argument("--pkgname",required=True)
    parser.add_argument("--vduip",required=True)
    parser.add_argument("--vduuser",required=True)
    parser.add_argument("--vdupswd",required=True)
    parser.add_argument("--kuafu_version",default="kuafu-v5.20.0")
    parser.add_argument("--namespace",required=True)
    parser.add_argument("--need_onboard",choices=["Yes","No"])
    args = parser.parse_args()
    # args = parser.parse_args([
    #             "--pkgname","0.300.4760",
    #             "--vduip","10.69.54.114",
    #             "--vduuser","core",
    #             "--vdupswd","system123",
    #             "--namespace","cran1",
    #             "--need_onboard","No"
    #     ])

    package_name = args.pkgname
    vdu_ip = args.vduip
    vdu_user = args.vduuser
    vdu_pswd = args.vdupswd
    kuafu_version = args.kuafu_version
    namespace = args.namespace
    need_onboard = args.need_onboard

    print(package_name)
    print(vdu_ip)
    print(vdu_user)
    print(vdu_pswd)
    print(kuafu_version)
    print(namespace)
    print(need_onboard)
    with VDU_Kuafu_Operator(vdu_ip,vdu_user,vdu_pswd,kuafu_version,namespace) as vdu_session:
        vdu_session.modify_package_version(package_name)
        vdu_session.change_work_directory()
        vdu_session.delete_vdu()
        if need_onboard == "Yes":
            vdu_session.onboard_image()
        vdu_session.deploy_vdu()
