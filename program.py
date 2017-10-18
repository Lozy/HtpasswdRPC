#!/bin/env python
# -*- coding: utf-8 -*-

import os
import crypt
import random
import string
import zerorpc


class HtpasswdHandle(object):
    def __init__(self, file_path):
        self.content = {}
        self.file = file_path
        self.load_from_file()

    @staticmethod
    def _salt():
        letters = string.ascii_letters + string.digits
        return random.choice(letters) + random.choice(letters)

    def load_from_file(self):
        """
        load user-data from password file.
        """
        if os.path.isfile(self.file):
            with open(self.file, 'r') as file_handle:
                for line in file_handle.readlines():
                    username, cypher_text = line.split(":")
                    self.content[username] = cypher_text

    def save_file(self):
        with open(self.file, 'w') as file_handle:
            file_handle.writelines(["{}:{}\n".format(item, self.content[item]) for item in self.content])

    def update(self, username, password):
        self.content[username] = crypt.crypt(password, self._salt())
        self.save_file()
        return True

    def delete(self, username):
        self.content.pop(username)
        self.save_file()
        return True

    def exist(self, username):
        return True if username in self.content else False


def rpc_server(passwd_file, host, port, debug):
    server = zerorpc.Server(HtpasswdHandle(passwd_file), heartbeat=5)
    server.bind("tcp://{}:{}".format(host, port))
    server.debug = debug

    try:
        server.run()
    except KeyboardInterrupt:
        print "zerorpc server terminate"
    except:
        print "zerorpc server reach error"
        raise


if __name__ == '__main__':
    rpc_server('/etc/danted/sockd.passwd', '127.0.0.1', '9090', True)
