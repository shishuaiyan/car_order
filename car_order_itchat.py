# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import re, datetime, copy, os, itchat, time



MAX_ORDER_DAYS = 7
EARLIEST_HOUR = 5
LAST_HOUR = 22
oneday = datetime.timedelta(days=1)
weekday = {'一':1, '二':2, '三':3, '四':4, '五':5, '六':6, '日':7}
order_list_log_path = os.path.join(os.getcwd(), 'log')

order_date = 0#申请日期     type: class< date >
order_time_start = 0#申请开始时间   type: int
order_time_end = 0#申请结束时间    type: int
order_list = []#[[today, {1: user_id, ...}],[]...]    type: [[class<date>, {int: str, ...}],[]...]
work_hours = {}#{EARLIEST_HOUR: user_id, ..., LAST_HOUR: user_id}   type: {int: str}
user_id = ''
user_nickname = ''
user_remarkname = ''
flag_judge_order_date = False
car_order_users_Regex = re.compile(r'car_\d\d\d')
users_flag = False

for hour in range(EARLIEST_HOUR,LAST_HOUR+1):
    work_hours[hour] = 0


def get_order_date(the_day):
    global order_date
    order_date = the_day
    today = datetime.date.today()
    print('Debug fun msg 0: ',order_date, 'today:', today)
    return order_date, today


def judge_order_date(today, order_date):
    global flag_judge_order_date
    if (0 <= (order_date-today).days <= MAX_ORDER_DAYS):
        flag_judge_order_date = True
        print('Debug fun msg 1: ','less then 7 days')
    elif (order_date-today).days <= 0:
        flag_judge_order_date = False
        callback_print('预约时间错误，请重新输入')
    else:
        flag_judge_order_date = False
        callback_print('您预约的日期超过{}天，请重新输入'.format(MAX_ORDER_DAYS))
        #print('Callback msg 1: ','more then 7 days, please change the date!')


def get_order_time(user_input_time):#传入user_input后半段(周|日等之后部分)
    if flag_judge_order_date:#judge the order_date is effective
        #start_time judgement
        print('Debug fun msg: 49', order_date)
        if(len(re.search(r'\d{1,99}', user_input_time).group())<3):#开始时间小于两位数
            order_time_start = re.search(r'\d\d|\d', user_input_time).group()
            if(EARLIEST_HOUR <= int(order_time_start) <= LAST_HOUR):
                print('Debug fun msg 2', 'order_time_start: ', order_time_start)
                #end_time judgement
                input_end_temp = re.search(r'\d{1,99}[\D]*$', user_input_time)
                if(len(re.search(r'\d{1,99}', input_end_temp.group()).group())<3):#结束时间小于两位数
                    order_time_end = re.search(r'\d\d|\d', user_input_time[input_end_temp.span()[0]:]).group()
                    if(EARLIEST_HOUR <= int(order_time_end) <= LAST_HOUR):
                        print('Debug fun msg 2', 'order_time_end: ', order_time_end)
                        print('Debug fun msg order_date: ', order_date)
                        if int(order_time_start) >= int(order_time_end):
                            callback_print('时间范围错误')
                            return 1
                        new_day_fun()
                        upgrade_order_list(int(order_time_start), int(order_time_end))
                        return 0
                    else:
                        callback_print('结束时间范围错误')
                        #print('Callback msg: ', '结束时间范围错误')
                        return 1
                else:
                    callback_print('结束时间输入错误')
                    #print('Callback msg: ', '结束时间输入错误')
                    return 1
            else:
                callback_print('开始时间范围错误')
                #print('Callback msg: ', '开始时间范围错误')
                return 1
        else:
            callback_print('开始时间输入错误')
            #print('Callback msg: ', '开始时间输入错误')
            return 1
    else:
        print('Debug msg 4: ', 'order_date 不合法')
    

def init_order_list(today):
    global order_list
    if os.path.isdir(order_list_log_path) and os.path.exists(order_list_log_path+'/order_list_logs.txt'):
        print('loading order list log....')
        f = open(order_list_log_path+'/order_list_logs.txt', 'r')
        order_list = eval(f.read())
        f.close()
        print('The roder_list_logs load compele~~~')
    else:
        for i in range(MAX_ORDER_DAYS+1):
            order_list.append([today])
            order_list[i].append(copy.deepcopy(work_hours))#深拷贝
            today += oneday
        make_directory(os.getcwd(), 'log')
        write_order_list_logs()


