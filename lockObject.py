'''
Created on 2016-06-19
'''

import json
import string
import random

class lockObject():
    def __init__(self):
        self.users = {}
        self.ulock = {}
        self.qrN = 15;
        jfile = open('ulock.json', 'r')
        self.ulock = json.load(jfile)
        jfile.close()
        jfile = open('users.json', 'r')
        self.users = json.load(jfile)
        jfile.close()

    def randString(self):
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(self.qrN))

    def draw_cid(self, cid):
        for key in self.ulock:
            if self.ulock[key]['full'] == 1 and self.ulock[key]['cardid'] == cid:
                return key
        else:
            return False

    def draw_qrcode(self, qrcode):
        for key in self.ulock:
            if self.ulock[key]['full'] == 1 and self.ulock[key]['qrcode'] == qrcode:
                return key
        return False

    def add_item(self, uid, lockid):
        if lockid in self.ulock and uid in self.users and self.ulock[lockid]['full'] == 0:
            self.ulock[lockid]['full'] = 1
            self.ulock[lockid]['uid'] = uid
            self.ulock[lockid]['cardid'] = self.users[uid]['cardid']
            self.ulock[lockid]['qrcode'] = self.randString()
            with open('ulock.json', 'w') as jfile:
                json.dump(self.ulock, jfile)
                jfile.close()
            return self.ulock[lockid]['qrcode']
        else:
            return False

    def remove_item(self, lockid):
        if lockid in self.ulock:
            self.ulock[lockid]['full'] = 0;
        with open('ulock.json', 'w') as jfile:
            json.dump(self.ulock, jfile)
            jfile.close()
