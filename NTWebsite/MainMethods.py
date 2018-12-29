from NTWebsite import AppConfig
# import AppConfig
import datetime
import hashlib
import base64
from oscrypto._win import symmetric
from NTWebsite.models import PreferredConfigName, ConfigParams
import os

def GetStringFromHtml(HtmlPath, filename, EncodeType="utf-8"):
    path = os.path.join(HtmlPath, filename)
    with open(path, encoding=EncodeType, errors="ignore") as htmlfile:
        htmlstring = htmlfile.read()

    return htmlstring


def Encrypt(data):

    return symmetric.aes_cbc_pkcs7_encrypt(AppConfig.S_Key.encode('utf-8'),
                                           data.encode('utf-8'),
                                           AppConfig.S_IV.encode('utf-8'))[1]


def Decrypt(data):

    return symmetric.aes_cbc_pkcs7_decrypt(AppConfig.S_Key.encode('utf-8'),
                                           data,
                                           AppConfig.S_IV.encode('utf-8')).decode('utf-8')


def EncodeWithBase64(data):

            # b64encode是编码，b64decode是解码
    return base64.b64encode(data).decode()


def DecodeWithBase64(data):

            # b64encode是编码，b64decode是解码
    return base64.b64decode(data)


def MD5(str):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def GetUserIP(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:

        return request.META['HTTP_X_FORWARDED_FOR']
    else:

        return request.META['REMOTE_ADDR']

def GetConfig():
    config = {}
    ConfigName = PreferredConfigName.objects.all()[0].PC_Name.CP_Name
    ConfigObject = ConfigParams.objects.get(CP_Name=ConfigName)
    config['ReadsLimit'] = ConfigObject.CP_ReadsThreshold
    config['HotKeyWord'] = ConfigObject.CP_HotKeyWord
    config['TopicsLimit'] = ConfigObject.CP_TopicsLimit
    config['TopicsPageLimit'] = ConfigObject.CP_TopicsPageLimit
    config['CommentsLimit'] = ConfigObject.CP_CommentsLimit
    config['CommentsPageLimit'] = ConfigObject.CP_CommentsPageLimit
    config['AvatarResolution'] = ConfigObject.CP_AvatarResolution
    config['SpecialTopicsPageLimit'] = ConfigObject.CP_SpecialTopicsPageLimit
    config['RollCallsPageLimit'] = ConfigObject.CP_RollCallsPageLimit
    return config

if __name__ == "__main__":
    eco = EncodeWithBase64(
        Encrypt('重庆市*&……&*%%*&……*&%*&%*&%*&%……*……&南岸区北冰露（）》》》》》。。。。'))
    deco = DecodeWithBase64(eco)
    print(Decrypt(deco))
    # print(decrypt(Encrypt('flysafely')))
