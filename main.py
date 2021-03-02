import requests
import datetime
import pandas as pd
from sty import fg, bg, ef, rs

#from unpywall.utils import UnpywallCredentials
#
#UnpywallCredentials('ycarissan@gmail.com')

now = datetime.datetime.now()
this_year = now.year

halid="yannickcarissan"
firstname="Yannick"
lastname="CARISSAN"
r=requests.get("https://api.archives-ouvertes.fr/search//?q=(authIdHal_s:{}%20OR%20authFullName_sci:%22{}%20{}%22)%20AND%20docType_s:ART&rows=10000&sort=producedDate_tdate%20desc&fl=docid,docType_s,authFullName_s,authAlphaLastNameFirstNameId_fs,title_s,number_s,producedDate_s,producedDateY_i,files_s,label_s,label_xml,halId_s,doiId_s".format(halid,firstname,lastname))

response_dec = r.json()

number_of_docs = response_dec["response"]["numFound"]
docs = response_dec["response"]["docs"]
print("Number of documents : {}".format(number_of_docs))

df = pd.DataFrame()
for doc in docs:
    doctype = doc["docType_s"]
    docid = doc["docid"]
    halid = doc["halId_s"]
    title = doc["title_s"][0]
    authors_full_name=""
    for auth in doc["authFullName_s"]:
        if len(authors_full_name)>0:
            authors_full_name = authors_full_name + ", " + auth
        else:
            authors_full_name = auth

    date = doc["producedDate_s"]
    year = doc["producedDateY_i"]
    try:
        doiid = doc["doiId_s"]
    except:
        doiid = "n/a"
    try:
        file_attached = doc["files_s"][0]
    except:
        file_attached = None
    if (file_attached!=None):
        hal_ok = fg.green + "\U00002714" + fg.rs
    else:
        hal_ok = fg.red + "\U00002718" + fg.rs
    dict_doc = {}
    dict_doc["doctype"] = doctype
    dict_doc["docid"]   = docid
    dict_doc["halid"]   = halid
    dict_doc["title"]   = title
    dict_doc["authors"] = authors_full_name
    dict_doc["date"]    = date
    dict_doc["year"]    = year
    dict_doc["doiid"]   = doiid
    dict_doc["hal_ok"]  = hal_ok
    df = df.append(dict_doc, ignore_index=True)
print(df)
