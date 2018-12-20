from django.contrib import auth
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, render
from django.template import Template, Context, RequestContext
from NTWebsite import MainMethods as mMs
from NTWebsite import AppConfig as aConf
from NTWebsite.models import UserCircuseeCollect,RollCallReadsIP,RollCallDialogue,RollCallInfo, UserCollect, UserLink, TopicArticleStatistic, ArticleUserLikesOrDislikesTable, CommentUserLikesOrDislikesTable, ArticleReadsIP, User, CategoryInfo, ArticleComment
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from PIL import Image as im
from NTConfig import settings
import sys
import os
import base64
import uuid
import time