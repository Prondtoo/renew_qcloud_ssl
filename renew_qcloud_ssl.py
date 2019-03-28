# -*- coding: utf8 -*-
from QcloudApi.qcloudapi import QcloudApi
import logging
import json
import os


DOMAIN = "*.pzwa.net"
CERTPATH = "/etc/letsencrypt/live/pzwa.net/fullchain.pem"
KEYPATH = "/etc/letsencrypt/live/pzwa.net/privkey.pem"


# 设置需要加载的模块
module = 'wss'
# 云API的公共参数
config = {
    'secretId': 'AAAAAAAAAABBBBBBBB',
    'secretKey': 'AAAABBBBBBBBBBBBB',
    'method': 'GET',
    'SignatureMethod': 'HmacSHA1',
}




def delete_old_ssl(domain):
    ##########  获取对应域名的ID
    try:
        action = 'CertGetList'
        action_params = {
            'Limit': 1,
        }
        service = QcloudApi(module, config)
        result_json = service.call(action, action_params)
        get_result = json.loads(result_json)
        if get_result['code'] != 0:
            raise  Exception
        data = (get_result['data'])['list']
        domain_id = ""
        #####找到匹配的ID
        for i in data:
            if(i['domain']) == domain:
                domain_id = i['id']
                break
        #####执行删除操作
        try:
            action = 'CertDelete'
            action_params = {
                'Limit': 1,
                'id': domain_id
            }
            service = QcloudApi(module, config)
            result_json = service.call(action, action_params)
            result = json.loads(result_json)
            if result['code'] != 0:
                raise Exception
            else:
                logging.info("Successfully deleted certificate")
        except Exception as e:
            logging.warning(result['message'])
            os._exit(0)
    except Exception as e:
        logging.warning(get_result['message'])
        os._exit(0)


def update_new_ssl():
    with open(CERTPATH, 'r') as f:
        cert = f.read()
    with open(KEYPATH, 'r') as f:
        key = f.read()
    try:
        action = 'CertUpload'
        action_params = {
            'Limit': 1,
            'cert': cert,
            'certType': "SVR",
            'key': key,
            'alias': "Auto upload from script"
        }
        service = QcloudApi(module, config)
        result_json = service.call(action, action_params)
        result = json.loads(result_json)
        if result['code'] != 0:
            raise Exception
        else:
            logging.info(result['message'])
    except Exception as e:
        logging.warning(result['message'])
        os._exit(0)


if __name__ == '__main__':
    delete_old_ssl(DOMAIN)
    update_new_ssl()