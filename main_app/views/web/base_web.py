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
import time

@login_required
def test_web(request):
    result = Time_code.objects.filter(code="testtesttest2").count()
    return HttpResponse(result)

@login_required
def check_code_page(request):
    if request.method == 'GET':
        return render(request,"check_code_page.html")
    else:
        try:
            code = request.POST["code"]
        except: #检查是否存在
            return render(request,"check_code_page.html",{"warn":"请输入正确的卡密！"})
        try:
            code_object = Time_code.objects.get(code=code)
        except Time_code.DoesNotExist: #检查是否正确
            return render(request, "check_code_page.html", {"warn": "请输入正确的卡密！"})

        if request.user.others_info.level > 1:  #检测是否有权限
            if request.user.is_superuser:
                return render(request, "check_code_page.html", {"warn": "错误！你无权查询！"})

        return redirect("check_my_code",code=code_object.code)


@login_required
def check_my_code(request,code):
    user = request.user
    try:
        Hcode = Time_code.objects.get(code=code)
    except Time_code.DoesNotExist: #找不到卡密
        context = {"link": "/shop/check_code_page/", "error_name": "错误，此卡密不存在", "error_name2": "错误！此卡密不存在！",
                   "error_name3": "此卡密不存在，请重试！"}
        return render(request, 'page-error.html', context)  # 引入

    if user.others_info.level != 1 or user.is_superuser == True or Hcode.proxy_man == user: #检查是否有查看卡密的权限
        context = {}
        context["code"] = Hcode.code
        context["name"] = Hcode.software.software_name
        context["prices"] = "%.2f" % Hcode.cost
        context["time"] = "%d天" % Hcode.time
        context["buyer"] = Hcode.proxy_man.username
        if Hcode.used:
            context["used"] = "已使用"
            # 加一个linux时间戳转换bu'y
        else:
            context["used"] = "未使用"
        return render(request, "check-my-code.html", context)

    else:
        context = {"link": "/shop/check_code_page/", "error_name": "你无权查询！", "error_name2": "错误！你无权查询！",
                   "error_name3": "你无权查询！"}
        return render(request, 'page-error.html', context)  # 引入



"""
提交卡密
"""
@login_required
def Admin_Post_Code(request):
    if request.user.is_superuser: #是管理员
        if request.method == 'GET':
            all_vip = Software.objects.all()
            return render(request,"post-code.html",{"software":all_vip})
        else:
            all_vip = Software.objects.all()
            try:
                software_name = request.POST["software_id"]
                Codes = request.POST["Codes"]
            except:
                return render(request,"post-code.html",{"warn":"请重新正确输入!","software":all_vip})
            if software_name == "None":
                return render(request,"post-code.html",{"warn":"请选择会员种类!","software":all_vip})
            if Codes == "":
                return render(request, "post-code.html", {"warn": "请输入卡密信息!", "software": all_vip})

            #检查会员种类
            try:
                vip = all_vip.get(software_id=software_name)
            except Software.DoesNotExist:
                return render(request, "post-code.html", {"warn": "请选择会员种类!", "software": all_vip})

            try:
                Checked = request.POST["Check"] #检查是否查重
            except:
                Checked = "0"
            #完成录入
            #需要测试查重问题
            strlist = Codes.splitlines() #分隔密链
            #去除特殊字符
            strlist_new = []
            for m in strlist:
                str_o = m.replace("\n", "").replace(" ", "").replace("\t", "").replace("\r", "")
                if (str_o !=""):
                    strlist_new.append(str_o)
            count = 0
            #查重完毕
            #开始录入

            for j in strlist_new:
                try:
                    code = Time_code.objects.create(software=vip,time=vip.software_each_time,code=j,cost=vip.software_cost) #录入卡密
                    code.save()
                    count +=1
                except:
                    continue
            #录入完毕
            if (count == 0):
                return render(request, "post-code.html", {"warn": "并未录入！可能有重复", "software": all_vip})
            return render(request, "post-code.html", {"success": "成功录入%d个卡密!" % count, "software": all_vip})

    else: #不是管理员就404
        context = {"link": "/", "error_name": "错误", "error_name2": "你无权查看此页面",
                   "error_name3": "你无权查看此页面"}
        return render(request, 'page-error.html', context)

