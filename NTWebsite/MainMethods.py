from NTWebsite import AppConfig
from .improtFiles.models_import_head import *
#import AppConfig
#from models.Configuration import *
from NTWebsite.models.Configuration import *
from django.http import HttpResponse, HttpResponseRedirect
from django_redis import get_redis_connection
from django.views.decorators.cache import cache_page
from django.core.cache import caches
from oscrypto._win import symmetric

import datetime
import hashlib
import base64
import os


def QueryDataBaseCache(**Others):
    #print(QueryString, QueryString_MD5)
    # 如下方式不支持存入除去byte string number以外的其他复杂数据类型
    #RedisConn = get_redis_connection("default")
    #RedisConn2 = get_redis_connection("flysafely")
    #RedisConn.setTimeOut = TimeOut
    # print(Others.keys())
    CacheHandler = caches['default']
    TableName = Others['TableName'] if 'TableName' in Others.keys() else ''
    QueryMethod = Others['QueryMethod'] if 'QueryMethod' in Others.keys(
    ) else ''
    DefaultCondition = Others['DefaultCondition'] if 'DefaultCondition' in Others.keys(
    ) else ''
    TimeOut = Others['TimeOut'] if 'TimeOut' in Others.keys() else 60
    Refresh = Others['Refresh'] if 'Refresh' in Others.keys() else False
    limit = Others['limit'] if 'limit' in Others.keys() else None
    operations = Others['operations'] if 'operations' in Others.keys() else ''

    ConditionsList = []
    DetailsLits = []
    if Others:
        for key in Others:
            if key not in ['TableName', 'TimeOut', 'Refresh', 'limit', 'operations', 'QueryMethod', 'isLimit'] and key != 'DefaultCondition':
                exec("%s_execCreate=Others['%s']" % (key, key))
                ConditionsList.append(key + '=' + key + '_execCreate')
                DetailsLits.append(repr(eval("%s_execCreate" % key)))
            elif key == 'DefaultCondition':
                ConditionsList.append(Others['DefaultCondition'])

    QueryString = "%s.objects.%s(%s)%s%s#%s" % (TableName, QueryMethod, ','.join(
        ConditionsList), operations, "[0:" + limit + "]" if limit else '', ','.join(DetailsLits))
    QueryString_MD5 = MD5(QueryString)

    if CacheHandler.get(QueryString_MD5) and Refresh != True:
        if not CacheHandler.get(QueryString_MD5)[1]:
            return CacheHandler.get(QueryString_MD5)[0]
        else:
            return CacheHandler.get(QueryString_MD5)[0]
    else:
        try:
            QueryResult = eval(QueryString)
        except Exception as e:
            raise e
        else:
            if Refresh != True:
                CacheHandler.set(QueryString_MD5, (QueryResult,
                                                   True if QueryResult else False,), TimeOut)
            return QueryResult


def WriteToDataBaseFromCache():
    return cache


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
    config['ReadsThreshold'] = ConfigObject.CP_ReadsThreshold
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
