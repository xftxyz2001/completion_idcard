""" 
    身份证号补全实现
"""
import time
import threading
import re
import psutil
import os
thread = 48



data = '51068*2000*6*4****'
# sex option supports：male、female、any
sex = 'male'



def check_id_data(n):
        if len(str(n)) != 18:
            return False

        global sex
        if sex == 'any':
            pass
        elif sex == 'male':
            if int(n[16]) % 2 == 0:
                return False
        else:
            if int(n[16]) % 2 != 0:
                return False

        var=[7,9,10,5,8,4,2,1,6,3,7,9,10,5,8,4,2]
        var_id=['1','0','x','9','8','7','6','5','4','3','2']
        n = str(n)
        sum = 0
        for i in range(0,17):
            sum += int(n[i])*var[i]
        sum %= 11
        if (var_id[sum])==str(n[17]):
             return True
        else:
             return False

        
disable_memory = False
def Memory_Get():
    while True:
        if disable_memory:
            break
        memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        print('>>> 正在将数据集加载到内存，已使用(MB)：', memory, end='\r')



of_year = {
    '01' : [x for x in range(1, 32)],
    '02' : [x for x in range(1, 29)],
    '03' : [x for x in range(1, 32)],
    '04' : [x for x in range(1, 31)],
    '05' : [x for x in range(1, 32)],
    '06' : [x for x in range(1, 31)],
    '07' : [x for x in range(1, 32)],
    '08' : [x for x in range(1, 32)],
    '09' : [x for x in range(1, 31)],
    '10' : [x for x in range(1, 32)],
    '11' : [x for x in range(1, 31)],
    '12' : [x for x in range(1, 32)]
}
# 如果第几天是个位数，前面补0
for k, v in of_year.items():
    for i in range(len(v)):
        if v[i] < 10:
            v[i] = '0' + str(v[i])

if len(data) != 18:
     print(len(data))
     print('>>> 请输入18位身份证号，补全位置用*代替')
     exit()

count = data.count('*')
if count > 18:
    print('>>> 补全数不能超过18位')
    exit()

if count == 0:
    print('>>> 没有补全位置')
    exit()



# 解析出身份证号
city = data[0:6]
year = data[6:10]
month = data[10:12]
day = data[12:14]
tail = data[14:18]


print('>>> 城市代码：', city)
print('>>> 出生年份：', year)
print('>>> 出生月份：', month)
print('>>> 出生日期：', day)
print('>>> 顺序号：', tail)

city_of = None
with open('citycodes.txt',mode='r',encoding='utf-8') as f:
    city_of = f.read().split('\n')

city_run = []
city_replace = city.replace('*','(\d)')
for i in city_of:
    if re.match(city_replace, i):
        city_run.append(i)
if len(city_run) == 0:
    print('>>> 错误：城市代码错误')
    exit()


print('>>> 补全城市代码列表：', city_run)


# 处理年份
year_run = []
if year == '****':
    year_run = [x for x in range(1949, time.localtime().tm_year+1)]
else:
    year_replace = year.replace('*','(\d)')
    for i in range(1949, time.localtime().tm_year+1):
        if re.match(year_replace, str(i)):
            year_run.append(i)

print('>>> 补全年份列表：', year_run)


if month == '00':
    print('>>> 错误：月份错误')
    exit()

month_run = []
# 判断month补全的范围
if month == '**':
    month_run = [x for x in range(1, 13)]
    for i in range(len(month_run)):
        if month_run[i] < 10:
            month_run[i] = '0' + str(month_run[i])

else:
    if month[0] == '*' and month[1] != '*':
        #   判断month[1]是多少
        if int(month[1]) == 1:
            month_run = ['01','11']
        elif int(month[1]) == 2:
            month_run = ['02','12']
        elif int(month[1]) == 3:
            month_run = ['03']
        elif int(month[1]) == 4:
            month_run = ['04']
        elif int(month[1]) == 5:
            month_run = ['05']
        elif int(month[1]) == 6:
            month_run = ['06']
        elif int(month[1]) == 7:
            month_run = ['07']
        elif int(month[1]) == 8:
            month_run = ['08']
        elif int(month[1]) == 9:
            month_run = ['09']
        else:
            month_run = ['10']
    elif month[0] != '*' and month[1] == '*':
        # 只能是1或者0
        if int(month[0]) == 1:
            month_run = ['10','11','12']
        elif int(month[0]) == 0:
            month_run = ['01','02','03','04','05','06','07','08','09']
        else:
            print('>>> 错误：月份错误')
            exit()
    else:
        month_run = [month]

    
print('>>> 补全月份列表：', month_run)
# exit()
day_run = {}