"""
创建会员种类
"""
@login_required
def Admin_Post_Vip(request):
    if (request.user.is_superuser):
        if request.method == 'GET':
            #这里待会要加个vip信息
            return render(request,"post-vip.html")
        else:
            try:
                vip_name = request.POST["vip_name"]
                if vip_name == "":
                    return render(request, "post-vip.html", {"warn": "请输入会员名！"})
                vip_prices = request.POST["vip_prices"]
                vip_time = request.POST["vip_time"]
                vip_version = request.POST["vip_version"]
            except:
                return render(request, "post-vip.html", {"warn": "请正确输入！"})
            try:
                vip_time = int(vip_time)
                vip_prices = int(vip_prices)
            except ValueError:
                return render(request,"post-vip.html",{"warn":"输入有误！请输入正整数！"})
            try:
                vip_prices = Decimal(vip_prices)
            except decimal.InvalidOperation:
                return render(request,"post-vip.html",{"warn","价格输入有误！请输入正整数"})
            new_vip =  Software.objects.create(software_id=get_software_code(),software_name=vip_name,software_cost=vip_prices,software_each_time=vip_time,software_version_number=vip_version)
            new_vip.save()
            return render(request,"post-vip.html",{"success":"成功创建会员："+vip_name})
    else:
        context = {"link": "/", "error_name": "错误", "error_name2": "你无权查看此页面",
                   "error_name3": "你无权查看此页面"}
        return render(request, 'page-error.html', context)


"""
可通过TOKEN或username找代理账号
返回一个列表，第一个是User对象，第二个是Others_info对象。
"""
def get_proxy_account(TOKEN=None,username=None,pk_id = None):
    if TOKEN != None:
        try:
            user_others_info = Others_info.objects.get(TOKEN=TOKEN)
            return [user_others_info.user,user_others_info]
        except:
            return False
    elif username != None:
        try:
            user_object = User.objects.get_by_natural_key(username=username)
            user_others_info = Others_info.objects.get(user=user_object)
            return [user_object,user_others_info]
        except:
            return False
    elif pk_id != None:
        try:
            user_object = User.objects.get(pk=pk_id)
            user_others_info = Others_info.objects.get(user=user_object)
            return  [user_object,user_others_info]
        except:
            return False

def get_my_up_proxy(user): #传入一个get_proxy_account函数的返回列表，user[0]是user对象，user[1]是others_info 对象
    if user[1].up_proxy != 0: #如果传入的账号有上级代理
        a = []
        up_user = get_proxy_account(pk_id=user[1].up_proxy) #获取他上级代理的特殊对象
        a.append(up_user) #添加到列表a中
        b = get_my_up_proxy(up_user) #递归获取它的上级
        if b != False: #如果它的存在，添加到列表中，并返回。
            c = a+b
            return c
        else: #返回a
            return a

    else: #如果传入的账号没有上级代理，返回False
        return False


@login_required
def index_page(request): #控制台主页
    user = request.user
    context = {"username":user.username}
    try:
        user_other_info = Others_info.objects.get(user=user)
    except:
        return HttpResponse("出现错误！报告错误号：1000。\n 你可能登陆了多个账户或管理员账户，请登出后再操作！")
    context["money"] = user_other_info.balance

    try:  #查找已购卡密
        auths = Time_code.objects.filter(proxy_man=user).order_by('id')
        context["auths_num"] = auths.count()
        auths_list =[]
        auths = auths.reverse()
        context["auths_list"] = auths[:4]
    except:
        context["auths_num"] = 0

    context['discount'] = "%.1f" % 1
    context["my_level"] = user_other_info.level

    notices = Notice.objects.all().order_by('-time')  #公告
    notices_list = []
    for i in notices[:3]:
        notices_list.append({"admin_name":i.admin_object.username,"time":i.time.strftime("%Y-%m-%d"),"title":i.title,"word":i.word})
    context["notices_list"]=notices_list
    return render(request,"index.html",context)

