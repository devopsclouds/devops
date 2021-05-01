###import Libraries
import json
import os
import requests
import datetime
import csv
import configparser
import pandas as pd
import openpyxl
import sys
import getpass
####calling app.properties file by using configparser where the bit bucket server url and auth details in app.properties file
cp= configparser.RawConfigParser()
cp.read(r"..\config\app.properties")
sys.dont_write_bytecode = True
####call the proxy function. function defined in proxy.py
#callProxy()
username = sys.argv[1]
print("Username being used for this run ::: " + username)
#token = getpass.getpass(prompt=" Please enter account-01 password: ")
password = sys.argv[2]
#repo = input("please enter repository: ")
repo = sys.argv[3]
print("Repositry being used for this run ::: " + repo)
#branch = input("please enter branch: ")
branch = sys.argv[4]
print("Branch being used for this run :::" + branch)
#st_date = input("enter a date with time(i.e YYYY:MM:DD:HH:MM: ")
st_date = sys.argv[5]
print("Date from which the records are picked ::: " + st_date)
st_dates = st_date.replace(":",",")
year, month, day,hours,mins = map(int, st_dates.split(','))

headers = {"Content-Type": 'application/json'}

auth = (username,password) 
####
b = cp.get("DEFAULT", "b")
c = cp.get("DEFAULT", "c")

### put all fields into  variable
csv_columns=['pull_request_id','title','jira_issue','createdDate','updatedDate','author','Branch_From','Branch_To','state','files','parent_directory_of_files','repository']

## To get the pull request server base url
url = cp.get("DEFAULT", "url")
#print(url)

### put the repository is parameterized.
#repo=sys.argv[1]
#repo = cp.get("DEFAULT", "repo")
#print(repo)
repo1=repo.replace("b2c-","")

### get the pullrequests
pull_requests = cp.get("DEFAULT", "pullrequests")
#print(pull_requests)

### get the  state eg like open,merge.
state = cp.get("DEFAULT", "state")
#print(state)

### put the branch is parameterized , eg like master or release
#branch = cp.get("DEFAULT", "branch")
#branch=sys.argv[2]
#print(branch)

#print(branches)



#print(branch1)
bt = []
bt.append(branch)
btt = []
for i in range(len(bt)):
	x=bt[i]
	y=x.split(',')
	for j in range(len(y)):
		btt.append(y[j])
print(btt)

brt = []
brt.append(repo)
brtt = []
for i in range(len(brt)):
	x=brt[i]
	y=x.split(',')
	for j in range(len(y)):
		brtt.append(y[j])
print(brtt)

