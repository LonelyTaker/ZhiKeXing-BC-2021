import pandas as pd
pd.set_option('display.max_columns',1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth',1000)
import pymysql
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.family']='SimHei'
plt.rcParams['axes.unicode_minus']=False
import warnings
warnings.filterwarnings('ignore')
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
# 集成算法
from xgboost import XGBRegressor 
from catboost import CatBoostRegressor 
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor  
from sklearn.metrics import r2_score
import datetime
from sklearn import preprocessing

# 给定开始时间和结束时间，返回日期列表
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

# 读取数据
# 连接数据库
db_pymysql = pymysql.connect(host='localhost',port=3306,user='root',passwd='root',db='zhikexing',use_unicode=True, charset="utf8")
# db_pymysql = pymysql.connect(host='localhost',port=3306,user='root',passwd='susu1010',db='subway_schema',use_unicode=True, charset="utf8")

# df_total = pd.DataFrame(columns=['sta_name', 'in_best_r2', 'in_best_reg', 'out_best_r2', 'out_best_reg'])

for sta in range(1,169):
    sta_name = 'Sta' + str(sta)
    print("Connecting...", sta_name)
    # 获取客流量数据（已将天气和日期类型合并）
    df_in=pd.read_sql('SELECT * \
               FROM (cnthourflow_in LEFT OUTER JOIN weather ON weather.w_date = cnthourflow_in.c_date_in) LEFT OUTER JOIN holidays ON cnthourflow_in.c_date_in = holidays.w_date\
            WHERE cnthourflow_in.c_sta_in = "%s" AND c_date_in >= "2020-03-01" AND c_date_in <= "2020-06-30" \
            ORDER BY c_date_in'%sta_name,con=db_pymysql)
    df_in.drop(columns=['c_sta_in','w_date','w_weather','w_top_temp','w_bot_temp'],inplace=True)
    df_in['c_date_in']=pd.to_datetime(df_in['c_date_in'], format='%Y-%m-%d')
    
    df_out=pd.read_sql('SELECT * \
               FROM (cnthourflow_out LEFT OUTER JOIN weather ON weather.w_date = cnthourflow_out.c_date_out) LEFT OUTER JOIN holidays ON cnthourflow_out.c_date_out = holidays.w_date\
            WHERE cnthourflow_out.c_sta_out = "%s" AND c_date_out >= "2020-03-01" AND c_date_out <= "2020-06-30" \
            ORDER BY c_date_out'%sta_name,con=db_pymysql)
    df_out.drop(columns=['c_sta_out','w_date','w_weather','w_top_temp','w_bot_temp'],inplace=True)
    df_out['c_date_out']=pd.to_datetime(df_out['c_date_out'], format='%Y-%m-%d')

    # 增加特征值
    df_in['pre_day1_flow'] = df_in.loc[:,['c_pflow_in']].shift(18)
    df_in['pre_day1_type'] = df_in.loc[:,['w_type']].shift(18)
    df_out['pre_day1_flow'] = df_out.loc[:,['c_pflow_out']].shift(18)
    df_out['pre_day1_type'] = df_out.loc[:,['w_type']].shift(18)
    
    df_in['pre_day3_flow'] = df_in.loc[:,['c_pflow_in']].shift(54)
    df_in['pre_day3_type'] = df_in.loc[:,['w_type']].shift(54)
    df_out['pre_day3_flow'] = df_out.loc[:,['c_pflow_out']].shift(54)
    df_out['pre_day3_type'] = df_out.loc[:,['w_type']].shift(54)

    df_in['week1'] = df_in.loc[:,['c_pflow_in']].shift(126)
    df_in['week2'] = df_in.loc[:,['c_pflow_in']].shift(126*2)
    df_out['week1'] = df_out.loc[:,['c_pflow_out']].shift(126)
    df_out['week2'] = df_out.loc[:,['c_pflow_out']].shift(126*2)
    # 删除缺失值
    df_in.dropna(inplace=True)
    df_out.dropna(inplace=True)

    # 归一化
    scaler = preprocessing.StandardScaler()
    
    top_temp_scale = scaler.fit(df_in['w_top_temp_value'].values.reshape(-1,1))
    df_in['w_top_temp_value'] = scaler.fit_transform(df_in['w_top_temp_value'].values.reshape(-1, 1), top_temp_scale)
    bot_temp_scale = scaler.fit(df_in['w_bot_temp_value'].values.reshape(-1,1))
    df_in['w_bot_temp_value'] = scaler.fit_transform(df_in['w_bot_temp_value'].values.reshape(-1, 1), bot_temp_scale)
    
    top_temp_scale = scaler.fit(df_out['w_top_temp_value'].values.reshape(-1,1))
    df_out['w_top_temp_value'] = scaler.fit_transform(df_out['w_top_temp_value'].values.reshape(-1, 1), top_temp_scale)
    bot_temp_scale = scaler.fit(df_out['w_bot_temp_value'].values.reshape(-1,1))
    df_out['w_bot_temp_value'] = scaler.fit_transform(df_out['w_bot_temp_value'].values.reshape(-1, 1), bot_temp_scale)
    
    week1_scale = scaler.fit(df_in['week1'].values.reshape(-1,1))
    df_in['week1'] = scaler.fit_transform(df_in['week1'].values.reshape(-1, 1), week1_scale)
    week1_scale = scaler.fit(df_out['week1'].values.reshape(-1,1))
    df_out['week1'] = scaler.fit_transform(df_out['week1'].values.reshape(-1, 1), week1_scale)
    
    week2_scale = scaler.fit(df_in['week2'].values.reshape(-1,1))
    df_in['week2'] = scaler.fit_transform(df_in['week2'].values.reshape(-1, 1), week2_scale)
    week2_scale = scaler.fit(df_out['week2'].values.reshape(-1,1))
    df_out['week2'] = scaler.fit_transform(df_out['week2'].values.reshape(-1, 1), week2_scale)
    
    w_value_scale = scaler.fit(df_in['w_value'].values.reshape(-1,1))
    df_in['w_value'] = scaler.fit_transform(df_in['w_value'].values.reshape(-1, 1), w_value_scale)
    w_value_scale = scaler.fit(df_out['w_value'].values.reshape(-1,1))
    df_out['w_value'] = scaler.fit_transform(df_out['w_value'].values.reshape(-1, 1), w_value_scale)

    w_type_scale = scaler.fit(df_in['w_type'].values.reshape(-1,1))
    df_in['w_type'] = scaler.fit_transform(df_in['w_type'].values.reshape(-1, 1), w_type_scale)
    w_type_scale = scaler.fit(df_out['w_type'].values.reshape(-1,1))
    df_out['w_type'] = scaler.fit_transform(df_out['w_type'].values.reshape(-1, 1), w_type_scale)
    
    # 模型搭建
    # 构建特征值X 和目标值 Y 
    X_in = df_in[['c_hour_in','w_value','w_top_temp_value','w_bot_temp_value','w_type',
            'week1',
            'week2',
            'pre_day1_flow','pre_day1_type','pre_day3_flow','pre_day3_type'
            ]]
    y_in = df_in['c_pflow_in']
    X_in.index = range(X_in.shape[0])
    
    X_out = df_out[['c_hour_out','w_value','w_top_temp_value','w_bot_temp_value','w_type',
            'week1',
            'week2',
            'pre_day1_flow','pre_day1_type','pre_day3_flow','pre_day3_type'
            ]]
    y_out = df_out['c_pflow_out']
    X_out.index = range(X_out.shape[0])
    
    # 绘制客流量统计图
    # df_in.plot(x = 'date', y = 'flow', grid = True)
    
    # 绘制特征变量热力图
# =============================================================================
#     feature = df_in.drop(['c_pflow_in',],axis=1)
#     corr = feature.corr()
#     plt.figure(figsize=(10,6))
#     ax = sns.heatmap(corr, xticklabels=corr.columns,
#                      yticklabels=corr.columns, linewidths=0.2, cmap="RdYlGn",annot=True)
#     plt.title("Correlation between variables")
# =============================================================================
    
    # 划分训练集和测试集
    X_in_length = X_in.shape[0]
    split_in = int(X_in_length*0.8)
    X_in_train, X_in_test = X_in[:split_in], X_in[split_in:]
    y_in_train, y_in_test = y_in[:split_in], y_in[split_in:]
    
    X_out_length = X_out.shape[0]
    split_out = int(X_out_length*0.8)
    X_out_train, X_out_test = X_out[:split_out], X_out[split_out:]
    y_out_train, y_out_test = y_out[:split_out], y_out[split_out:]
    
    best_reg_in=Lasso()
    best_r2_in=-100
    best_reg_out=Lasso()
    best_r2_out=-100
    
    # 回归算法
    in_Regressors=[["Random Forest",RandomForestRegressor(
                                n_estimators=100, # 决策树个数，越多越好，但是性能会更差
                                random_state=10, # 设置后可以固定预测结果
                                # n_jobs=1,
                                bootstrap=True, # 有放回地采样
                                max_depth=11,
                                oob_score=True
                                )]
                ,["Decision Tree",DecisionTreeRegressor()]
                ,["Lasso",Lasso()]
                ,["AdaBoostRegressor", AdaBoostRegressor()]
                ,["GradientBoostingRegressor", GradientBoostingRegressor(
                            n_estimators=350,
                            learning_rate=0.02,
                            random_state = 17        
                            )]
                ,["XGB", XGBRegressor()]
                ,["CatBoost", CatBoostRegressor(
                    iterations=450,
                    learning_rate=0.03,
                    logging_level='Silent'
                    )]  
                ,["LogisticRegression",LogisticRegression()]
                ,["LinearRegression",LinearRegression()]
                ,["Ridge",Ridge()]
                ]
    out_Regressors=[["Random Forest",RandomForestRegressor(
                                n_estimators=100, # 决策树个数，越多越好，但是性能会更差
                                random_state=10, # 设置后可以固定预测结果
                                # n_jobs=1,
                                bootstrap=True, # 有放回地采样
                                max_depth=11,
                                oob_score=True
                                )]
                ,["Decision Tree",DecisionTreeRegressor()]
                ,["Lasso",Lasso()]
                ,["AdaBoostRegressor", AdaBoostRegressor()]
                ,["GradientBoostingRegressor", GradientBoostingRegressor(
                            n_estimators=350,
                            learning_rate=0.02,
                            random_state = 17        
                            )]
                ,["XGB", XGBRegressor()]
                ,["CatBoost", CatBoostRegressor(
                    iterations=450,
                    learning_rate=0.03,
                    logging_level='Silent'
                    )]  
                ,["LogisticRegression",LogisticRegression()]
                ,["LinearRegression",LinearRegression()]
                ,["Ridge",Ridge()]
                ]

    for name,reg in in_Regressors:
        reg_in = reg.fit(X_in_train, y_in_train)
        y_in_pred=reg_in.predict(X_in_test)
        #计算拟合
        r2_in= r2_score(y_in_test,y_in_pred)
        if r2_in>best_r2_in:
            best_reg_in=reg
            best_r2_in=r2_in
            
    for name,reg in out_Regressors:
        reg_out = reg.fit(X_out_train, y_out_train)
        y_out_pred=reg_out.predict(X_out_test)
        r2_out=r2_score(y_out_test,y_out_pred)
        if r2_out>best_r2_out:
            best_reg_out=reg
            best_r2_out=r2_out

    
    best_reg_in = best_reg_in.fit(X_in_train, y_in_train)
    y_in_pred = best_reg_in.predict(X_in_test)
    best_reg_out = best_reg_out.fit(X_out_train, y_out_train)
    y_out_pred = best_reg_out.predict(X_out_test)
    
    print(sta_name+"站点")
    print("进站", "拟合度", str(best_r2_in), "最优模型", best_reg_in)
    print("出站", "拟合度", str(best_r2_out), "最优模型", best_reg_out)
    
    # 结果可视化
    # 进站
    plt.figure(figsize=(9,5))
    plt.title(sta_name+'进站预测结果图')
    plt.plot(y_in_test.ravel(),label='真实值')
    plt.plot(y_in_pred,label='预测值')
    plt.xticks([])
    plt.legend()
    plt.show()
    # 出站
    plt.figure(figsize=(9,5))
    plt.title(sta_name+'出站预测结果图')
    plt.plot(y_out_test.ravel(),label='真实值')
    plt.plot(y_out_pred,label='预测值')
    plt.xticks([])
    plt.legend()
    plt.show()
    
    # 存储每个站点拟合度到df
    # df_total.loc[sta] = [sta_name, best_r2_in, best_reg_in, best_r2_out, best_reg_out]
    
    #开始预测
    #进站
    el_in=pd.read_sql('SELECT * \
               FROM (cnthourflow_in LEFT OUTER JOIN weather ON weather.w_date = cnthourflow_in.c_date_in) LEFT OUTER JOIN holidays ON cnthourflow_in.c_date_in = holidays.w_date\
            WHERE cnthourflow_in.c_sta_in = "%s" AND c_date_in >= "2020-06-15" AND c_date_in <= "2020-07-01" \
            ORDER BY c_date_in'%sta_name,con=db_pymysql)
    el_in.drop(columns=['c_sta_in','w_date','w_weather','w_top_temp','w_bot_temp'],inplace=True)
    el_in['c_date_in']=pd.to_datetime(el_in['c_date_in'], format='%Y-%m-%d')
    
    el_in['pre_day1_flow'] = el_in.loc[:,['c_pflow_in']].shift(18)
    el_in['pre_day1_type'] = el_in.loc[:,['w_type']].shift(18)
    
    el_in['pre_day3_flow'] = el_in.loc[:,['c_pflow_in']].shift(54)
    el_in['pre_day3_type'] = el_in.loc[:,['w_type']].shift(54)

    el_in['week1'] = el_in.loc[:,['c_pflow_in']].shift(126)
    el_in['week2'] = el_in.loc[:,['c_pflow_in']].shift(126*2)
    
    top_temp_scale = scaler.fit(el_in['w_top_temp_value'].values.reshape(-1,1))
    el_in['w_top_temp_value'] = scaler.fit_transform(el_in['w_top_temp_value'].values.reshape(-1, 1), top_temp_scale)
    bot_temp_scale = scaler.fit(el_in['w_bot_temp_value'].values.reshape(-1,1))
    el_in['w_bot_temp_value'] = scaler.fit_transform(el_in['w_bot_temp_value'].values.reshape(-1, 1), bot_temp_scale)
    
    week1_scale = scaler.fit(el_in['week1'].values.reshape(-1,1))
    el_in['week1'] = scaler.fit_transform(el_in['week1'].values.reshape(-1, 1), week1_scale)
    week2_scale = scaler.fit(el_in['week2'].values.reshape(-1,1))
    el_in['week2'] = scaler.fit_transform(el_in['week2'].values.reshape(-1, 1), week2_scale)
    
    w_value_scale = scaler.fit(el_in['w_value'].values.reshape(-1,1))
    el_in['w_value'] = scaler.fit_transform(el_in['w_value'].values.reshape(-1, 1), w_value_scale)
    w_type_scale = scaler.fit(el_in['w_type'].values.reshape(-1,1))
    el_in['w_type'] = scaler.fit_transform(el_in['w_type'].values.reshape(-1, 1), w_type_scale)
    el_in.dropna(inplace=True)
    
    el_in=el_in.loc[el_in['c_date_in']=='2020-07-01']
    el_in_X=el_in[['c_hour_in','w_value','w_top_temp_value','w_bot_temp_value','w_type',
            'week1','week2',
            'pre_day1_flow','pre_day1_type','pre_day3_flow','pre_day3_type'
            ]]
    el_in_y_pred = best_reg_in.predict(el_in_X)
    
    cs=db_pymysql.cursor()
    for i in range(6,24):
        query = 'update cnthourflow_in set c_pflow_in = '+str(int(el_in_y_pred[i-6]))+' where c_sta_in = "'+sta_name+'" AND c_date_in = "2020-07-01" AND c_hour_in = '+ str(i)
        cs.execute(query)
        db_pymysql.commit() #提交操作
    cs.close() #关闭cursor对象
        
    #出站
    el_out=pd.read_sql('SELECT * \
               FROM (cnthourflow_out LEFT OUTER JOIN weather ON weather.w_date = cnthourflow_out.c_date_out) LEFT OUTER JOIN holidays ON cnthourflow_out.c_date_out = holidays.w_date\
            WHERE cnthourflow_out.c_sta_out = "%s" AND c_date_out >= "2020-06-15" AND c_date_out <= "2020-07-01" \
            ORDER BY c_date_out'%sta_name,con=db_pymysql)
    el_out.drop(columns=['c_sta_out','w_date','w_weather','w_top_temp','w_bot_temp'],inplace=True)
    el_out['c_date_out']=pd.to_datetime(el_out['c_date_out'], format='%Y-%m-%d')
    
    el_out['pre_day1_flow'] = el_out.loc[:,['c_pflow_out']].shift(18)
    el_out['pre_day1_type'] = el_out.loc[:,['w_type']].shift(18)
    
    el_out['pre_day3_flow'] = el_out.loc[:,['c_pflow_out']].shift(54)
    el_out['pre_day3_type'] = el_out.loc[:,['w_type']].shift(54)

    el_out['week1'] = el_out.loc[:,['c_pflow_out']].shift(126)
    el_out['week2'] = el_out.loc[:,['c_pflow_out']].shift(126*2)
    
    top_temp_scale = scaler.fit(el_out['w_top_temp_value'].values.reshape(-1,1))
    el_out['w_top_temp_value'] = scaler.fit_transform(el_out['w_top_temp_value'].values.reshape(-1, 1), top_temp_scale)
    bot_temp_scale = scaler.fit(el_out['w_bot_temp_value'].values.reshape(-1,1))
    el_out['w_bot_temp_value'] = scaler.fit_transform(el_out['w_bot_temp_value'].values.reshape(-1, 1), bot_temp_scale)
    
    week1_scale = scaler.fit(el_out['week1'].values.reshape(-1,1))
    el_out['week1'] = scaler.fit_transform(el_out['week1'].values.reshape(-1, 1), week1_scale)
    week2_scale = scaler.fit(el_out['week2'].values.reshape(-1,1))
    el_out['week2'] = scaler.fit_transform(el_out['week2'].values.reshape(-1, 1), week2_scale)
    
    w_value_scale = scaler.fit(el_out['w_value'].values.reshape(-1,1))
    el_out['w_value'] = scaler.fit_transform(el_out['w_value'].values.reshape(-1, 1), w_value_scale)
    w_type_scale = scaler.fit(el_out['w_type'].values.reshape(-1,1))
    el_out['w_type'] = scaler.fit_transform(el_out['w_type'].values.reshape(-1, 1), w_type_scale)
    el_out.dropna(inplace=True)
    
    el_out=el_out.loc[el_out['c_date_out']=='2020-07-01']
    el_out_X=el_out[['c_hour_out','w_value','w_top_temp_value','w_bot_temp_value','w_type',
            'week1','week2',
            'pre_day1_flow','pre_day1_type','pre_day3_flow','pre_day3_type'
            ]]
    el_out_y_pred = best_reg_out.predict(el_out_X)
    
    cs=db_pymysql.cursor()
    for i in range(6,24):
        query = 'update cnthourflow_out set c_pflow_out = '+str(int(el_out_y_pred[i-6]))+' where c_sta_out = "'+sta_name+'" AND c_date_out = "2020-07-01" AND c_hour_out = '+ str(i)
        cs.execute(query)
        db_pymysql.commit() #提交操作
    
    for i in range(6,24):
        print(str(sta_name)+"站点预测2020-07-01日"+str(i)+"时进站客流为:"+str(int(el_in_y_pred[i-6]))+";出站客流为:"+str(int(el_out_y_pred[i-6])))
        query = 'INSERT INTO forecast_hour VALUES("'+sta_name+'","'+'2020-07-01'+'", '+str(i)+', '+str(int(el_in_y_pred[i-6]))+', '+str(int(el_out_y_pred[i-6]))+')'
        cs.execute(query)
        db_pymysql.commit()
    cs.close() #关闭cursor对象
    
#关闭数据库
db_pymysql.close()