@login_required
def shop_page(request):
    user = request.user
    user = get_proxy_account(username=user.username)
    if user == False:
        return HttpResponse("出现错误！报告错误号：1000。\n 你可能登陆了多个账户或管理员账户，请登出后再操作！")
    # 生成本账号折扣
    all_software = Software.objects.all()
    all_software_list = []
    others_info_object = Others_info.objects.get(user=request.user)
    discount = Decimal(1 - (user[1].level * 0.05)) # 折扣，输出一个浮点数
    for i in all_software:
        a = {
            "software_cost":"%.2f" % (i.software_cost*discount),
            "software_id":i.software_id,
            "software_name":i.software_name,
            "software_each_time":i.software_each_time,
            "software_version_number":i.software_version_number,
             }
        all_software_list.append(a)

    context = {"all_software":all_software_list}
    return render(request,"page-shop.html",context=context)

@login_required
def shop_detail(request, software_id):
    if request.method == 'GET':
        try:
            user_others_info = Others_info.objects.get(user=request.user)
        except:
            return HttpResponse("出现错误！报告错误号：1000。\n 你可能登陆了多个账户或管理员账户，请登出后再操作！")

        user = request.user
        user = get_proxy_account(username=user.username)
        if user == False:
            return HttpResponse("出现错误！报告错误号：1000。\n 你可能登陆了多个账户或管理员账户，请登出后再操作！")
        #生成本账号折扣
        discount = Decimal(1 - (user[1].level * 0.05))  # 折扣，输出一个浮点数
        software = Software.objects.get(software_id=software_id)
        software_list = {
            "software_cost":"%.2f" % (software.software_cost*discount),
            "software_id":software.software_id,
            "software_name":software.software_name,
            "software_each_time":software.software_each_time,
            "software_version_number":software.software_version_number,
        }
        count = Time_code.objects.filter(software=software,used=False).count()
        list_num = []
        for i in range(1,count+1):
            list_num.append(i)
        context = {"software": software_list, "money": user_others_info.balance,"count":count,"list_num":list_num}
        return render(request,'items-detail.html',context=context)