#startlimit = ["&start=0&limit=1000","&start=100&limit=1000","&start=200&limit=1000","&start=300&limit=1000"]
startlimit = ["&start=0&limit=1000"]
#results = cp.get("DEFAULT", "results")
pr_list=[]
for branches in btt:
	
	
	if branches != "master":
		branches=branch.replace("/","%2F")
	else:
		branches="master"
	for repos in brtt:
		
		for results in startlimit:

			pull_request_url=url+repos+pull_requests+state+branches+results
			pull_request_url_file=url+repos+pull_requests

			diff = 'diff'
			commits = 'commits'
			#print(pull_request_url)
			#print(pull_request_url)

			#### call the bit bucket pull request url and auth details and converted to json
			res = requests.get(pull_request_url, headers=headers, auth=auth)

			### to get the valuses from json
			values =res.json()['values']
			#type(values)
			#values =res.json()['values']

			### 
			
			json_str=json.dumps(values)
			#type(json_str)

			### take a string and return json object 
			json_list=json.loads(json_str)
			type(json_list)

			

			### use for loop to fetch all the details in json_list and append into pr_list
			for j in json_list:
				pullreq_details={}
				
				
				
				pullreq_details['title'] = j['title']
				pullreq_details['repository'] = j['fromRef']['repository']['name']
				createdDate=datetime.datetime.fromtimestamp(j['createdDate']/1000)
				
				pullreq_details['createdDate'] = createdDate
				updatedDate=datetime.datetime.fromtimestamp(j['updatedDate']/1000)
				pullreq_details['updatedDate'] = updatedDate
				
				pullreq_details['author'] =j['author']['user']['displayName']
				pullreq_details['Branch_From'] = j['fromRef']['displayId']
				pullreq_details['Branch_To'] = j['toRef']['displayId']
				
				

				pullreq_details['state'] = j['state']
			   
				pullreq_details['pull_request_id'] = j['id']
				pid = pullreq_details['pull_request_id']
				url_for_files = pull_request_url_file + b + str(pid) + c + diff
				url_for_jira_ids = pull_request_url_file + b + str(pid) + c + commits
				print(url_for_files)
				file_res = requests.get(url_for_files, headers=headers, auth=auth)
				values = file_res.json()['diffs']
				#print(values)
				file_json_str = json.dumps(values)
				file_json_list = json.loads(file_json_str)
				#print(file_json_list)
				file_list = []
				for f in file_json_list:
					# print(f['new']['path'])
					if (f['destination']) is not None:
						#print(f['destination']['name'])
						file_list.append(f['destination']['name'])
						
					elif (f['source']) is not None:
						#print(f['source']['name'])
						file_list.append(f['source']['name'])
					else:
						print('value')  
				
				for f in file_json_list:
					# print(f['new']['path'])
					if (f['destination']) is not None:
						#print(f['destination']['name'])
						file_list1 = f['destination']['parent']
						
					elif (f['source']) is not None:
						#print(f['source']['name'])
						file_list1 = f['source']['parent']
					else:
						print('value')
							
				jira_res = requests.get(url_for_jira_ids, headers=headers, auth=auth)
				values1 = jira_res.json()['values']
				#print(values1)
				#print(values)
				jira_json_str = json.dumps(values1)
				jira_json_list = json.loads(jira_json_str)
				
				
				jira_list = []  
				for j in jira_json_list:
					# print(f['new']['path'])
					try:
						jira_list.append(j['properties']['jira-key'])
						#print(jira_list)
					except KeyError:
						pass
				issues_list = []
				for i in jira_list:
					for x in i:
							if x not in issues_list:
							
								issues_list.append(x)
                
                pullreq_details['files'] = file_list
                pullreq_details['parent_directory_of_files'] = file_list1
                pullreq_details['jira_issue'] = issues_list
        
                pr_list.append(pullreq_details)



#os.chdir(r"../reports")
a = cp.get("DEFAULT", "a")
##file=repo1 + a + branch1 
file="release_management_report"
#### To create report 
with open('pullrequest.csv', 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    writer.writerows(pr_list)
    
   
    

   
    f = open('pullrequest.csv')
    f.read().splitlines()
    f.close()

    


df = pd.read_csv (r'pullrequest.csv')
df['jira_issue']=df['jira_issue'].str.replace("]", "") 
df['jira_issue']=df['jira_issue'].str.replace("[", "")
df['jira_issue']=df['jira_issue'].str.replace("'", "")
#df['createdDate'] = df['createdDate'].apply(lambda x: pd.Timestamp(x).strftime('%Y-%m-%d'))
#DATE=df['createdDate']
df.sort_values(by=['createdDate'],inplace=True,ascending=False)

start_date= datetime.datetime(year, month, day,hours,mins)
end_date= datetime.datetime.now()
df['createdDate']=pd.to_datetime(df['createdDate'])
mask = (df['createdDate'].dt.tz_localize(None) > start_date) & (df['createdDate'].dt.tz_localize(None) <= end_date)
df_new=df.loc[mask]

df_new.to_excel(file + ".xlsx", index = None, header=True)


book = openpyxl.load_workbook(file + ".xlsx")
sheet1 = book.active
sheet1.column_dimensions['A'].width = 20
sheet1.column_dimensions['B'].width = 70
sheet1.column_dimensions['C'].width = 20
sheet1.column_dimensions['D'].width = 25
sheet1.column_dimensions['E'].width = 25
sheet1.column_dimensions['F'].width = 21
sheet1.column_dimensions['G'].width = 50
sheet1.column_dimensions['H'].width = 15
sheet1.column_dimensions['I'].width = 10

sheet1.column_dimensions['J'].width = 600
sheet1.column_dimensions['K'].width = 100
sheet1.column_dimensions['L'].width = 20








book.save(file + ".xlsx")
book.close()






####if the file exits it will be remove

filePath = 'pullrequest.csv';
# As file at filePath is deleted now, so we should check if file exists or not not before deleting them
if os.path.exists(filePath):
    os.remove(filePath)
else:
    print("Can not delete the file as it doesn't exists")
 