from NTWebsite import AppConfig
from .improtFiles.models_import_head import *
#import AppConfig
#from models.Configuration import *
from NTWebsite.models.Configuration import *
from django_redis import get_redis_connection
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from oscrypto._win import symmetric

import datetime
import hashlib
import base64
import os

def QueryDataBaseCache(TableName, Method, TimeOut=60, Refresh=False, *Conditions, **Others):
    QueryString = "%s.objects.%s(%s)%s[0:%s]" % (TableName, Method, ','.join(Conditions), Others['operations'] if 'operations' in Others.keys() else '', Others['limit'] if 'limit' in Others.keys() else '')
    QueryString_MD5 = MD5(QueryString)
    print(QueryString,QueryString_MD5)
    #如下方式不支持存入除去byte string number以外的其他复杂数据类型
    #RedisConn = get_redis_connection("default")
    #RedisConn.setTimeOut = TimeOut
    if cache.get(QueryString_MD5) and Refresh != True:
        print('存在直接提取')
        return cache.get(QueryString_MD5)
    else:
        print('写入中......')
        QueryResult = eval("%s.objects.%s(%s)%s[0:%s]" % (TableName, Method,','.join(Conditions), Others['operations'] if 'operations' in Others.keys() else '', Others['limit'] if 'limit' in Others.keys() else ''))
        cache.set(QueryString_MD5,QueryResult,TimeOut)
        print('已经写入',QueryString_MD5)


def WriteDataBaseCache():
    pass

def GetStringFromHtml(HtmlPath, filename, EncodeType="utf-8"):
    path = os.path.join(HtmlPath, filename)
    with open(path, encoding=EncodeType, errors="ignore") as htmlfile:
        htmlstring = htmlfile.read()

    return htmlstring


def Encrypt(data):
    Config = GetConfig()
    return symmetric.aes_cbc_pkcs7_encrypt(Config['SecretKey'].encode('utf-8'),
                                           data.encode('utf-8'),
                                           Config['SecretVI'].encode('utf-8'))[1]


def Decrypt(data):
    Config = GetConfig()
    return symmetric.aes_cbc_pkcs7_decrypt(Config['SecretKey'].encode('utf-8'),
                                           data,
                                           Config['SecretVI'].encode('utf-8')).decode('utf-8')


def EncodeWithBase64(data):

            # b64encode是编码，b64decode是解码
    return base64.b64encode(data).decode()


def DecodeWithBase64(data):

            # b64encode是编码，b64decode是解码
    return base64.b64decode(data)


def MD5(data):
    hash_md5 = hashlib.md5(data.encode('utf-8'))
    return hash_md5.hexdigest()


def GetUserIP(request):
    if 'HTTP_X_FORWARDED_FOR' in request.META:

        return request.META['HTTP_X_FORWARDED_FOR']
    else:

        return request.META['REMOTE_ADDR']


def GetConfig():
    config = {}
    ConfigName = PreferredConfigName.objects.all()[0].PC_Name.CP_Name
    ConfigObject = ConfigParams.objects.get(CP_Name=ConfigName)
    config['SecretKey'] = ConfigObject.CP_SecretKey
    config['SecretVI'] = ConfigObject.CP_SecretVI
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
