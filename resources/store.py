import pymysql
from sqlalchemy import create_engine

def create_database(host,user,passwd,schema):
    db = pymysql.connect(host=host,user=user,passwd=passwd)
    cursor = db.cursor()
    SCHEMA = """CREATE SCHEMA `{}` DEFAULT CHARACTER SET utf8 ;""".format(schema)
    cursor.execute(SCHEMA)
    db.close()

def create_table(host,user,passwd,schema,table):
    db = pymysql.connect(host=host,user=user,passwd=passwd)
    cursor = db.cursor()
    TABLE = """CREATE TABLE `{}`.`{}` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `Date` date NULL,
            `Time` time NULL,
            `usec` VARCHAR(45) NULL,
            `SourceIP` VARCHAR(45) NULL,
            `SourcePort` INT(11) NULL,
            `DestinationIP` VARCHAR(45) NULL,
            `DestinationPort` INT(11) NULL,
            `FQDN` text NULL,
            PRIMARY KEY (`id`))
            ENGINE = InnoDB
            DEFAULT CHARACTER SET = utf8;""".format(schema,table)
    cursor.execute(TABLE)
    db.close()

def data_to_mysql(user,passwd,host,port,schema,df,table):
    engine = create_engine("mysql+pymysql://{}:{}@{}/{}?charset={}"
    .format(user, passwd, host +':'+ port, schema,'utf8'))
    
    con = engine.connect()
    df.to_sql(name=table, con=con, if_exists='append', index=False)