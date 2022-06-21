import json
import yaml
import requests
from bs4 import BeautifulSoup


with open('temp.json', 'r') as file:
    data = json.load(file)

filtered_data = []

new_data = []

for d in data[10:11]:
    scrape_url = d['link']

    req = requests.get(scrape_url)
    content = req.text

    soup = BeautifulSoup(content, features="html.parser")

    #Get title
    title = soup.find(id="gsc_oci_title").string
    print(title)
    
    #Initialise dict
    temp_dict = {'title': None, 'description': None, 'image': None, 'authors': None, 'link':{'url': None, 'display': None, 'DOI': None, 'video': None, 'talk':None, 'bibtex': None}, 'highlight': None, 'year': None, 'type': None, 'news2': None, 'award': None}
    
    #Get tabular scholar data
    for div in soup.body.findAll("div", class_="gs_scl"):
        field_name = div.find("div", class_="gsc_oci_field").string.lower() #Get scholar fieldname
        
        field_value = div.find("div", class_="gsc_oci_value").string #Get value of field
        field_links = div.find('a') #Collect any links
        
        #Check for publication info
        if field_name == "book":
            temp_dict['link']['display'] = str(field_value) #Can't trust scholar for book credit so don't change type
            continue
        elif field_name == "journal":
            temp_dict['link']['display'] = str(field_value)
            temp_dict['type'] = "journal"
            continue
            
        if field_name == "pages":
            temp_dict['link']['display'] = temp_dict['link']['display'] + ", pages " + str(field_value)
            continue
        
        if field_name == "publication date":
            continue
        
        if field_value != None:
            temp_dict[str(field_name)] = str(field_value)
        if field_links != None:
            temp_dict['link']['url'] = "https://scholar.google.com" + str(field_links.get("href"))
    
    temp_dict['title'] = str(title)
    temp_dict['highlight'] = 0 #default
    temp_dict['year'] = int(d['year'])
    
    filtered_data.append(temp_dict)


def represent_none(self, _):
    return self.represent_scalar('tag:yaml.org,2002:null', '')

yaml.add_representer(type(None), represent_none)

with open(r'test.yml', 'w') as file:
    outputs = yaml.dump(filtered_data, file)
