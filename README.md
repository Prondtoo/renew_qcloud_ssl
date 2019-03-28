# renew_qcloud_ssl
Automatically delete the old SSL certificate on Tencent Cloud and upload a new SSL certificate.

## 这个脚本的使用场景
本人的网站由腾讯云CDN托管，使用的是Let's Encrypt的SSL证书，有效期很短，需要一个能自动定时运行更新证书的脚本。

## 使用说明 （以CentOS7为例）
**要求python版本3.6+**

### 1. 安装腾讯云的SDK
```pip3.6 install qcloudapi-sdk-python```

### 2. 根据需求配置文件
主要修改的地方有：
```DOMAIN = "域名"
CERTPATH = "证书路径"
KEYPATH = "私钥路径"
config = {
    'secretId': '腾讯云API的ID',
    'secretKey': '腾讯云API的key',
}
```
API的key[点击这里获取](https://console.qcloud.com/capi)

### 3. 结合certbot加入到定时任务crontab里面
例如，每个月的第28天运行此脚本
```crontab -e
10 13 28 * * certbot renew
10 14 28 * * python3.6 /root/auto_renew_qcloudssl.py
```