@login_required
def buy_items(request):
    if request.method == 'POST':
        num = request.POST['num']
        sid = request.POST['sid']
        if num == "None":  #余额不足
            context = {"link":"/shop/item/"+sid+'/',"error_name":"库存不足","error_name2":"库存不足","error_name3":"库存不足，请联系管理员"}
            return render(request,'page-error.html',context) #引入
        try:
            num = int(num)
        except:
            context = {"link": "/shop/item/" + sid + '/', "error_name": "错误", "error_name2": "数量错误",
                       "error_name3": "数量错误，请重试！"}
            return render(request, 'page-error.html', context)  # 引入
        if num<0:
            raise Http404("错了！")
        try:
            software = Software.objects.get(software_id=sid)
        except:
            raise Http404("错了！找不到sid！")
        user = request.user
        user = get_proxy_account(username=user.username)
        if user == False:
            return HttpResponse("出现错误！报告错误号：1000。\n 你可能登陆了多个账户或管理员账户，请登出后再操作！")
        #生成本账号折扣

        all_codes = Time_code.objects.filter(software=software, used=False)
        if num > all_codes.count():
            context = {"link": "/shop/item/" + sid + '/', "error_name": "余卡不足", "error_name2": "余卡不足",
                       "error_name3": "余卡不足，请重试！"}
            return render(request, 'page-error.html', context)  # 引入

        discount = Decimal(1 - (user[1].level * 0.05))

        cost = software.software_cost * num * discount  # 生成此次提卡价格
        singlecost = software.software_cost * discount
        count = user[1].balance - (cost)  # 减了以后得余额
        if count < 0: #余额错误，返回错误页面
            context = {"link":"/shop/item/"+sid+'/',"error_name":"余额不足","error_name2":"余额不足","error_name3":"您的余额为："+str(user[1].balance)}
            return render(request,'page-error.html',context)
        user[1].balance -= cost #扣钱
        user[1].save() #保存

        #创建交易
        deal_record = Deal_record.objects.create(deal_code=get_deal_code(),acount=user[0],money=cost,symbol=False,notes="提卡-"+str(software.software_name)+"_数量："+str(num))
        deal_record.save()#保存

        all_up_proxy = get_my_up_proxy(user)  # 获取所有上级代理的账号对象
        # 结算出最顶级上级的价格，减去本用户的价格，获取需要分配的金额
        if all_up_proxy != False:
            highest_proxy = all_up_proxy[-1]
            dirty_money = cost - (software.software_cost * num * Decimal(1 - (highest_proxy[1].level * 0.05)))  # 生成中间差价

            # 进入多层代理账号循环
            for i in range(len(all_up_proxy)):
                if i == 0:  # 如果匹配到是第0个号，就是本账号的直属上级代理。将他与本账号的cost价格相减，得出它的利润
                    cost_up = software.software_cost * num * Decimal(
                        1 - (all_up_proxy[i][1].level * 0.05))  # 生成本次循环账号的代理价格
                    sub_money = cost - cost_up  # 获得这层代理的中间差价
                    # 生成订单
                    up_deal_record = Deal_record.objects.create(deal_code=get_deal_code(5), acount=all_up_proxy[i][0],
                                                                money=sub_money, symbol=True,
                                                                notes="下级代理提卡的提成：" + "%.2f" % sub_money)
                    up_deal_record.save()
                    # 完成加钱
                    all_up_proxy[i][1].balance += sub_money
                    all_up_proxy[i][1].save()
                else:
                    sub_money = cost_up - (software.software_cost * num * Decimal(
                        1 - (all_up_proxy[i][1].level * 0.05)))  # 获得这层代理的中间差价
                    cost_up = software.software_cost * num * Decimal(
                        1 - (all_up_proxy[i][1].level * 0.05))  # 生成本次循环账号的代理价格，以供下次循环使用。
                    # 生成订单
                    up_deal_record = Deal_record.objects.create(deal_code=get_deal_code(5), acount=all_up_proxy[i][0],
                                                                money=sub_money, symbol=True,
                                                                notes="下级代理提卡的提成：" + "%.2f" % sub_money)
                    up_deal_record.save()
                    # 完成加钱
                    all_up_proxy[i][1].balance += sub_money
                    all_up_proxy[i][1].save()

		
        #获取所有没用过的卡

        #提取卡。
        for i in range(num):
            code = all_codes[i]
            code.proxy_man = user[0]
            code.used = True
            code.cost = singlecost
            code.deal_object = deal_record
            code.save()

        return redirect("check_deal",deal_code=deal_record.deal_code)

@login_required
def check_deal(request,deal_code):
        deal_record = Deal_record.objects.get(deal_code=deal_code)
        if deal_record.acount != request.user:
            return redirect("index")
        codes_list = Time_code.objects.filter(deal_object=deal_record)
        context = {"codes_list":codes_list,"deal_record":deal_record}
        return render(request,'table-datatable.html',context=context)


@login_required
def check_all_deal(request):
    all_deal = Deal_record.objects.filter(acount=request.user).order_by("time")
    all_deal = all_deal.reverse()
    context = {"all_deal":all_deal}
    return render(request,"page-deal.html",context)

@login_required
def check_all_down_deal(request):
    down_account_list = Others_info.objects.filter(up_proxy=request.user.id)
    deal_list = []
    for i in down_account_list:
        all_deal = Deal_record.objects.filter(acount=i.user).order_by("time")
        all_deal = all_deal.reverse()
        deal_list.append(all_deal)
    context = {"deal_list":deal_list}
    return render(request,"page-deal.html",context)