#def upgrade_order_list(order_time_start, order_time_end):#type: (class<date>, class<date>, int, int)
#    global order_list
#    order_hours = 0
#    used_hours = 0
##    print('Debug fun msg: ', '98: ', order_list)
##    print('Debug fun msg: ', '99', order_date)
##    print('Debug fun msg: ', type(order_date))
#    for oneday_list in order_list:
#        if(oneday_list[0] == order_date):#定位至order_date
#            for thehour in range(order_time_start, order_time_end+1):
#                if(oneday_list[1][thehour]):
#                    used_hours += 1
#                    #callback_print('{}号{}点已被{}预定。发送“查询”查看未来7天预约情况'.format(str(order_date), thehour, userName2nickName(oneday_list[1][thehour])))
#                else:
#                    order_hours += 1
#            if used_hours:
#                callback_print('{}号{}点-{}点已被{}预定。发送“查询”查看未来7天预约情况'.format(str(order_date), thehour-order_hours-used_hours+1, thehour-order_hours, remarkName2nickName(oneday_list[1][thehour-order_hours-used_hours+1])))############======remarkName2nickName(oneday_list[1][thehour])
##                callback_print('{}号{}点-{}点已被{}预定。发送“查询”查看未来7天预约情况'.format(str(order_date), thehour-used_hours+1, thehour+1, remarkName2nickName(oneday_list[1][thehour-used_hours+1])))
#                used_hours = 0
#            if(order_hours == order_time_end-order_time_start+1):
#                for i in range(order_time_start, order_time_end+1):
#                    oneday_list[1][i] = user_remarkname ####################===================
#                callback_print('已预约{}日{}点到{}点用车,预定成功！'.format(str(order_date), order_time_start, order_time_end+1))
#                #print('Callback msg: ', '已预约{}日{}点到{}点用车,预定成功！'.format(str(order_date), order_time_start, order_time_end))
#                order_hours = 0
#                write_order_list_logs()
#            else:
#                pass
#                #print('Debug fun msg: ', '117')
#        else:
#            pass
#            #print('Debug fun msg: ', '119')
def upgrade_order_list(order_time_start, order_time_end):#type: (class<date>, class<date>, int, int)
    global order_list
    order_used_hours = []
    print('Debug msg: enter upgrade_order_list')
    for oneday_list in order_list:
        if(oneday_list[0] == order_date):#定位至order_date
            oneday_used_list = fun_oneday_used_list(oneday_list)
            start_end_list = start_end2list(order_time_start, order_time_end)
            for start_end_ele in start_end_list:
                if start_end_ele in oneday_used_list:
                    order_used_hours.append(start_end_ele)
            if order_used_hours:#someone is ordered in this day
                callback_print('{}号{}点已被预定。发送“查询”查看未来7天预约情况'.format(str(order_date), str(order_used_hours)))
                order_used_hours = []
            else:#no one has ordered in this day, luckily
                for i in range(order_time_start, order_time_end):
                    oneday_list[1][i] = user_remarkname
                callback_print('已预约{}日{}点到{}点用车,预定成功！'.format(str(order_date), order_time_start, order_time_end))
                write_order_list_logs()

#def clear_user_input():
#    global user_input
#    user_input = ''
#    #input写入log文件


def make_directory(path, name):
    if(os.path.isdir(path)):
        if(os.path.isdir(os.path.join(path, name))):
            print('目录已存在，请勿重复创建')
        else:
            os.mkdir(os.path.join(path, name))
        print('文件夹创建成功,路径：{}'.format(os.path.join(path, name)))
    else:
        print('路径错误')


def write_order_list_logs():
    f_order_list_log = open(order_list_log_path+'/order_list_logs.txt', 'w')
    f_order_list_log.write(str(order_list))
    f_order_list_log.close()


def callback_print(callback_str):
    #print('Callback msg: ', callback_str)
    itchat.send_msg(callback_str, user_id)
    time.sleep(0.5)

search_result = ''
def remarkName2nickName(remark_name):
    global search_result
    search_result = itchat.search_friends(name=remark_name)
    return search_result[0]['NickName']


def fun_oneday_used_list(order_list_oneday):#返回当天已被使用的小时  list
    oneday_used_list = []
    for hour in order_list_oneday[1]:#遍历一天中所有有效时间  type(hour)=int
        if(order_list_oneday[1][hour]):#当前小时有人预约
            oneday_used_list.append(hour)
    return oneday_used_list


def start_end2list(start, end):
    start_end_list = []
    for i in range(start, end):
        start_end_list.append(i)
    return start_end_list


