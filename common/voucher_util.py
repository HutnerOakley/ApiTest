import os
import json
from common.requests_util import HttpRequest

jessionid_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], 'config', 'JESSIONID.txt')


class VoucherUtil(object):

    def get_jessionid(self):
        '''
        获取jessionid
        :return:
        '''
        with open(jessionid_path, 'r')as f:
            value = f.read()
        api_token = json.loads(value).get('api-token')
        return api_token

    def get_token(self):
        '''
        获取token
        :return:
        '''
        url = "https://idsaas.test.leiniao.com/idsaas/generateToken"
        headers = {
            "Cookie": (
                          "rhp=https://idsaas.test.leiniao.com; JSESSIONID=%s; return-url=https://idsaas.test.leiniao.com/page/cms-api-docs/#/") % self.get_jessionid(),
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": "en-GB,en;q=0.9,fr-FR;q=0.8,fr;q=0.7,es-US;q=0.6,es;q=0.5,pt-PT;q=0.4,pt;q=0.3,it-IT;q=0.2,it;q=0.1,zh-CN;q=0.1,zh;q=0.1,ar-IL;q=0.1,ar;q=0.1,ru-RU;q=0.1,ru;q=0.1,zh-TW;q=0.1,en-US;q=0.1,es-ES;q=0.1,smn-FI;q=0.1,smn;q=0.1,hy-AM;q=0.1,hy;q=0.1",
            "Accept-Encoding": "gzip, deflate, br",
            "Cache-Control": "max-age=0",
            "Content-Type": "application/json;charset=UTF-8",
            "traditional": "true"
        }
        res = HttpRequest(url='https://idsaas.test.leiniao.com/idsaas').get(url='/generateToken',headers=headers).json()
        return res["data"]["generatedToken"]


if __name__ == '__main__':
    # api_token = VoucherUtil().get_jessionid()
    # print(api_token)
    token = voucher = VoucherUtil().get_token()
    print(token)

