import cx_Oracle

# 连接数据库
conn = cx_Oracle.connect('NJ_CBS:p9bv0h21GMWk40Fy@10.10.105.110:1521/?service_name=NJ_SCM')

# 执行SQL语句
cursor = conn.cursor()
cursor.execute("select * from PERF_BARGADEVGEAR_INFO")
result = cursor.fetchall()

# 关闭游标和连接
cursor.close()
conn.close()
