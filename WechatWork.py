#!/usr/bin/env python
# encoding: utf-8
# Time    : 2/28/2019 4:19 PM
# Author  : Luzaofa

import time
import requests
import json
import sys

if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')


class WeChat(object):
    def __init__(self, user):
        self.CORPID = 'XXX'
        self.CORPSECRET = 'XXX'
        self.AGENTID = 'XXX'
        self.TOUSER = user  # 接收者用户名

    def _get_access_token(self):
        url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        values = {'corpid': self.CORPID,
                  'corpsecret': self.CORPSECRET,
                  }
        req = requests.post(url, params=values)
        data = json.loads(req.text)
        # print data
        return data["access_token"]

    def get_access_token(self):
        try:
            with open('token/access_token.conf', 'r') as f:
                t, access_token = f.read().split()
        except Exception:
            with open('token/access_token.conf', 'w') as f:
                access_token = self._get_access_token()
                cur_time = time.time()
                f.write('\t'.join([str(cur_time), access_token]))
                return access_token
        else:
            cur_time = time.time()
            if 0 < cur_time - float(t) < 7260:
                return access_token
            else:
                with open('token/access_token.conf', 'w') as f:
                    access_token = self._get_access_token()
                    f.write('\t'.join([str(cur_time), access_token]))
                    return access_token

    def send_data(self, message):
        msg = message.encode('utf-8')
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + self.get_access_token()
        send_data = '{"msgtype": "text", "safe": "0", "agentid": %s, "touser": "%s", "text": {"content": "%s"}}' % (
            self.AGENTID, self.TOUSER, msg)
        r = requests.post(send_url, send_data)
        # print r.content
        return r.content


if __name__ == '__main__':
    wx = WeChat('luzaofa')
    wx.send_data("test")
