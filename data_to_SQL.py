from resources import data_etl,store

datapath = "/home/ubuntu/data.csv"
outputdata = "/home/ubuntu/output.csv"
user = 'porter'
passwd = 'pn1234567890'
host = 'localhost'
port = '3306'
schema = 'test'
table = 'test'

data_etl.csv_etl(datapath)
df = data_etl.pd_etl(outputdata)
store.create_database(host=host,user=user,passwd=passwd,schema=schema)
store.create_table(host=host,user=user,passwd=passwd,schema=schema,table=table)
store.data_to_mysql(user=user,passwd=passwd,host=host,port=port,schema=schema,df=df,table=table)