@login_required
def profile_setting(request):
    if request.method == 'GET':
        others_info = Others_info.objects.get(user=request.user)
        context = {"others_info":others_info}
        return render(request,"profile.html",context)
    elif request.method == 'POST':
        opw = request.POST['opw']
        pw = request.POST['pw']
        pwa = request.POST['pwa']
        qq = request.POST['qq']
        ad = request.POST['ad']
        if request.user.email != qq:
            request.user.email = qq
            request.user.save()
            context = {"success": "修改成功！"}
        others_info = Others_info.objects.get(user=request.user)
        if others_info.ad != ad:
            others_info.ad = ad
            others_info.save()
            context = {"success":"修改成功！"}
        try:
            context["others_info"] = others_info
        except:
            context = {"others_info": others_info}
        if opw != '' or pw != '' or pwa != '':
            user = authenticate(username=request.user.username, password=opw)
            if user != None:
                if user.is_active:
                    if pw == pwa:
                        if pw == '' or pwa == '':
                            context['warn'] = "请输入新密码！"
                            return render(request, 'profile.html', context)
                        user.set_password(pw)
                        user.save()
                        context['success'] = "修改成功！"
                        return redirect("login")
                    else:
                        context['warn'] = "新密码输入两次错误！请重试"
                        return render(request,'profile.html',context)
                else:
                    context['warn'] = "密码输入错误！请重试！"
                    return render(request,'profile.html',context)
            else:
                context['warn'] = "密码输入错误！请重试！"
                return render(request, 'profile.html', context)
        else:
            return render(request, 'profile.html', context)


@login_required
def check_all_auth(request):
    context = {}
    try:  #查找授权
        auths = Authorization.objects.filter(proxy_man=request.user).order_by('id')
        auths_list =[]
        auths = auths.reverse()
        for i in auths:
            a = {"software":i.software,"customer_QQ":i.customer_QQ,"bot_QQ":i.bot_QQ,"begin_time":i.begin_time,"deadline_time":i.deadline_time,"pk":i.pk}
            auths_list.append(a)
            if i.deadline_time < timezone.now():
                a["auths_state"] = False
            else:
                a["auths_state"] = True
        context["auths_list"] = auths_list
    except:
        pass

    return render(request,'page-auth.html',context)

@login_required
def check_auth(request,pk):
    if request.method == "GET":
        context = {"pk":pk}
        try:
            auth = Authorization.objects.get(pk=pk)
            if auth.proxy_man != request.user:
                return Http404("此授权不属于此账户！")
            context["auth"] = auth
            return render(request,'auth-detail.html',context=context)
        except Authorization.DoesNotExist:
            raise Http404("未找到！错误！")

    elif request.method == "POST":
        context ={"pk":pk}
        qq = request.POST['qq']
        try:
            qq = int(qq)
        except ValueError:
            context['warn'] = "QQ不正确"
            try:
                auth = Authorization.objects.get(pk=pk)
                if auth.proxy_man != request.user:
                    raise Http404("此授权不属于此账户！")

            except Authorization.DoesNotExist:
                raise Http404("找不到！错误！")
            context['auth'] = auth
            return render(request,"auth-detail.html", context = context)

        try:
            auth = Authorization.objects.get(pk=pk)
        except Authorization.DoesNotExist:
            raise Http404("找不到！错误！")
        if auth.proxy_man != request.user:
            raise Http404("此授权不属于此账户！")
        try:
            Authorization.objects.get(bot_QQ=qq, software=auth.software)
            context['auth'] = auth
            context['warn'] = "新的机器人QQ已经存在，请尝试其他Q号或联系管理员"
        except Authorization.DoesNotExist:
            if auth.bot_QQ != qq:
                auth.bot_QQ = qq
                auth.save()
                context['success'] = "机器人QQ修改成功！"
        context['auth'] = auth
        return render(request, 'auth-detail.html', context=context)


@login_required
def check_all_down_proxy(request): #查看所有下级代理
    user_id = request.user.id
    all_proxy_list = Others_info.objects.filter(up_proxy=user_id)
    context = {"all_proxy_list":all_proxy_list}
    return render(request,'proxy_list.html',context=context)



