import requests
import datetime
import pandas as pd
from sty import fg, bg, ef, rs

#from unpywall.utils import UnpywallCredentials
#
#UnpywallCredentials('ycarissan@gmail.com')

now = datetime.datetime.now()
this_year = now.year

r=requests.get("https://api.archives-ouvertes.fr/search//?q=(authIdHal_s:yannickcarissan%20OR%20authFullName_sci:%22Yannick%20CARISSAN%22)%20AND%20docType_s:ART&rows=10000&sort=producedDate_tdate%20desc&fl=docid,docType_s,authFullName_s,authAlphaLastNameFirstNameId_fs,title_s,number_s,producedDate_s,producedDateY_i,files_s,label_s,label_xml,halId_s,doiId_s")

response_dec = r.json()

number_of_docs = response_dec["response"]["numFound"]
docs = response_dec["response"]["docs"]
print("Number of documents : {}".format(number_of_docs))
for yy in range(this_year, 2000, -1):
    print("Documents published in {} :".format(yy))
    for doc in docs:
        if doc["producedDateY_i"] == yy:
            docid = doc["docid"]
            halid = doc["halId_s"]
            title = doc["title_s"][0]
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
            print("hal-did : {} DOI : {} Title : {}... {}".format(halid, doiid, title[:40], hal_ok))
