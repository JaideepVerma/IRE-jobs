import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import os
from datetime import datetime, timezone, timedelta

def get_ist_timestamp():
    ist = timezone(timedelta(hours=5, minutes=30))
    return datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S")

def scrape_barclays():
    url = "https://careers.ardonagh.com/jobs?split_view=true&query=&country=Ireland"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
        "Accept": "*/*"
    }

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    #print(soup)
  
    
    jobs = []
    #print(soup)
    for job_card in soup.select("ul#jobs_list_container li.block-grid-item"):  
        
        link = job_card.select_one("a")
        #print(link)
        #title = link.get_text(strip=True) if link else None
        apply_link = link["href"] if link and link.has_attr("href") else None
        #role = link.select_one(".flex flex-col justify-center p-3 text-center min-h-[11.25rem]")
        #div = link.select_one("div")
        #print(div)
        job_info_div = link.select_one("div.flex.flex-col.justify-center")
        role = job_info_div.select_one("span").get_text(strip=True)
        company_location = job_info_div.get_text(strip=True).replace(role, "").strip()

        #print("Title:", title)
        #print("Company/Location:", company_location)
        #print(role)
        #print(title)
        #print(apply_link)
        #print('----')
        
        jobs.append({
            "company": 'Ardonagh',
            "industry": 'industry',
            "job_id": 'Not found',
            "role":role,
            "description": 'description',
            "responsibilities" : 'responsibilities',
            "qualifications": 'qualifications',
            "location": company_location,
            "JobFamily":'job_family',
            "JobFunction":'job_function',
            "posting_date": 'posting_date',
            "update_date":'update_date',
            "apply_link": apply_link                
        })
   
        #jobs.append(job)
    print(len(jobs), "barclays Jobs added")
    
    return jobs
    
def save_jobs(jobs):
    # Get current directory
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'ardonaghjobs.db')
    #dbpath = f'C:/Users/jdver/OneDrive/Desktop/py/JPMCjobs.db'
    print('Jobs added to : ' , dbpath)
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    #print(jobs)
    for job in jobs:

        c.execute("SELECT * FROM jobs WHERE company=? AND role=?",
                  (job["company"], job["role"]))
        if not c.fetchone():
            c.execute("""INSERT INTO jobs 
                         (company,industry, job_id, role, description, responsibilities, qualifications, location, posting_date, job_family, job_function,update_date, apply_link) 
                         VALUES (?,?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?)""",
                      (job["company"],job["industry"], job["job_id"], job["role"], job["description"], job["responsibilities"], job["qualifications"], job["location"], job["posting_date"], job["JobFamily"], job["JobFunction"],job["update_date"],job["apply_link"])) ##
    conn.commit()
    conn.close()

def create_db():
    current_dir = os.getcwd()
    dbpath = os.path.join(current_dir, 'ardonaghjobs.db')
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    #c.execute('''DROP Table jobs''')
    c.execute('''
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        industry TEXT,
        job_id TEXT,
        role TEXT,
        description TEXT,
        responsibilities TEXT,
        qualifications TEXT,
        location TEXT,
        posting_date TEXT,
        job_family TEXT,
        job_function TEXT,
        apply_link TEXT,
        update_date TEXT,
        loaded_at TEXT 
            
    )
    ''')
    conn.commit()
    conn.close()

    print("Jobs table updated successfully.")

#Run Below if there is any new column 
'''
conn = sqlite3.connect("JPMCjobs.db")
cur = conn.cursor()
cur.execute("ALTER TABLE jobs ADD COLUMN update_date TEXT;")
conn.commit()
conn.close() 
'''
def main():
    # put your scraping logic here
    create_db()
    jobs =scrape_barclays()
    save_jobs(jobs)
    
    print('Ardonagh Jobs saved to .db')
    #print("Running JPMC scraper...")

if __name__ == "__main__":
    main()
    


   
