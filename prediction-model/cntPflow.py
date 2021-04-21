import pymysql
import datetime

# 连接DB
db = pymysql.connect(host='localhost',port=3306,user='root',passwd='susu1010',db='subway_schema',use_unicode=True, charset="utf8")
print("Connecting...")
# 得到一个可以执行SQL语句的光标对象
cursor = db.cursor()

# 统计小时进站客流量
def cntHourFlowIn():
    begin = datetime.date(2019,12,26)
    end = datetime.date(2020,7,16)
    d = begin
    delta = datetime.timedelta(days=1)
    while d <= end:
        for sta in range(1, 169):
            sta_name = 'Sta' + str(sta)
            print("cntHourFlowOut", sta_name, d)
            # 统计小时出站客流量
            cursor.execute("INSERT INTO cnthourflow_in(c_sta_in, c_date_in, c_hour_in, c_pflow_in) \
                           SELECT t_sta_in, DATE(t_time_in), HOUR(t_time_in), COUNT(*) \
                           FROM trips \
                           WHERE t_sta_in = '%s' AND DATE(t_time_in) = '%s' \
                           GROUP BY HOUR(t_time_in) \
                           ORDER BY HOUR(t_time_in)" % (sta_name, d))
            # 将以小时为单位的客流统计表中无客流的日期记录填充为0
            for h in range(6, 24):
                isFull = cursor.execute("SELECT CONCAT(c_sta_in,c_date_in,c_hour_in,c_pflow_in)\
                                   FROM cnthourflow_in\
                                   WHERE c_sta_in = '%s' AND c_date_in = '%s' AND c_hour_in = '%s'" % (sta_name, d, h))
                if(isFull == 0):
                    cursor.execute("INSERT INTO cnthourflow_in VALUES('%s', '%s', '%s', 0)" % (sta_name, d, h))
        d += delta
    print(" cntHourFlowOut Done")  
    
# 统计小时出站客流量
def cntHourFlowOut():
    begin = datetime.date(2019,12,26)
    end = datetime.date(2020,7,16)
    d = begin
    delta = datetime.timedelta(days=1)
    while d <= end:
        for sta in range(1, 169):
            sta_name = 'Sta' + str(sta)
            print("cntHourFlowOut", sta_name, d)
            # 统计小时出站客流量
            cursor.execute("INSERT INTO cnthourflow_out(c_sta_out, c_date_out, c_hour_out, c_pflow_out) \
                           SELECT t_sta_out, DATE(t_time_out), HOUR(t_time_out), COUNT(*) \
                           FROM trips \
                           WHERE t_sta_out = '%s' AND DATE(t_time_out) = '%s' \
                           GROUP BY HOUR(t_time_out) \
                           ORDER BY HOUR(t_time_out)" % (sta_name, d))
            # 将以小时为单位的客流统计表中无客流的日期记录填充为0
            for h in range(6, 24):
                isFull = cursor.execute("SELECT CONCAT(c_sta_out,c_date_out,c_hour_out,c_pflow_out)\
                                   FROM cnthourflow_out\
                                   WHERE c_sta_out = '%s' AND c_date_out = '%s' AND c_hour_out = '%s'" % (sta_name, d, h))
                if(isFull == 0):
                    cursor.execute("INSERT INTO cnthourflow_out VALUES('%s', '%s', '%s', 0)" % (sta_name, d, h))
        d += delta
    print(" cntHourFlowOut Done")    

def cntDailyFlowIn():
    for sta in range(1, 169):
        sta_name = 'Sta' + str(sta)
        # 统计
        print("Calculating pflow_in", sta_name)
        cursor.execute("INSERT INTO pflow_in(p_date, p_sta_name, p_flow_in) \
                       SELECT DATE(t_time_in) AS p_date, t_sta_in AS p_sta_name, COUNT(*) AS p_flow_in \
                       FROM trips \
                       WHERE t_sta_in = '%s' \
                       GROUP BY DATE(t_time_in) \
                       ORDER BY DATE(t_time_in)" % (sta_name))
        begin = datetime.date(2019,12,26)
        end = datetime.date(2020,7,16)
        d = begin
        delta = datetime.timedelta(days=1)
        while d <= end:
            # 填充客流量为0的记录
            print("insertZero in", sta_name, d)
            isFull = cursor.execute("SELECT CONCAT(p_date,p_sta_name,p_flow_in)\
                           FROM pflow_in\
                           WHERE p_date = '%s' AND p_sta_name = '%s'" % (d, sta_name))
            if(isFull == 0):
                cursor.execute("INSERT INTO pflow_in VALUES('%s', '%s', 0)" % (d, sta_name))
            d += delta
    print("cntDailyFlowIn Done") 

def cntDailyFlowOut():
    for sta in range(1, 169):
        sta_name = 'Sta' + str(sta)
        # 统计每天出站客流量
        print("Calculating pflow_out", sta_name)
        cursor.execute("INSERT INTO pflow_out(p_date, p_sta_name, p_flow_out) \
                       SELECT DATE(t_time_out) AS p_date, t_sta_out AS p_sta_name, COUNT(*) AS p_flow_out \
                       FROM trips \
                       WHERE t_sta_out = '%s' \
                   GROUP BY DATE(t_time_out) \
                   ORDER BY DATE(t_time_out)" % (sta_name))
        begin = datetime.date(2019,12,26)
        end = datetime.date(2020,7,16)
        d = begin
        delta = datetime.timedelta(days=1)
        while d <= end:
            # 填充客流量为0的记录
            print("insertZero out", sta_name)
            isFull = cursor.execute("SELECT CONCAT(p_date,p_sta_name,p_flow_out)\
                           FROM pflow_out\
                           WHERE p_date = '%s' AND p_sta_name = '%s'" % (d, sta_name))
            if(isFull == 0):
                cursor.execute("INSERT INTO pflow_out VALUES('%s', '%s', 0)" % (d, sta_name))
            d += delta
    print("cntDailyFlowOut Done") 

# 调用函数
# 统计各站点小时客流量
# 执行统计函数前请先确保对应表同站点同日期无记录
cntHourFlowIn()
# cntHourFlowOut()

# 统计各站点每天客流量
# 执行统计函数前请先确保对应表同站点同日期无记录
# cntDailyFlowIn()
# cntDailyFlowOut()


# 提交
db.commit()

# 关闭光标对象
cursor.close()
# 关闭DB
db.close()
print("DB closed")