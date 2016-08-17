'''
Author: Scott Dwyer
First created: August 13
Questions? spdwyer2@gmail.com
'''

import pandas as pd
import requests
from bs4 import BeautifulSoup 
import re 

#pull Trump-specific statements from politifact. The "n" determines how many statements are pulled. NOTE: it's left at 1 right now just for simplicity's sake. I plan on upping it to 180 once I get the formatting right.
statements = requests.get("http://www.politifact.com/api/statements/truth-o-meter/people/donald-trump/xml/?n=5")

#Encode the xml in utf-8 because the internet is terrible
statements = statements.text.encode("utf-8")

#Parse the XML with BeautifulSoup
soup = BeautifulSoup(statements, "xml") 

#These statements find and store the various tags that pertain to rulings (lie, truth, etc.), the date the statement was made
rulingslugs = soup.find_all("ruling_slug")
rulingdates = soup.find_all('ruling_date')
rulingdomains = soup.find_all("subject_slug")
rulingsubjects = soup.find_all("subject")
rulingnames = soup.find_all("name_slug")
rulingstatement = soup.find_all("statement")

#These are the lists for the above attributes (truth, date, subject, etc.) that I'll append with individual comments using the below for loops
rulings = []
names = []
dates = []
domains = []
subjects = []
statements = []

#These are all my for loops - they populate the above lists. They strip the XML tags using get_text()
for element in rulingslugs:
	ruling_result = element.get_text()
	rulings.append(ruling_result)

for element in rulingdates:
	ruling_date = element.get_text()
	dates.append(ruling_date)

for element in rulingdomains:
	ruling_domain = element.get_text()
	#ruling_domain = str(ruling_domain)
	#ruling_domain = str(ruling_domain)
	ruling_domain_fixed = " ".join([str(item) for item in ruling_domain])
	#ruling_domain = " ".join([str(item) for item in ruling_domain])
	domains.append(ruling_domain_fixed)

for element in rulingsubjects:
	ruling_subject = element.get_text()
	#ruling_subject = str(ruling_subject)
	ruling_subject_fixed = " ".join([str(item) for item in ruling_subject])
	#ruling_subject = str(ruling_subject)
	#ruling_subject = " ".join([str(item) for item in ruling_subject])
	subjects.append(ruling_subject_fixed)

for element in rulingnames:
	ruling_names = element.get_text()
	#ruling_names = str(ruling_names)
	ruling_names_fixed = " ".join([str(item) for item in ruling_names])
	#ruling_names = " ".join([str(item) for item in ruling_names])
	#ruling_names = str(ruling_names)
	names.append(ruling_names_fixed)

for element in rulingstatement:
	ruling_statement = element.get_text()
	statements.append(ruling_statement)

data = {}
data['rulings'] = rulings
data['names'] = names
data['dates'] = dates
data['domains'] = domains
data['subjects'] = subjects
data['statements'] = statements

'''
def is_military(content):
	if "military" in content:return 1
	else: return 0
df['military'] = df.domains.apply(is_military)
'''

df = pd.DataFrame.from_dict(data)
#print df.domains.unique()
df['statements'].apply(lambda x: re.sub('<[^>]*>|&quot;','',x).strip())
df.to_csv('new_after_Ivan4.csv')

#I've included these just to show that the results are not perfectly formatted


'''
Issues:
1. For fields that potentially have two entries, e.g. domain, should I create columns like "domain 1", "domain 2", "domain 3", and have 2 and 3 NULL if
there is only one?
2. Still can't get those darn quotes off of my "statements" column
3. 


Ivan advice:
Create TFIDF score for every single statement
These scores are for words
Then have topic scores for every observation

'''


