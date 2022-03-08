# Modules Used
import time
import yaml
from _datetime import datetime
import threading

Status = 0  # 1 - Entry , 2 - Exit , 3 - Executing
taskname = ''

# Reading Yaml File
with open('/home/soma/KLA/practice/KLA MAIN HACKATHON 2022/DataSet/Milestone1/Milestone1B.yaml') as f:
    WorkFlow = yaml.load(f, Loader=yaml.FullLoader)

# Storing Work Flow Name
WorkFlowName = list(WorkFlow.keys())[0]
print(WorkFlowName)

LogLines = []

# Sleep Function
def TimeFunction(stime):
    time.sleep(stime)
    print(stime)

# Code For Exctracting Current Time
def Current_time():
    now = datetime.now()
    CurrentTime = now.strftime("%Y-%m-%d %H:%M:%S.%f")[:-1]
    return CurrentTime

# Editing String According to Conditions
def LogFile(Status, loc, fun=None):
    t = threading.Lock()
    t.acquire()
    loc = ".".join(loc.split('.')[1:])
    s = str(Current_time()) + ';'
    if (Status == 1):
        s = s + loc + ' Entry'
    elif (Status == 2):
        s = s + loc + ' Exit'
    elif (Status == 3):
        s = s + loc + ' Executing ' + fun

    LogLines.append(s)
    s = ''
    t.release()


# Function For Executing Task

def RunTask(task, key, loc):
    loc = loc + '.' + key
    if (task['Function'] == 'TimeFunction'):
        print(key)
        taskname = key
        Status = 1
        LogFile(Status, loc)
        s = task['Function'] + ' (' + task['Inputs']['FunctionInput'] + ', ' + task['Inputs']['ExecutionTime'] + ')'
        Status = 3
        LogFile(Status, loc, s)
        TimeFunction(int(task['Inputs']['ExecutionTime']))
        Status = 2
        LogFile(Status, loc)
    print(task)

# Function For Passing Work Flow
def RunFlow(flow, key, loc):
    # thread.acquire()
    loc = loc + '.' + key
    Status = 1
    LogFile(Status, loc)
    Actvty = flow['Activities']

    if flow['Execution'] == 'Sequential':
        for key in Actvty.keys():
            if Actvty[key]['Type'] == 'Task':
                RunTask(Actvty[key], key, loc)
            elif Actvty[key]['Type'] == 'Flow':
                RunFlow(Actvty[key], key, loc)
        Status = 2
        LogFile(Status, loc)

    else:
        jobs = []
        for key in Actvty.keys():
            if Actvty[key]['Type'] == 'Task':
                t = threading.Thread(target=RunTask, args=(Actvty[key], key, loc))
                # t1 = threading.Thread(target=RunTask(Actvty[key], key, loc))
                jobs.append(t)
                t.start()
            elif Actvty[key]['Type'] == 'Flow':
                t = threading.Thread(target=RunFlow, args=(Actvty[key], key, loc))
                # t1 = threading.Thread(RunFlow(Actvty[key], key, loc))
                jobs.append(t)
                t.start()
        for job in jobs:
            job.join()
        Status = 2
        LogFile(Status, loc)

# Running Function To Get Separate Work Flow
# lock = threading.Lock()
RunFlow(WorkFlow[WorkFlowName], WorkFlowName, WorkFlowName)

# For Checking Purspose
for i in LogLines:
    print(i)

#Converting Into Log File
textfile = open("log1b.txt", "w")
for element in LogLines:
    textfile.write(element + "\n")
textfile.close()