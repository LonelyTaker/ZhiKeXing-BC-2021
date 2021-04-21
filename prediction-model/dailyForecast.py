# 数据科学
import pandas as pd
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
import pymysql
# 画图相关
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.family']='SimHei' # 中文乱码
plt.rcParams['axes.unicode_minus']=False # 负号无法正常显示
# 忽略警告
import warnings
warnings.filterwarnings('ignore')
# 回归模型
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression  # 一元线性回归模型
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge  # 岭回归
from sklearn.linear_model import Lasso
# 集成算法
from xgboost import XGBRegressor 
from catboost import CatBoostRegressor 
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor 
# 模型评估
from sklearn.metrics import r2_score
import datetime

#给定开始时间和结束时间，返回日期列表
def getBetweenDay(begin_date,end_date):
    date_list = []
    begin_date = datetime.datetime.strptime(begin_date, "%Y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    while begin_date <= end_date:
        date_str = begin_date.strftime("%Y-%m-%d")
        date_list.append(date_str)
        delta = datetime.timedelta(days=1)
        begin_date += delta
    return date_list

#读取数据
#连接数据库
db_pymysql = pymysql.connect(host='localhost',port=3306,user='root',passwd='root',db='zhikexing',use_unicode=True, charset="utf8")
#db_pymysql = pymysql.connect(host='localhost',port=3306,user='root',passwd='susu1010',db='subway_schema',use_unicode=True, charset="utf8")

print("开始获取数据")
#获取天气信息
weather = pd.read_sql('select w_date AS date,w_value,w_top_temp_value,w_bot_temp_value from weather',con=db_pymysql)
weather['date']=pd.to_datetime(weather['date'], format='%Y-%m-%d')
#获取节假日信息
workdays = pd.read_sql('select w_date AS date,w_type from holidays',con=db_pymysql)
workdays['date']=pd.to_datetime(workdays['date'], format='%Y-%m-%d')
#将date设置为索引
workdays.set_index('date', inplace=True)
weather.set_index('date', inplace=True)

# df_total = pd.DataFrame(columns=['sta_name', 'in_best_r2', 'in_best_reg', 'out_best_r2', 'out_best_reg'])

# 获取车站列表
# station_list=pd.read_sql('select s_sta_name from stations',con=db_pymysql)
# station_list.set_index('s_sta_name', inplace=True)
for sta in range(1,169):
# for station in list(station_list.index):
    station = 'Sta'+str(sta)
    print("站点："+station)
    #获取客流量
    df_in=pd.read_sql('SELECT  p_date AS date, p_flow_in AS flow FROM pflow_in WHERE p_sta_name = "'+station+'" AND DATE(p_date) = "2020-05-01"',con=db_pymysql)
    df_out=pd.read_sql('SELECT  p_date AS date, p_flow_out AS flow FROM pflow_out WHERE p_sta_name = "'+station+'" AND DATE(p_date) = "2020-05-01"',con=db_pymysql)
    date_list=getBetweenDay("2020-05-02","2020-06-30")
    for date in date_list:
        sql='SELECT  p_date AS date, p_flow_in AS flow FROM pflow_in WHERE p_sta_name = "'+station+'" AND DATE(p_date) = "'+date+'"'
        temp = pd.read_sql(sql,con=db_pymysql)
        df_in=df_in.append(temp, ignore_index=True)
        
        sql='SELECT  p_date AS date, p_flow_out AS flow FROM pflow_out  WHERE p_sta_name = "'+station+'" AND DATE(p_date) = "'+date+'"'
        temp = pd.read_sql(sql,con=db_pymysql)
        df_out=df_out.append(temp, ignore_index=True)
    #获得该站点所在区域等级、人口密度
    #area_info=pd.read_sql('select a_level,a_popf,a_popi from area_level where a_name=(select s_area from stations where s_sta_name="Sta40")',con=db_pymysql)
    #a_level=area_info.iat[0,0]
    #a_popf=area_info.iat[0,1]
    #a_popi=area_info.iat[0,2]

    df_in.set_index('date', inplace=True)
    df_out.set_index('date', inplace=True)
    #合并
    df_in = df_in.join(workdays)
    df_in = df_in.join(weather)
    df_out = df_out.join(workdays)
    df_out = df_out.join(weather)
    #重置索引
    df_in = df_in.reset_index()
    df_out = df_out.reset_index()
    #类型转换（非常重要）
    df_in['date']=pd.to_datetime(df_in['date'], format='%Y-%m-%d')
    df_in['flow']=df_in['flow'].astype('float')
    df_out['date']=pd.to_datetime(df_out['date'], format='%Y-%m-%d')
    df_out['flow']=df_out['flow'].astype('float')
    
   
    #特征值构造
    #客流量衡量标准改为/区域等级
    #df['flow_relative']=df['flow']/a_level
    #df['pre_date_flow_relative'] = df.loc[:,['flow_relative']].shift(1)
    #df['MA2_relative'] = df['pre_date_flow_relative'].rolling(2).mean()
    #df['MA7_relative'] =df['pre_date_flow_relative'].rolling(7).mean()
    #增加人口密度
    #df['a_popf']=a_popf
    #df['a_popi']=a_popi
    #增加区域等级
    #df['a_level']=a_level
    #增加月份
    #df['month'] = df['date'].map(lambda x: x.month)
    #增加前一天的数据
    df_in['pre_date_flow'] = df_in.loc[:,['flow']].shift(1)
    df_out['pre_date_flow'] = df_out.loc[:,['flow']].shift(1)
    #增加前7日的平均客流
    df_in['MA7'] =df_in['pre_date_flow'].rolling(7).mean()
    df_out['MA7'] =df_out['pre_date_flow'].rolling(7).mean()
    #增加前2日的平均客流
    df_in['MA2'] = df_in['pre_date_flow'].rolling(2).mean()
    df_out['MA2'] = df_out['pre_date_flow'].rolling(2).mean()
    #增加上周同一天的客流
    #df['week1'] = df.loc[:,['flow']].shift(7)
    #增加上上周同一天的客流
    #df['week2'] = df.loc[:,['flow']].shift(14)
    #增加上上上周同一天的客流
    df_in['week3'] = df_in.loc[:,['flow']].shift(21)
    df_in.index = range(df_in.shape[0])
    df_out['week3'] = df_out.loc[:,['flow']].shift(21)
    df_out.index = range(df_out.shape[0])
    #删除缺失值
    df_in.dropna(inplace=True)
    df_out.dropna(inplace=True)
    
    #模型搭建
    #构建特征值X 和目标值 Y 
    X_in = df_in[['week3',
                  'w_value',
                  'w_top_temp_value',
                  # 'w_bot_temp_value',
                  'w_type',
                   'MA2',
                   'MA7',
                  'pre_date_flow']]
    y_in = df_in['flow']
    X_in.index = range(X_in.shape[0])
    
    X_out = df_out[['week3',
                    'w_value',
                    'w_top_temp_value',
                    # 'w_bot_temp_value',
                    'w_type',
                    'MA2',
                    'MA7',
                    'pre_date_flow']]
    y_out = df_out['flow']
    X_out.index = range(X_out.shape[0])

    # 绘制客流量统计图
    # df_in.plot(x = 'date', y = 'flow', grid = True)
    # df_out.plot(x = 'date', y = 'flow', grid = True)
    
    # 绘制特征变量热力图
# =============================================================================
#     feature = df_in.drop(['flow', 'w_bot_temp_value'],axis=1)
#     corr = feature.corr()
#     plt.figure(figsize=(10,6))
#     ax = sns.heatmap(corr, xticklabels=corr.columns,
#                      yticklabels=corr.columns, linewidths=0.2, cmap="RdYlGn",annot=True)
#     plt.title("Correlation between variables")
# =============================================================================

    
    #划分训练集和测试集
    X_in_length = X_in.shape[0]
    split_in = int(X_in_length*0.8)
    X_in_train, X_in_test = X_in[:split_in], X_in[split_in:]
    y_in_train, y_in_test = y_in[:split_in], y_in[split_in:]
    
    X_out_length = X_out.shape[0]
    split_out = int(X_out_length*0.8)
    X_out_train, X_out_test = X_out[:split_out], X_out[split_out:]
    y_out_train, y_out_test = y_out[:split_out], y_out[split_out:]
    
    in_best_reg=Lasso()
    in_best_r2=-100
    out_best_reg=Lasso()
    out_best_r2=-100
    
    #回归算法
    in_Regressors=[["Random Forest",RandomForestRegressor( 
                                                    n_estimators=50,
                                                    random_state=10,
                                                    # max_depth=11,
                                                    bootstrap=True,
                                                    oob_score=True)]
                ,["Decision Tree",DecisionTreeRegressor()]
                ,["Lasso",Lasso()]
                ,["AdaBoostRegressor", AdaBoostRegressor()]
                ,["GradientBoostingRegressor", GradientBoostingRegressor()]
                ,["XGB", XGBRegressor()]
                ,["CatBoost", CatBoostRegressor(logging_level='Silent')]  
                ,["LogisticRegression",LogisticRegression()]
                ,["LinearRegression",LinearRegression()]
                ,["Ridge",Ridge()]
                ]
    out_Regressors=[["Random Forest",RandomForestRegressor( 
                                                    n_estimators=50,
                                                    random_state=10,
                                                    # max_depth=11,
                                                    bootstrap=True,
                                                    oob_score=True)]
                ,["Decision Tree",DecisionTreeRegressor()]
                ,["Lasso",Lasso()]
                ,["AdaBoostRegressor", AdaBoostRegressor()]
                ,["GradientBoostingRegressor", GradientBoostingRegressor()]
                ,["XGB", XGBRegressor()]
                ,["CatBoost", CatBoostRegressor(logging_level='Silent')]  
                ,["LogisticRegression",LogisticRegression()]
                ,["LinearRegression",LinearRegression()]
                ,["Ridge",Ridge()]
                ]
    for name,reg in in_Regressors:
        in_reg = reg.fit(X_in_train, y_in_train)
        y_in_pred=in_reg.predict(X_in_test)
        #计算拟合
        in_r2= r2_score(y_in_test,y_in_pred)
        if in_r2>in_best_r2:
            in_best_reg=in_reg
            in_best_r2=in_r2
    for name,reg in out_Regressors:
        out_reg = reg.fit(X_out_train, y_out_train)
        y_out_pred=out_reg.predict(X_out_test)
        out_r2=r2_score(y_out_test,y_out_pred)
        if out_r2>out_best_r2:
            out_best_reg=out_reg
            out_best_r2=out_r2
        
    print("进站", "拟合度", str(in_best_r2), "最优模型", in_best_reg)
    print("出站", "拟合度", str(out_best_r2), "最优模型", out_best_reg)
         
    # '''网格搜索自动调参'''
    # from sklearn.model_selection import GridSearchCV # 网格搜索 用于自动调参
    # from sklearn.model_selection import StratifiedKFold # 交叉验证
    # from sklearn.ensemble import GradientBoostingClassifier
    # param_grid_forest = [
    #     {'n_estimators':[20, 50, 70, 80, 100], 'max_features':[3,5, 6, 7]}, 
    #     {'bootstrap':['Flase'], 'n_estimators':[20, 50, 100], 'max_features':[3, 5, 6, 7]}]
         
    '''进站模型预测'''
    # 自动调参
# =============================================================================
#     in_best_reg = RandomForestRegressor(
#         # max_features=6,
#         n_estimators=50,
#         random_state=1,
#         # max_depth=11,
#         bootstrap=True,
#         oob_score=True)
# =============================================================================
# =============================================================================
#     gs_forest_in = GridSearchCV(in_best_reg, param_grid_forest, cv = 5, 
#                                 scoring = 'neg_mean_squared_error')
#     gs_forest_in.fit(X_in_train, y_in_train)
#     print(gs_forest_in.best_params_)
# =============================================================================
    # 预测
    in_best_reg = in_best_reg.fit(X_in_train, y_in_train)
    y_in_pred = in_best_reg.predict(X_in_test)
    # 结果可视化
    plt.figure(figsize=(9,5))
    #plt.title(str(station)+'进站预测结果图')
    plt.plot(y_in_test.ravel(),label='真实值')
    plt.plot(y_in_pred,label='预测值')
    plt.xticks([])
    plt.legend()
    plt.show()
    
    '''出站模型预测'''
    # 自动调参
# =============================================================================
#     out_best_reg = RandomForestRegressor(
#         max_features=7,
#         n_estimators=100)
# =============================================================================
# =============================================================================
#     gs_forest_out = GridSearchCV(out_best_reg, param_grid_forest, cv = 5, 
#                                 scoring = 'neg_mean_squared_error')
#     gs_forest_out.fit(X_in_train, y_in_train)
#     print(gs_forest_out.best_params_)
# =============================================================================
    # 预测
    out_best_reg = out_best_reg.fit(X_out_train, y_out_train)
    y_out_pred = out_best_reg.predict(X_out_test)
    # 结果可视化
    plt.figure(figsize=(9,5))
    #plt.title(str(station)+'出站预测结果图')
    plt.plot(y_out_test.ravel(),label='真实值')
    plt.plot(y_out_pred,label='预测值')
    plt.xticks([])
    plt.legend()
    plt.show()
    
    # 存储每个站点拟合度到df
    # df_total.loc[sta] = [station, in_best_r2, in_best_reg, out_best_r2, out_best_reg]
    
    #开始预测
    forecast_date_list=getBetweenDay("2020-07-01","2020-07-07")
    for el_date in forecast_date_list:
        temp_date=(datetime.datetime.strptime(el_date, "%Y-%m-%d")-datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        start_date=(datetime.datetime.strptime(el_date, "%Y-%m-%d")-datetime.timedelta(days=6)).strftime("%Y-%m-%d")
        end_date=(datetime.datetime.strptime(el_date, "%Y-%m-%d")-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        
        el_in_flow =pd.read_sql('SELECT  p_date AS date, p_flow_in AS flow FROM pflow_in WHERE p_sta_name = "'+station+'" AND DATE(p_date) = "'+temp_date+'"',con=db_pymysql)
        el_out_flow =pd.read_sql('SELECT  p_date AS date, p_flow_out AS flow FROM pflow_out WHERE p_sta_name = "'+station+'" AND DATE(p_date) = "'+temp_date+'"',con=db_pymysql)
        
        for date in getBetweenDay(start_date,end_date):
            sql='SELECT  p_date AS date, p_flow_in AS flow FROM pflow_in WHERE p_sta_name = "'+station+'" AND DATE(p_date) = "'+date+'"'
            temp = pd.read_sql(sql,con=db_pymysql)
            el_in_flow=el_in_flow.append(temp, ignore_index=True)
            
            sql='SELECT  p_date AS date, p_flow_out AS flow FROM pflow_out WHERE p_sta_name = "'+station+'" AND DATE(p_date) = "'+date+'"'
            temp = pd.read_sql(sql,con=db_pymysql)
            el_out_flow=el_out_flow.append(temp, ignore_index=True)
            
        el_in_flow['date']=pd.to_datetime(el_in_flow['date'], format='%Y-%m-%d')
        el_out_flow['date']=pd.to_datetime(el_out_flow['date'], format='%Y-%m-%d')
        #日期类型
        el_type=workdays.loc[el_date,'w_type']
        #客流量
        pre_date_flow_in_sum=0
        pre_date_flow_out_sum=0
        for i in range(1,8):
            pre_date=(datetime.datetime.strptime(el_date, "%Y-%m-%d")-datetime.timedelta(days=i)).strftime("%Y-%m-%d")
            
            pre_date_flow_in=el_in_flow.loc[el_in_flow['date']==pre_date]
            pre_date_flow_in.set_index('date', inplace=True)
            pre_date_flow_in=pre_date_flow_in.loc[pre_date,'flow']
            pre_date_flow_in_sum += pre_date_flow_in
            
            pre_date_flow_out=el_out_flow.loc[el_out_flow['date']==pre_date]
            pre_date_flow_out.set_index('date', inplace=True)
            pre_date_flow_out=pre_date_flow_out.loc[pre_date,'flow']
            pre_date_flow_out_sum += pre_date_flow_out
            if i == 1:
                el_pre_date_flow_in=pre_date_flow_in_sum    #前一天客流
                el_pre_date_flow_out=pre_date_flow_out_sum
            elif i == 2:
                el_MA2_in=pre_date_flow_in_sum/2    #前2天平均客流
                el_MA2_out=pre_date_flow_out_sum/2
            elif i == 7:
                el_MA7_in=pre_date_flow_in_sum/7    #前7天平均客流
                el_MA7_out=pre_date_flow_out_sum/7
                
        #天气因子
        el_w_value=weather.loc[el_date,'w_value']
        el_w_top_temp=weather.loc[el_date,'w_top_temp_value']
        #上上上周同一天的客流
        el_week3_datetime = datetime.datetime.strptime(el_date, "%Y-%m-%d")-datetime.timedelta(days=21)
        
        el_week3_in=df_in.loc[df_in['date']==el_week3_datetime]
        el_week3_in.set_index('date', inplace=True)
        el_week3_in=el_week3_in.loc[el_week3_datetime,'flow']
        
        el_week3_out=df_out.loc[df_out['date']==el_week3_datetime]
        el_week3_out.set_index('date', inplace=True)
        el_week3_out=el_week3_out.loc[el_week3_datetime,'flow']

        el_in= pd.DataFrame({'week3':[el_week3_in],
                          'w_value':[el_w_value],
                          'w_top_temp_value':[el_w_top_temp],
                          'w_type':[el_type],
                          'MA2':[el_MA7_in],
                          'MA7':[el_MA2_in],
                          'pre_date_flow':[el_pre_date_flow_in]
                          })
        
        el_out= pd.DataFrame({'week3':[el_week3_out],
                          'w_value':[el_w_value],
                          'w_top_temp_value':[el_w_top_temp],
                          'w_type':[el_type],
                          'MA2':[el_MA7_out],
                          'MA7':[el_MA2_out],
                          'pre_date_flow':[el_pre_date_flow_out]
                          })
        #进行预测
        in_test = in_best_reg.predict(el_in)
        out_test=out_best_reg.predict(el_out)
        
        print(station+"站点预测"+str(el_date)+"日进站客流为"+str(int(in_test[0]))+";出站客流为"+str(int(out_test[0])))
        
        cs=db_pymysql.cursor() #创建cursor对象
        query = 'update pflow_in set p_flow_in = '+str(int(in_test[0]))+' where p_sta_name = "'+station+'" AND DATE(p_date) = "'+el_date+'"'
        cs.execute(query)
        db_pymysql.commit() #提交操作
        query = 'update pflow_out set p_flow_out = '+str(int(out_test[0]))+' where p_sta_name = "'+station+'" AND DATE(p_date) = "'+el_date+'"'
        cs.execute(query)
        db_pymysql.commit()
        query = 'INSERT INTO forecast_daily VALUES("'+station+'","'+el_date+'", '+str(int(in_test[0]))+', '+str(int(out_test[0]))+', '+'0.8'+')'
        cs.execute(query)
        db_pymysql.commit()
        cs.close() #关闭cursor对象
        
#关闭数据库连接
db_pymysql.close()