@login_required
def change_down_proxy_info(request,pk):
    if request.method == 'GET':
        user_id = request.user.id
        try:
            down_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404("干你")

        #检查是否是下级代理。
        down_user = get_proxy_account(username=down_user.username)
        if down_user[1].up_proxy != int(user_id):
            raise Http404("想干啥？")
        else:
            context = {"down_user_object":down_user[0],"down_user_others":down_user[1]}
            return render(request,'down_proxy_detail.html',context)
    elif request.method == "POST":
        user_id = request.user.id
        user = get_proxy_account(pk_id=user_id)
        try:
            down_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404("干你")
        # 检查是否是下级代理。
        down_user = get_proxy_account(username=down_user.username)
        if down_user[1].up_proxy != int(user_id):
            raise Http404("想干啥？")
        context = {"down_user_object": down_user[0], "down_user_others": down_user[1]}
        level = request.POST['level']
        qq = request.POST['qq']
        if level == '' or qq == '':
            context['warn'] = "修改失败！不可以清除信息！"
            return render(request, 'down_proxy_detail.html', context)

        try:
            level = int(level)
        except:
            context['warn'] = "请输入正确的等级！（例如：1）"
            return render(request,'down_proxy_detail.html',context)

        if level <= 0:
            context['warn'] = "请输入大于0的等级！（例如：1）"
            return render(request, 'down_proxy_detail.html', context)

        if level >= user[1].level:
            context['warn'] = "请输入小于的自身！（例如：1）"
            return render(request, 'down_proxy_detail.html', context)

        if level != down_user[1].level:
            down_user[1].level = level
            down_user[1].save()
            context["success"] = "等级修改成功！"

        if qq != down_user[0].email:
            down_user[0].email = qq
            down_user[0].save()
            context['success'] = 'QQ号修改成功！'

        if "pw" in request.POST and "pwa" in request.POST:
            pw = request.POST['pw']
            pwa = request.POST['pwa']
            if pw != '' and pwa != '':
                if pw == pwa:
                    down_user[0].set_password(pw)
                    down_user[0].save()

                    context['success'] = "密码修改成功！"
                    return render(request,"down_proxy_detail.html",context)
                else:
                    context['warn'] = "新密码输入两次错误！请重试"
                    return render(request, 'down_proxy_detail.html', context)
            else:
                if pw != '' or pwa != '':
                    context['warn'] = "请输入新密码!"
                    return render(request, 'down_proxy_detail.html', context)
                else:
                    return render(request, 'down_proxy_detail.html', context)
        else:
            return render(request,'down_proxy_detail.html',context)


@login_required
def create_new_down_account(request):
    if request.method == "GET":
        user = get_proxy_account(username=request.user.username)
        level = str(user[1].level - 1)
        context = {"level":level}
        return render(request,"add_down_proxy.html",context)
    elif request.method == "POST":
        user = get_proxy_account(username=request.user.username)
        context = {"level":str(user[1].level - 1)}
        if "proxy_username" in request.POST:
            proxy_username = request.POST['proxy_username']
            try:
                User.objects.get_by_natural_key(username=proxy_username)
                context['warn'] = "用户名已存在，请重试！"
                return render(request, 'add_down_proxy.html', context)
            except User.DoesNotExist:
                pass

        else:
            return render(request, 'add_down_proxy.html', context)

        if "pw" in request.POST and "pwa" in request.POST:
            pw = request.POST['pw']
            pwa = request.POST['pwa']
            if pw != pwa:
                context['warn'] = "密码二次验证输入错误！请重试"
                return render(request, 'add_down_proxy.html', context)
            elif pw == '' or pwa == '':
                context['warn'] = "请输入密码！请重试"
                return render(request, 'add_down_proxy.html', context)
        else:#错误提示
            context['warn'] = "请输入密码！请重试"
            return render(request, 'add_down_proxy.html', context)
        if "qq" in request.POST:
            qq = request.POST['qq']
            if qq == '':
                context['warn'] = "请输入QQ号！请重试"
                return render(request, 'add_down_proxy.html', context)
        else:
            context['warn'] = "请输入QQ号！请重试"
            return render(request, 'add_down_proxy.html', context)
        if "level" in request.POST:
            down_level = request.POST['level']
            try:
                down_level = int(down_level)
            except:
                context['warn'] = "请输入正确的等级！（例如：1）"
                return render(request, 'add_down_proxy.html', context)
            if down_level <= 0:
                context['warn'] = "请输入正确的等级！（例如：1）"
                return render(request, 'add_down_proxy.html', context)
            elif down_level >= user[1].level:
                context['warn'] = "请输入小于自身账户的等级！"
                return render(request, 'add_down_proxy.html', context)
        else:
            context['warn'] = "请输入新账号的等级！请重试"
            return render(request, 'add_down_proxy.html', context)
        down_user = User.objects.create_user(username=proxy_username,password=pw,email=qq)
        down_user.save()
        down_user_others = Others_info.objects.create(user=down_user,TOKEN=get_TOKEN(),level=down_level,up_proxy=user[0].id)
        down_user_others.save()
        return redirect("change_down_proxy_info",down_user.id)

