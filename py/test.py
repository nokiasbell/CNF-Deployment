import sys
from sessionbase import SSHConnection


def hello():
    print("hello PHP")
class Kuafu_Transmission(object):
    def __init__(self, host, username, password, kuafu_version):
        self.child = SSHConnection()
        self.child.logfile_read = sys.stdout
        # self.child.logfile_read = log_file
        self.host = host
        self.username = username
        self.password = password
        self.kuafu_version = kuafu_version
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


if __name__ == '__main__':
    # hello()
    vcu_ip = "10.69.57.210"
    vcu_user = "cranuser1"
    vcu_pswd = "systeM!23"
    kuafu_version = "kuafu-v6.19.0"
    # with open("bbb", 'w') as f:
    with Kuafu_Transmission(vcu_ip, vcu_user, vcu_pswd, kuafu_version) as session:
        import time
        time.sleep(10)
        # sys.exit(1)