def new_day_fun():
    global order_list
    diff_days = (datetime.date.today()-order_list[0][0]).days
    order_list_last_day = order_list[-1][0]
    if diff_days:
        for diff_day in range(diff_days):
            print('Debug msg: new_day_fun 日期更新中')
            order_list.append([order_list_last_day+datetime.timedelta(days=diff_day+1), copy.deepcopy(work_hours)])
            del order_list[0]
        write_order_list_logs()




@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def reply_msg(msg):
    global user_id, user_nickname, today, order_date, users_flag, user_remarkname
    user_id = msg['FromUserName']
    user_nickname = msg['User']['NickName']
    user_remarkname = msg['User']['RemarkName']
    today = datetime.date.today()
    user_input = msg['Content']
    print('来自"{}"的消息: {}'.format(user_nickname, user_input))
    if car_order_users_Regex.match(user_remarkname):
        users_flag = True
    else:
        users_flag = False
    
    
    if users_flag:#判断用户是否在用户列表中
        if user_input == u'你好':
            print("接收消息: ", msg['Content'])
            itchat.send_msg(msg['User']['NickName'] + "你好啊！", msg['FromUserName'])
        
        
        if(user_input.split(' ')[0] == "预约"):
            order_date_week = re.search(r'周|下周|本周', user_input)
#            order_date_tomo = re.match(r'今天|明天|后天|大后天', user_input.split(' ')[1])
            order_date_tomo = re.search(r'今天|明天|后天|大后天', user_input)
            order_date_date = re.search(r'号|日', user_input)
            
            if(order_date_week):#input mode one: 周|下周|本周
                for i in weekday:
                    if((user_input[order_date_week.span()[1]] == str(weekday[i])) or (user_input[order_date_week.span()[1]] == i)):
                        print('Debug msg 1: ',weekday[i])
                        if(order_date_week.group() in ['周','本周']):
                            print('Debug msg 2: ','this week')
                            for day in range(weekday[i]-datetime.date.isoweekday(today)):
                                today += oneday
                            order_date,today = get_order_date(today)
                            judge_order_date(today, order_date)
                            get_order_time(user_input[order_date_week.span()[1]+1:])
                            print('Debug msg 4: ', order_time_start, order_time_end)
                            break
                        elif(order_date_week.group() in ['下周']):
                            print('Debug msg 3: ','next week')
                            for day in range(weekday[i]-datetime.date.isoweekday(today)+7):
                                today += oneday
                            order_date,today = get_order_date(today)
                            judge_order_date(today, order_date)
                            get_order_time(user_input[order_date_week.span()[1]+1:])
                            break
#                    if(weekday[i] == 7):
#                        callback_print('请正确输入(mode 周)')#===================================已知bug：会同时出现“请正确输入（mode 周）”和预约成功
#                        #print('Callback msg 2: ', '请正确输入(mode 周)')
                        
            elif(order_date_tomo):#input mode two: 今天|明天|后天|大后天
                if(order_date_tomo.group() == '今天'):
                    order_date,today = get_order_date(today)
                    judge_order_date(today, order_date)
                    get_order_time(user_input[order_date_tomo.span()[1]:])
                elif(order_date_tomo.group() == '明天'):
                    today += oneday
                    order_date,today = get_order_date(today)
                    judge_order_date(today, order_date)
                    get_order_time(user_input[order_date_tomo.span()[1]:])
                elif(order_date_tomo.group() == '后天'):
                    today += datetime.timedelta(days=2)
                    order_date,today = get_order_date(today)
                    judge_order_date(today, order_date)
                    get_order_time(user_input[order_date_tomo.span()[1]:])
                elif(order_date_tomo.group() == '大后天'):
                    today += datetime.timedelta(days=3)
                    order_date,today = get_order_date(today)
                    judge_order_date(today, order_date)
                    get_order_time(user_input[order_date_tomo.span()[1]:])
                else:
                    pass
    
                
            elif(order_date_date):#input mode three: 号|日
                input_date_l = re.search(r'\d{1,2}[\D]*$', user_input[:order_date_date.span()[0]])
                if(input_date_l):
                    input_date = re.search(r'\d+',input_date_l.group())
                else:
                    callback_print('请正确输入(mode 号)')
                    #print('Callback msg 3: ', '请正确输入(mode 号)')
                print('Debug msg 4: ',input_date.group())
                if(int(input_date.group()) in [1,2,3,4,5,6,7]):
                    order_date_month = today.month+1
                    order_date = datetime.date(today.year, order_date_month, int(input_date.group()))
                    judge_order_date(today, order_date)
                    get_order_time(user_input[order_date_date.span()[1]:])
                else:
                    try:
                        order_date = datetime.date(today.year, today.month, int(input_date.group()))
                        judge_order_date(today, order_date)
                        get_order_time(user_input[order_date_date.span()[1]:])
                    except(ValueError):
                        callback_print('请输入一个合法日期')
                        #print('Callback msg 4: ', '请输入一个合法日期')
            else:
                callback_print('请正确输入')
                    
                
        elif(user_input == '取消预约'):
            cancel_str = ''
            for order_list_oneday in order_list:
                for i in order_list_oneday[1]:
                    if(order_list_oneday[1][i] == user_remarkname): #################================
                        order_list_oneday[1][i] = 0
                        cancel_str = '取消预约成功'
                    else:
                        pass
                        #print('Debug fun msg: ', '246')
            if cancel_str:
                write_order_list_logs()
                callback_print(cancel_str)
                #print('Callback msg: ', cancel_str)
            else:
                callback_print('取消预约失败，请联系管理员')
            
            
