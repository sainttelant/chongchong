
# coding: utf-8

# In[1]:

import numpy as np
import pandas as pd
import time,datetime
import matplotlib.pyplot as plt

#读取Citi Bike的数据并创建数据表
cb=pd.DataFrame(pd.read_csv('C:\\Users\\Administrator\\Downloads\\JC-201703-citibike-tripdata.csv'))
#查看有多大的csv数据
cb.shape
#唯一的租赁点数量统计
len(cb['Start Station ID'].unique())
#唯一自行车ID
len(cb['Bike ID'].unique())
#租赁次数
cb['Start Station ID'].count()
#平均每辆车使用的频率
cb['Start Station ID'].count()/cb['Start Station ID'].count()
#平均每辆车每日使用的频率
cb['Start Station ID'].count()/cb['Start Station ID'].count()/31
#每次租借平均时长(分钟)
cb['Trip Duration'].sum()/cb['Bike ID'].count()/60

#按用户性别进行汇总并计算不同性别的占比
user_gender=cb.groupby('Gender')['Bike ID'].agg(len)/cb["Bike ID"].count()*100
#汇总用户性别占比饼图
plt.rc('font', family='STXihei', size=15)
colors = ["#052B6C","#39A2E3","#EA1F29"]
name=['未知', '男性', '女性']
plt.pie(user_gender,labels=name,colors=colors,explode=(0, 0, 0),startangle=60,autopct='%1.1f%%')
plt.title('Citi Bike用户性别占比')
plt.legend(['未知', '男性', '女性'], loc='lower right')
plt.show()

#查看出生日期的范围
cb['Birth Year'].min(),cb['Birth Year'].max()

#使用2017年与用户出生日期计算年龄
cb['age']=2017-cb['Birth Year']
#用户最小。最大年龄
cb['age'].min(),cb['age'].max()
#对用户年龄进行分组
bins = [0, 18, 30, 50,150]
group_age = ['少年', '青年', '中年', '老年']
cb['group_age'] = pd.cut(cb['age'], bins, labels=group_age)
#按年龄分组对数据进行汇总
user_age=cb.groupby('group_age')['group_age'].agg(len)
#生成用户年龄分布柱状图
plt.rc('font', family='STXihei', size=15)
a=np.array([1,2,3,4])
plt.bar([1,2,3,4],user_age,color='#052B6C',alpha=0.8,align='center',edgecolor='white')
plt.xlabel('年龄分组')
plt.ylabel('租赁次数')
plt.title('Citi Bike用户年龄分布')
plt.legend(['次数'], loc='upper right')
plt.grid(color='#95a5a6',linestyle='--', linewidth=1,axis='y',alpha=0.4)
plt.xticks(a,('少年','青年','中年','老年'))
plt.show()

#按用户的会员类别进行汇总并计算占比
user_type=cb.groupby('User Type')['Bike ID'].agg(len)/cb["Bike ID"].count()*100
#汇总用户会员类别饼图
plt.rc('font', family='STXihei', size=15)
colors = ["#EA1F29","#39A2E1"]
name=['Customer', 'Subscriber']
plt.pie(user_type,labels=name,colors=colors,explode=(0,0),startangle=43,autopct='%1.1f%%')
plt.title('Citi Bike用户类别占比')
plt.legend(['Customer', 'Subscriber'], loc='upper left')
plt.show()

#骑行距离与年龄是否存在关联？
#计算并增加年龄字段
cb['age']=2017-cb['Birth Year']
#提取年龄和骑行速度字段
age_speed=cb[['Trip Duration','age']]
#去除骑行速度为0的数据
age_speed=age_speed.dropna()
#年龄设置为自变量X
X = np.array(age_speed[['age']])
#距离设置为因变量Y
Y = np.array(age_speed[['Trip Duration']])
 
#导入线性回归库,用线性预测
from sklearn import linear_model
#将数据导入模型
clf = linear_model.LinearRegression()
clf.fit (X,Y)
#计算相关度
clf.score(X,Y)
#斜率
clf.coef_

#截距
clf.intercept_
 
#那么得到的回归方程就是 骑行duration= 斜率*最大年龄-截距

#重头戏，进行不同年龄骑行duration的预测
#20岁的骑行duration预测
clf.predict(20)

#获得骑行开始和结束地点及经纬度数据
end_station=pd.pivot_table(cb,index=["Start Station Name","Start Station Latitude","Start Station Longitude","End Station Latitude","End Station Longitude","End Station Name"],values=['Bike ID'],aggfunc=[len],fill_value=0,margins=True).head(10)