@login_required
def get_money(request):
    if request.method == "GET":
        user = get_proxy_account(username=request.user.username)
        context = {"balance":user[1].balance}
        return render(request,"getmoney.html",context)

    elif request.method == "POST":
        user = get_proxy_account(username=request.user.username)
        context = {"balance":user[1].balance}
        money = request.POST['money']
        money_account_kind = request.POST['money_account_kind']
        money_account_num = request.POST['money_account_num']
        money_account_name = request.POST['money_account_name']
        if money == '' or money_account_num == '' or money_account_name == '' or money_account_kind == '':
            context["warn"] = "请输入完整信息！"
            return render(request,"getmoney.html",context)

        try:
            money = Decimal(money)
        except decimal.InvalidOperation:
            context["warn"] = "请输入正确的提款金额"
            return render(request,"getmoney.html",context)

        if user[1].balance - money < 0:
            context['warn'] = "账户余额不足！请重试！"
            return render(request,"getmoney.html",context)

        #开始扣费
        user[1].balance -= money
        user[1].save()
        #创建订单
        deal_record = Deal_record.objects.create(deal_code=get_deal_code(5),acount=user[0],money=money,symbol=False,notes="网页提现操作")
        deal_record.save()

        #创建提现单
        get_money_object = Getmoney.objects.create(proxy_account=user[0],money=money,money_account_name=money_account_kind,money_account_num=money_account_num,account_name=money_account_name)
        get_money_object.save()
        return redirect("check_all_deal")


@login_required
def transfer(request):
    if request.method == "GET":
        user = get_proxy_account(username=request.user.username)
        down_account_list = Others_info.objects.all()
        context = {"down_account_list":down_account_list,"balance":user[1].balance}
        return render(request,"transfer.html",context)

    elif request.method == "POST":
        user=get_proxy_account(username=request.user.username)
        down_account_list = Others_info.objects.all()
        context = {"down_account_list":down_account_list,"balance":user[1].balance}
        money = request.POST['money']
        account = request.POST['account']
        if money == '' or account == '':
            context['warn'] = "请输入转账信息！"
            return render(request,"transfer.html",context)

        if account == '0':
            return render(request,'transfer.html',context)

        try:
            money = Decimal(money)
        except:
            context['warn'] = "请输入正确的金额"
            return render(request, 'transfer.html', context)
        if money <= 0:
            context['warn'] = "请输入正确的金额"
            return render(request, 'transfer.html', context)

        if user[1].balance - money < 0:
            context['warn'] = "你的余额不足，请重新尝试！"
            return render(request, 'transfer.html', context)

        account = int(account)
        target_account = get_proxy_account(pk_id=account)
        if target_account == False:
            context['warn'] = "账号错误！请重新尝试！"
            return render(request, 'transfer.html', context)
        #开始扣款
        user[1].balance -= money
        user[1].save()

        #转出者创建订单
        my_deal_record = Deal_record.objects.create(deal_code=get_deal_code(5),acount=user[0],money=money,symbol=False,notes="网页转账-转出")
        my_deal_record.save()

        #转入者收款
        target_account[1].balance += money #收款
        target_account[1].save()

        target_deal_record = Deal_record.objects.create(deal_code=get_deal_code(5),acount=target_account[0],money=money,notes="网页转账-转入")
        target_deal_record.save()

        context['success'] = "成功转账！收款账号：" + target_account[0].username + "  金额：%.2f" % money
        context['balance'] = user[1].balance
        return render(request,'transfer.html',context)



