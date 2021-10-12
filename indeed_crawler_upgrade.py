import requests
from bs4 import BeautifulSoup
import pandas as pd

idArray = []

# Extracts everything from the page. Entire HTML 
def extractLayer1(page):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f'https://www.indeed.com/jobs?q=Developer+USA&explvl=entry_level&start={page}'
    r = requests.get(url,headers)
    # Used to return status 200 if we are able to access the site properly. 
    # return r.status_code
    soup = BeautifulSoup(r.content,'html.parser')
    return soup

# Filters out the required "divs" from HTML (Passed from extract function)
def scrapLayer1(soup):
    # Finds all the div that has the respective class from the html taken from extract function. 
    divs = soup.find_all('a',class_ = 'tapItem')
    for item in divs: 
        if item.get('id') is not None:
            id = item.get('id')
            id = id.replace('job_','')
            idArray.append(id)
            link = f"https://www.indeed.com/jobs?q=Developer+USA&explvl=entry_level&vjk={id}"
        else:
            idArray.append("NTH")
        
        title = location = item.find('h2', class_ = 'jobTitle').text.strip()
        company = item.find('span', class_ = 'companyName').text.strip()
        date = item.find('span', class_ = 'date').text.strip()
        summary = item.find('div', class_ = 'job-snippet').text.strip().replace('\n','')
        
        location = item.find('div', class_ = 'companyLocation')
        if location is not None:
            location = location.text.strip()
        else:
            location = ''
        
        # Storing all data obtained into a Dictionary. 
        job = {
            'Job Title':title, 
            'Job Location':location, 
            'Job Company Name':company,
            'Job Description':summary, 
            'Job Date' : date, 
            # 'Job Salary':salary, 
            'Job Link':link,
        }

        joblist.append(job)
    return 

# Extracts everything from the page. Entire HTML 
def extract(id):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    url = f'https://www.indeed.com/viewjob?jk={id}'
    r = requests.get(url,headers)
    # Used to return status 200 if we are able to access the site properly. 
    # return r.status_code
    soup = BeautifulSoup(r.content,'html.parser')
    return soup

joblist = []

# Get all HTML details of job search 
# Create loop here to obtain more job info, to cover pagination. 
c = extractLayer1(0)
# Getting ID of all available jobs extracted
scrapLayer1(c)

for i in range(0,len(idArray)):
    d = extract(idArray[i])
    desc = d.find('div',class_ = 'jobsearch-jobDescriptionText').text
    joblist[i]['Job Description'] = desc
    print(joblist[i]["Job Description"])

df = pd.DataFrame(joblist)
print(df.head())
df.to_csv(r'C:\Users\Asif\Desktop\Indeed Crawler\jobs.csv')
print(joblist)