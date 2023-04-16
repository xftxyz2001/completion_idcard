# 大陆身份证号补全工具

该项目目前只支持补全后8位，如果补全前12位，那么数量级将会是指数级别的，除此之外，如果补全后12位，那么参考意义也不大，谁会连年份都不知道就去补全呢？

如果有这个需求，后续会加上。

## 算法及原理

### 第一步
我对身份证号每一个部分进行了拆分，如下代码
```py
city = data[0:6] # 城市
year = data[6:10] # 年份
month = data[10:12] # 月份
day = data[12:14] # 日期
tail = data[14:18] # 校验码
```

## 第二步
我对月份进行了枚举

### 2.1

首先判断是否月份都是`**`，如果是，则代表1-12月份都需要补全。
如代码所示。
```py
if month == '**':
    month_run = [x for x in range(1, 13)]
    for i in range(len(month_run)):
        if month_run[i] < 10:
            month_run[i] = '0' + str(month_run[i])
```
输出结果为
```
01 02 03 ... 10 11 12
```

### 2.2
如果第一个是``*``，第二个是具体数字，那么就进行对第二位数进行判断：

可能出现的月份：
- 1：01、11
- 2：02、12
- 3：03、13
- 4：04、14
- 其他：10

    ....
- 9：09

### 2.3
如果第二个数是``*``，第一个数是具体数字，进行如下判断：

可能出现的月份：
- 1：10、11、12
- 0：01、02、03、04、05、06、07、08、09
- 其他：报错

### 2.4
这就是最理想情况，不需要补全，直接就是结果。代码如下
```py
month_run = [month]
```

## 第三步

通过上面枚举出来的可能出现的月份，来枚举日期。

### 3.1
如果两位数都是``**``，那么就是全年365天，直接for循环全年进去就行了。
```py
for i in month_run:
    if day == '**':
        day_run[str(i)] = of_year[str(i)]
```


### 3.2
步骤和处理月份时原理相同，举出可能出现的月份


### 3.3
这就是最理想情况，直接告诉你日期
```py
day_run[str(i)] = [day]
```


### 第四步
现在需要判断是否是闰年，对于2月份的枚举日期进行处理。

```py
for i in day_run:
    # 判断闰年
    if int(year) % 4 == 0 and int(year) % 100 != 0 or int(year) % 400 == 0:
        if i == '02':
            if '29' not in day_run[i]:
                day_run[i].append('29')
    else:
        if i == '02':
            if '29' in day_run[i]:
                day_run[i].remove('29')

```
上述代码我对需要枚举的月份进行了遍历，如果是闰年，且2月份没有29号，则添加，反之删除


### 第五步
对于后4位校验码的处理
```py
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

```
原理不再阐述


### 第六步
创建线程来处理即可



## 任务耗时统计
以下内容均使用15线程来处理。


后8位：14.1046秒

后7位：在1-9月耗时10.7488秒，10-12月耗时3.8160秒

后6位：耗时1.5676秒

后5位：耗时0.8796秒

后4位：耗时0.0419秒

后3位及以后：小于0.010秒

## 开发过程中遇到的问题以及经验总结
1、

问题：最开始我使用单线程来跑，跑后8位用时64秒，CPU利用率100%

解决方法：我使用threading来创建了多线程跑，后8位用时40秒

2、

问题：通过上述解决方法后，时间提升了20秒左右，但是CPU利用率很高，速度不理想。

解决方法：通过研究发现，导致速度慢，CPU利用率高的问题，根本原因是在验证成功后直接写入文件，导致IO利用很高，所以我将验证成功的写入到了缓存中，待所有线程验证完成后统一写入文件。使用该方法解决后，后8位耗时14秒，CPU（i5-10400f）利用率16%.

## 郑重提示
请勿将 本项目 应用到任何可能会违反法律规定和道德约束的工作中，请友善使用 本项目，不要将 本项目 用于任何非法用途。如您选择使用 本项目 即代表您遵守此协议，作者不承担任何由于您违反此协议带来任何的法律风险和损失，一切后果由您承担。

## 作者信息
QQ：3139505131

WECHAT：laravel_debug

E-Mail：wlkjyy@vip.qq.com

## 后言
参考文献：

- https://blog.csdn.net/qq_21516633/article/details/103166438
开发不易，如果本项目对你有用，让我喝杯咖啡吧。
