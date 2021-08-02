import csv
import pandas as pd

def csv_etl(datapath):
    with open(datapath, newline='') as csvfile:
        rows = csv.reader(csvfile, delimiter=',')
        headers = next(rows)
        with open('/home/ubuntu/output.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
        for row in rows:
            a = float(row[0])*1000000
            a = int(a)
            row[0] = a
            with open('/home/ubuntu/output.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(row)

def pd_etl(output_data):
    df = pd.read_csv(output_data)
    UNIX = df['frame.time_epoch'].apply(str).apply(lambda x:x[:10]).tolist()
    usec = df['frame.time_epoch'].apply(str).apply(lambda x:x[10:]).tolist()
    UNIX2 = pd.to_datetime(UNIX, unit='s',utc=True).tz_convert('Asia/Shanghai')
    date_dict = {"year": UNIX2.year,"month": UNIX2.month,"day": UNIX2.day,
                "hour": UNIX2.hour,"minute": UNIX2.minute,"second": UNIX2.second,"usec": usec}
    date_dict = pd.DataFrame(date_dict)
    date_dict['date'] = pd.to_datetime(date_dict[['year', 'month', 'day']])
    date_dict["hour"] = date_dict["hour"].astype(str)
    date_dict["minute"] = date_dict["minute"].astype(str)
    date_dict["second"] = date_dict["second"].astype(str)
    date_dict["time"] = date_dict["hour"] + ":" + date_dict["minute"] + ":" + date_dict["second"]
    date_dict = date_dict.drop(["year", "month", "day", "hour","minute", "second"], axis=1)
    res = pd.concat([date_dict,df],axis=1,ignore_index=True).rename(columns={0:'usec',1:'date',2:'time',3:'frame.time_epoch',4:'SourceIP',5:'SourcePort',6:'DestinationIP',7:'DestinationPort',8:'FQDN'})
    res = res.drop(["frame.time_epoch"], axis=1).reindex(columns=['date','time','usec','SourceIP','SourcePort','DestinationIP','DestinationPort','FQDN'])
    return res