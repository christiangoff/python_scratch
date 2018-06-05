import csv
import os
from datetime import datetime

os.chdir('C://Users//ChristianGoff//Downloads')
print(os.getcwd())

report = open('module_exception_report (60).csv','rt')
reader = csv.reader(report)
rownumber = 0
data = []
for row in reader:
    if rownumber == 0:
        header = row
    else:
        data.append(row)
    rownumber += 1
    
report.close()

for i in range(0, len(header)):
    print( '%s: %s' % (str(i),header[i]))

def get_stores(data):
    stores = {}
    for tm in data:
        location = tm[8]
        if not location in stores:
            stores[location]=1
        elif location != '':
            stores[location]+=1
    print(stores)
    return stores    
        
def get_completions(data):
    stores = {}
    for tm in data:
        location = tm[8]
        completion = tm[29]
        if completion == 'Yes':
            comp_count = 1
        else:
            comp_count = 0
        if not location in stores:
            stores[location]=[1,comp_count]
        elif location != '':
            stores[location][0]+=1
            stores[location][1]+=comp_count
    return(stores)

def get_completion_data(data):
    comps = get_completions(data)
    for i in comps.keys():
        print('%s: %s%%' % (i,int((comps[i][1])/(comps[i][0])*100)))


def get_overdue(data, start_date, end_date):
    stores = {}
    for tm in data:
        location = tm[header.index('Location')]
        if tm[header.index('Completed')] == 'Yes':
            due_date = tm[header.index('Due Date')]
            due_datetime = datetime.strptime(due_date, "%m/%d/%Y")
            comp_date = tm[header.index('Completed Date')]
            comp_datetime = datetime.strptime(comp_date, "%m/%d/%Y")
            day_diff = comp_datetime - due_datetime
            if day_diff.days > 0 and due_date >= start_date and due_date <= end_date:
                overdue = True
                in_date_range = True
            elif day_diff.days <= 0 and due_date >= start_date and due_date <= end_date:
                overdue = False
                in_date_range = True
            else:
                overdue = False
                in_date_range = False
        elif tm[header.index('Due Date')] == 'N/A':
            overdue = False
            in_date_range = False
        else:
            due_date = tm[header.index('Due Date')]
            due_datetime = datetime.strptime(due_date, "%m/%d/%Y")
            if due_date > start_date:
                overdue = True
                in_date_range = True
            else:
                overdue = False
                in_date_range = False
        if not location in stores:
            stores[location] = [in_date_range, overdue]
        else:
            stores[location][0] += in_date_range
            stores[location][1] += overdue
    return stores

def get_overdue_data(data, start_date, end_date):
    stores = get_overdue(data, start_date, end_date)
    for i in stores.keys():
        if stores[i][0] == 0:
            print(i,"N/A")
        else:
            print(i, int((stores[i][0] - stores[i][1])/stores[i][0]*100))
    
def get_all(data, start_date, end_date):
    comps = get_completions(data)
    overdue = get_overdue(data, start_date, end_date)
    headers = [['Store', 'Completion', 'Overdue']]
    results  = []
    for i in comps.keys():
        if overdue[i][0] == 0:
            overdue_data='N/A'
        else:
            overdue_data = ((overdue[i][0] - overdue[i][1])/overdue[i][0])
        results.append([i, ((comps[i][1])/(comps[i][0])), overdue_data])
    file = open('results.csv','w')
    with file:
        write = csv.writer(file, lineterminator='\n')
        write.writerows(headers+results)
    file.close()
    return results



                        
