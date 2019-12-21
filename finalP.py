
# %matplotlib inline
import requests
import json
import ast
import string
import pandas as pd
import pymongo
from random import randint
import re
import numpy as np
import matplotlib.pyplot as plt
from datetime import date

def send_request(jobCate):
    try:
        response = requests.get( url="https://www.amazon.jobs/en/search.json?",params={
                "base_query": "",
                "category[]": jobCate,
                "city": "",
                "country": "",
                "county": "",
                "facets[]": "location,category,normalized_location,job_function_id, business_category, schedule_type_id, employee_class, normalized_location, job_function_id",
                "latitude": "",
                "loc_group_id": "",
                "loc_query": "",
                "longitude": "",
                "offset": 0,
                "query_options": "",
                "radius": "24km",
                "region": "",
                "result_limit": 10000,
                "sort": "relevant"},
            headers={
                "Host": "www.amazon.jobs",
                "Connection": "keep-alive",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
                "Accept-Encoding": "gzip, deflate",
                "Cookie": "preferred_locale=en-US"})
        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
        return response.text
    except requests.exceptions.RequestException:
        print('HTTP Request failed')

################################################################################
def geoL(city_L, country_L, cities, state_L, state, lat, lng, country_code):
    if country_L == "US":
        for count2 in range(0,len(cities)): 
            
            if city_L == cities[count2] and state_L == state[count2]:
                Lat_Lon = [lat[count2],lng[count2]]
                break
            if count2 == len(cities)-1:
                Lat_Lon = ["",""] 
    else:
        for count2 in range(0,len(cities)):
            if city_L == cities[count2]:
                Lat_Lon = [lat[count2],lng[count2]]
                break
            if count2 == len(cities)-1:
                for count in range(0,len(cities)):
                    if country_code[count] == country_L:
                        Lat_Lon = [lat[count],lng[count]]
                        break
                    if count == len(cities)-1:
                        Lat_Lon = ["",""]
    return Lat_Lon
###############################################################################
#Get geocoordinates from a file
geocoor = pd.read_csv("Otros_Resources/worldcities.csv")
cities = geocoor["city_ascii"].tolist()
country_code = geocoor["iso2"].tolist()
state = geocoor["admin_name"].tolist()
lat = geocoor["lat"].tolist()
lng = geocoor["lng"].tolist()
###############################################################################
def addr(Location):
    try:
        comP_loc = Location.split(", ")
        if (len(comP_loc) == 3):
            st = comP_loc[1]
        if (len(comP_loc) == 2):
            st = "NaN"
        return st
    except:
        st = "NaN"
        return st
###############################################################################
job_categories = ["administrative-support",                    #01done
                  "audio-video-photography-production",        #02done
                 "business-merchant-development"]#,              #03done
                #  "business-intelligence",                      #04done
                #  "buying-planning-instock-management",         #05done
                #  "customer-service",                           #06done
                #  "data-science",                               #07done
                #  "database-administration",                    #08done
                #  "design",                                     #09done
                #  "economics",                                  #10done
                #  "editorial-writing-content-management",       #11done
                #  "facilities-maintenance-real-estate",         #12done
                #  "finance-accounting",                         #13done
                #  "fulfillment-operations-management",
                #  "fulfillment-warehouse-associate",
                #  "hardware-development",
                #  "human-resources",                            #17done
                #  "investigation-loss-prevention",
                #  "leadership-development-training",
                #  "legal",
                #  "machine-learning-science",                   #21done
                #  "marketing-pr",
                #  "medical-health-safety",
                #  "operations-it-support-engineering",          #24done
                #  "project-program-product-management-non-tech",#25done
                #  "public-policy",
                #  "research-science",                           #27done
                #  "sales-advertising-account-management",
                #  "software-development",                      #29done
                #  "solutions-architect",                        #30done
                #  "supply-chain-transportation-management",     #31done
                #  "systems-quality-security-engineering",       #32done
                #  "project-program-product-management-technical"] #33done
###############################################################################
def updating(job_categories):
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)
    db = client.jobs
    collection = db.roles
    collection2 = db.filled

    category_add_rem = []    
    jobs_L = []
    job_list_to_add = []
    job_list_to_rem = []
    #-------------------------------------
    for job_cat in job_categories:
        raw_D = send_request(job_cat)    #aqui llamando a la funcion
        raw_D = json.loads(raw_D)
        jobs = raw_D["jobs"]             #esta lista contiene todos los roles que van a ser documents en el collection

        jobs_dic = {}
        state_L = []
        job_ID_list = []
        arr = []
        
        for job in jobs:
            jobs_dic["category"] = job["job_category"]
            jobs_dic["title"] = job["title"]
            jobs_dic["Job_ID"] = job["id_icims"]
            jobs_dic["City"] = job["city"]
            jobs_dic["Country"] = job["country_code"]

            statex = job["normalized_location"]
            state_L = addr(statex)           #aqui llamo a la funcion ADDR
            
            jobs_dic["Posted_date"] = job["posted_date"]
            jobs_dic["Description"] = job["description"]
            jobs_dic["Basic_Qualif"] = job["basic_qualifications"]
            jobs_dic["Preferred_Qualif"] = job["preferred_qualifications"]
            jobs_dic["Company"] = job["company_name"]
            jobs_dic["Apply"] = job["url_next_step"]
            jobs_dic["Geocoordinates"] = geoL(job["city"], job["country_code"], cities, state_L, state, lat, lng, country_code)
            job_ID_list.append(job["id_icims"])
            jobs_L.append(jobs_dic.copy())

        for obj in collection.find():
            try:
                formaObj = obj["category"].lower()
                formaObj = re.sub("/", " ", formaObj)
                formaObj = re.sub("-", " ", formaObj)
                formaObj = formaObj.translate(str.maketrans('', '', string.punctuation))
                formaObj = re.sub(" +", " ", formaObj)
                formaObj = re.sub(" ", "-", formaObj)
            except:
                print("error", obj["Job_ID"])

            if formaObj == job_cat:
                arr.append(obj["Job_ID"])

        new_jobs = list(set(job_ID_list) - set(arr))
        remove_jobs = list(set(arr) - set(job_ID_list))
        job_list_to_add = job_list_to_add + new_jobs
        job_list_to_rem = job_list_to_rem + remove_jobs
        category_add_rem.append([len(new_jobs),len(remove_jobs)])
    return category_add_rem, job_list_to_add, job_list_to_rem, jobs_L
##############################################################################
##############################################################################
##############################################################################