# 基于month_run补全day_run
for i in month_run:
    if day == '**':
        day_run[str(i)] = of_year[str(i)]
    else:
        if day[0] == '*' and day[1] != '*':
            # 判断day[1]是多少
            if int(day[1]) == 1:
                day_run[str(i)] = ['01','11','21']
            elif int(day[1]) == 2:
                day_run[str(i)] = ['02','12','22']
            elif int(day[1]) == 3:
                day_run[str(i)] = ['03','13','23']
            elif int(day[1]) == 4:
                day_run[str(i)] = ['04','14','24']
            elif int(day[1]) == 5:
                day_run[str(i)] = ['05','15','25']
            elif int(day[1]) == 6:
                day_run[str(i)] = ['06','16','26']
            elif int(day[1]) == 7:
                day_run[str(i)] = ['07','17','27']
            elif int(day[1]) == 8:
                day_run[str(i)] = ['08','18','28']
            elif int(day[1]) == 9:
                day_run[str(i)] = ['09','19','29']
            else:
                day_run[str(i)] = ['10','20','30']
        elif day[0] != '*' and day[1] == '*':
            if int(day[0]) == 1:
                day_run[str(i)] = ['10','11','12','13','14','15','16','17','18','19']
            elif int(day[0]) == 0:
                day_run[str(i)] = ['01','02','03','04','05','06','07','08','09']
            elif int(day[0]) == 2:
                day_run[str(i)] = ['20','21','22','23','24','25','26','27','28','29']
            elif int(day[0]) == 3:
                day_run[str(i)] = ['30','31']
            else:
                print('>>> 错误：日期错误')
                exit()
        else:
            day_run[str(i)] = [day]

# for i in day_run:
#     # 判断闰年
#     if int(year) % 4 == 0 and int(year) % 100 != 0 or int(year) % 400 == 0:
#         if i == '02':
#             if '29' not in day_run[i]:
#                 day_run[i].append('29')
#     else:
#         if i == '02':
#             if '29' in day_run[i]:
#                 day_run[i].remove('29')





print('>>> 补全日期列表：', day_run)


# 最后4位补全
tail_run = []
if tail == '****':
    tail_run = [x for x in range(10000)]
    for i in range(len(tail_run)):
        if tail_run[i] < 10:
            tail_run[i] = '000' + str(tail_run[i])
        elif tail_run[i] < 100:
            tail_run[i] = '00' + str(tail_run[i])
        elif tail_run[i] < 1000:
            tail_run[i] = '0' + str(tail_run[i])
else:
    if tail.count('*') == 0:
        tail_run = [tail]
    else:
        # 对*进行替换，0-9

        # 1个*
        if tail.count('*') == 1:
            for i in range(10):
                tail_run.append(tail.replace('*', str(i)))
        # 2个*
        elif tail.count('*') == 2:
            for i in range(10):
                for j in range(10):
                    tail_run.append(tail.replace('*', str(i), 1).replace('*', str(j)))
        # 3个*
        elif tail.count('*') == 3:
            for i in range(10):
                for j in range(10):
                    for k in range(10):
                        tail_run.append(tail.replace('*', str(i), 1).replace('*', str(j), 1).replace('*', str(k)))
        else:
            print('>>> 错误：后4位错误')
            exit()
    

# print('>>> 补全顺序号列表：', tail_run)


# 计算出所有的可能性
# all_run = []
# for i in month_run:
#     for j in day_run[str(i)]:
#         for k in tail_run:
#             # all_run.append(year + i + j + k)
#             all_run.append(str(year) + str(i) + str(j) + str(k))

threading.Thread(target=Memory_Get).start()


all_run = []
for i in city_run:
    for j in year_run:
        for k in month_run:
            for l in day_run[str(k)]:
                for m in tail_run:
                    # all_run.append(year + i + j + k)
                    all_run.append(str(i) + str(j) + str(k) + str(l) + str(m))
                    # print(str(i) + str(j) + str(k) + str(l) + str(m))



disable_memory = True
time.sleep(1)
os.system('cls')
disable_memory = False
# print('>>> 计算出所有的可能性：', len(all_run))
all_in = len(all_run)
print('>>> 数据集：', all_in)
lock = threading.Lock()
index = []
cache = []

def split_and_verify(array,index_index):
    global index
    global cache
    for i in array:
        index[index_index] += 1


        real = str(i)

        if check_id_data(real):
            cache[index_index].append(real)
            # print('>>> 正确：', real)
    # print('子线程：', threading.current_thread().name, '完成')
        
        # print('

    pass

def list_split(items, n):
    return [items[i:i+n] for i in range(0, len(items), n)]

print('>>> 数据集分割：', thread + 1 , '\n>>> 正在分割，请等待加载完成\n')
threading.Thread(target=Memory_Get).start()

# 对数据进行分割为10份
data_split = list_split(all_run, all_in//thread)
start = time.time()
for i in range(thread):
    index.append(0)
    cache.append([])
    t = threading.Thread(target=split_and_verify, args=(data_split[i],i))
    t.start()

# 清理内存
all_run = []
time.sleep(1)

disable_memory = True
time.sleep(1)

os.system('cls')
while True:
    if threading.active_count() == 1:
        print('>>> 所有线程完成')
        print('>>> 耗时：', time.time() - start)

        # 将结果写入文件
        r = []
        for i in cache:
            r += i
        result = "\n".join(r)
        with open('id.txt', 'a') as f:
            f.write(result)


        break
    else:
        time.sleep(0.5)
        total = 0
        for i in index:
            total += i
        print('pass：' + str(total) + '/' + str(all_in) + '  ' + str(round(total/all_in*100, 2)) + '%', end='\r')