#        elif(user_input == '查询'):#用regular expression匹配用户输入
#            checkout_str = ''
#            ordered_hours = 0
#            hours_user = {}
#            for order_list_oneday in order_list:#只显示已预约部分
#                checkout_str = r'日期: {}       已预约时间：'.format(order_list_oneday[0])
#                #len_flag = len(checkout_str)
#                for hour in order_list_oneday[1]:
#                    if(order_list_oneday[1][hour]):
#                        if ordered_hours == 0:
#                            hour_temp = hour
#                        ordered_hours += 1
#                        hours_user[hour] = order_list_oneday[1][hour]
#                        #checkout_str += ' {}:{} '.format(i, userName2nickName(order_list_oneday[1][i]))#user_nickname
#                if(ordered_hours):
#                    #print('Debug msg: ', order_list_oneday[1][i], type(order_list_oneday[1][i]))
#                    for hour_user in hours_user:
#                        
#                    checkout_str += '{}点-{}点  预约人：{}'.format(hour_temp, hour_temp+ordered_hours-1, remarkName2nickName(order_list_oneday[1][i]))
#                    callback_print(checkout_str)
#                    ordered_hours = 0
#                    #print(checkout_str)
        elif(user_input == '查询'):#用regular expression匹配用户输入
            new_day_fun()
            checkout_str = ''
#            hours_user = {}#新建一个字典存放当天被预约的时间及人  dict
            none_ordered_flag = True
            for order_list_oneday in order_list:#只显示已预约部分
                checkout_str = r'日期: {}      '.format(order_list_oneday[0])
                checkout_str_len = len(checkout_str)
                #len_flag = len(checkout_str)
                user_list_index = -1
                user_list = []
                user_start_hour = 0
                user_end_hour = 0
                for hour in order_list_oneday[1]:#遍历一天中所有有效时间  type(hour)=int
                    if(order_list_oneday[1][hour]):#当前小时有人预约
                        if hour >= user_end_hour:#未添加
                            user_list.append(order_list_oneday[1][hour])
                            user_list_index += 1
                            used_hours = 0
                            while order_list_oneday[1][hour+used_hours] == user_list[user_list_index]:
                                used_hours += 1
                            user_start_hour = hour
                            user_end_hour = user_start_hour+used_hours
                            checkout_str += '{}点-{}点  预约人：{}           '.format(str(user_start_hour), str(user_end_hour), remarkName2nickName(user_list[user_list_index])) 
                        else:#已添加至user_list
                            pass
                    else:#当前小时无人预约
                        pass
#                print('Debug msg user_list: ', user_list )
                if len(checkout_str) > checkout_str_len:
                    callback_print(checkout_str)
                    none_ordered_flag = False   
            if none_ordered_flag:
                callback_print('暂无预约记录，您可以放心预约')
            
        
        elif(user_input == '帮助'):
            help_str = '''
            最大预约时间：{}天
            一天中可供预约时间：{}点至{}点
            输入“预约”+空格+日期+时间 进行车辆使用预约；实例：“预约 明天6-12”，“下周日12点到14点”，“22号18-22点”
            输入“取消预约”取消当前账号所有预约
            输入“查询”查看当前预约情况
            输入“帮助”显示当前提示
            '''.format(MAX_ORDER_DAYS, EARLIEST_HOUR, LAST_HOUR)
            callback_print(help_str)
        
        
        else:
            callback_print('未识别输入')
            #print('Callback msg: ', '未识别输入')
        
        
    
    
    












if __name__ == '__main__':
    #initation order_list and log
    init_order_list(datetime.date.today())
    
    itchat.auto_login()
#    itchat.auto_login(enableCmdQR=2)#命令行显示二维码
    itchat.run()
#    print('after itchat.run')#程序在itchat.run循环，logout后打印

    





    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
