from requests import Session
import cloudscraper
import pandas as pd
import json

#  scrape 8a to collect data for database containing boulders and crags across the southeast.
file = 'database.json'

with open(file, 'r') as f:
    data = json.load(f)


crag = data['crags']
for key,values in crag.items():
    cragSlug = values['cragSlug']
    country = values['countrySlug']
    

#each boulderfield is sorted different. When looking for stone-fort, it returns route immediately. When looking at rocktown, it returns crags within the boulderfield, not the routes. How to create the url automatically based on this? 



page_index = 0 

#two urls to try. different zones will need to use alternate url to grab data
url = f"https://www.8a.nu/api/zlaggables/bouldering/{country}?sectorSlug=&pageIndex={page_index}&sortField=totalascents&grade=&searchQuery=&order=desc&cragSlug={cragSlug}"

sess = Session()
scraper = cloudscraper.create_scraper(
)

everything_from_api = scraper.get(url).text
response2 = scraper.get(url)
boulders_input = response2.json()
keep_keys = ['zlaggableName','zlaggableSlug','difficulty','gradeIndex',
                'countryName','countrySlug','cragName','cragSlug','sectorName', 'sectorSlug']

#function that pulls crag info
def grabbing_boulders(boulders_input):
    """Pass the GET response and retain only needed boulder attributes"""
    slim_boulders = []
    for boulder in boulders_input['items']: 
        tmp = {}
        for k,v in boulder.items():
                if k in keep_keys:
                    tmp[k] = v
        slim_boulders.append(tmp)
    return slim_boulders


continue_grabbing = boulders_input['pagination']
more_pages = continue_grabbing['hasNext']

while more_pages == True: 
    page_index += 1 ##This is not totally correct. While more pages is true, + 1 page and put the data into the new dictionary and then run the scipt again for the next page.
    grabbing_boulders(boulders_input)

# for pages in boulders_input['pagination']:
#     while more_pages == 'true':


# boulders_input = json.loads(everything_from_api)





    
df = pd.json_normalize(slim_boulders)
df.rename(
    columns={
        'zlaggableName':'boulderName',
        
    }
)




# Just another method for grabbing boulders. A little wordier, but functional. 
# boulders_output = []
# for boulder in boulders_input['items']:
#     boulder_object = {}
#     boulder_object['boulderName']= boulder['zlaggableName']
#     boulder_object['boulderSlug']= boulder['zlaggableSlug']
#     boulder_object['difficulty']= boulder['difficulty']
#     boulder_object['gradeIndex']= boulder['gradeIndex']
#     boulder_object['countryName']= boulder['countryName']
#     boulder_object['countrySlug']= boulder['countrySlug']
#     boulder_object['cragName']= boulder['cragName']
#     boulder_object['cragSlug']= boulder['cragSlug']
#     boulder_object['sectorName']= boulder['sectorName']

#     boulders_output.append(boulder_object)

# print(boulders_output)
# # store the data in a new file 

