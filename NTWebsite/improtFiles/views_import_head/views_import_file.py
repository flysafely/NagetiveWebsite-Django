from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import Template, Context, RequestContext
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
#from django.db.models import Q
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from ..models_import_head import *

from PIL import Image as im
from NTConfig import settings

from NTWebsite import MainMethods as mMs
from NTWebsite.MainMethods import QueryDataBaseCache as QDBC
from NTWebsite import AppConfig as aConf
'''
from NTWebsite.models import \
NotificationTable,\
RecommendAuthor,\
SpecialTopicComment,\
SpecialTopicReadsIP,\
SpecialTopicFollow,\
SpecialTopicInfo,\
UserCircuseeCollect,\
RollCallReadsIP,\
RollCallDialogue,\
RollCallInfo,\
UserCollect,\
UserLink,\
TopicArticleStatistic,\
ArticleUserLikesOrDislikesTable,\
CommentUserLikesOrDislikesTable,\
ArticleReadsIP,\
User,\
CategoryInfo,\
ArticleComment,\
BlackList
'''

import sys
import os
import base64
import uuid
import time
import json
import redis
from django_redis import get_redis_connection
