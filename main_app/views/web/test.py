from django.shortcuts import render
from django.shortcuts import render,redirect
from django.core.urlresolvers import reverse #用来进行命名空间的反调用
from django.contrib.auth import authenticate, login,logout
from django.http import HttpResponse,HttpResponseRedirect #HttpResponseRedirect是用于进行url进行跳转
from main_app.models import *
from datetime import date,timedelta
from .time_deal import *
from django.contrib.auth.decorators import login_required
import django.utils.timezone as timezone
from django.http import Http404
from decimal import *
from MainDB.models import *

@login_required
def test(request):
    return render(request,"post-code.html")