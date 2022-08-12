import pandas as pd
import time
from datetime import datetime
from openpyxl import load_workbook
from plyer import notification
def timeto24h(t,m):
    '''
    This function will clean the time and convert it to 24 hours time.
    '''
    temp = int(t.split(':')[0])
    if m=='pm' and temp!=12:
        temp+=12
        return str(temp)+':'+str(t.split(':')[1])+':00'
    elif m=='am' and temp==12:
        return "00"+':'+str(t.split(':')[1])+':00'
    else:
        return t

if __name__ == "__main__":
    tasklist=load_workbook("mytasks.xlsx")["Sheet1"].values
    next(tasklist)
    df=pd.DataFrame(data=tasklist,columns=('time','am/pm','task','status'))
    del tasklist
    for index, row in df.iterrows():
        if row['time'] == None:
            break
        task_time=timeto24h(row['time'].strftime('%H:%M:%S'),row['am/pm'])
        curr_time=datetime.now().strftime("%H:%M:%S")
        h,m,s=task_time.split(':')
        x=h+m+s
        h,m,s=curr_time.split(':')
        y=h+m+s
        if(int(x) < int(y)):
            notification.notify(
                title=row['task'],
                message="You probably have missed a task to do: \n"+row['task'],
                app_name="Task Reminder ",
                app_icon="Schedule.ico",
                timeout=10
            )
            continue
        time_left=datetime.strptime(task_time, '%H:%M:%S') - datetime.strptime(curr_time, '%H:%M:%S')
        del curr_time
        time_left=str(time_left).split(':')

        time_left_sec=int(int(time_left[0])*3600+int(time_left[1])*60+int(time_left[2]))

        del task_time,time_left

        time.sleep(time_left_sec)
        notification.notify(
            title=row['task'],
            message="You have a task to do: \n"+row['task'],
            app_name="Task Reminder ",
            app_icon="Schedule.ico",
            timeout=7
        )
        time.sleep(1)
