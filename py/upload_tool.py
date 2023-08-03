import re
import sys
import argparse

from sessionbase import SSHConnection


class Upload_Tool(object):
    def __init__(self, host, username, password, kuafu_version):
        self.child = SSHConnection()
        self.child.logfile_read = sys.stdout
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
