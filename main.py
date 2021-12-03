import requests
import datetime
import pandas as pd
from sty import fg, bg, ef, rs
import sqlite3 as sql
from pyexcel_ods import save_data
from collections import OrderedDict

#from unpywall.utils import UnpywallCredentials
#
#UnpywallCredentials('toto@gmail.com')

names=["Paola NAVA", "Jean-Marc MATTALIA", "Denis HAGEBAUM-REIGNIER", "Stéphane HUMBEL", "Gwang-Hi JEUNG", "Yannick CARISSAN"]
#names=["Paola"]

df = pd.DataFrame()
dict_doc = {}
total_number_of_docs = 0

collaborators_ism2=["rodriguez", "coquerel", "chuzel", "chouraqui", "commeiras", "martinez", "orio", "simaan", "clavier"]

for name in names:
    if name=="Paola NAVA":
        halid_user="paola-nava"
        firstname="Paola"
        lastname="NAVA"
    elif name=="Denis HAGEBAUM-REIGNIER":
        halid_user="denis-hagebaum-reignier"
        firstname="Denis"
        lastname="HAGEBAUM-REIGNIER"
    elif name=="Stéphane HUMBEL":
        halid_user="stephane-humbel"
        firstname="Stéphane"
        lastname="HUMBEL"
    elif name=="Gwang-Hi JEUNG":
        halid_user="gwang-hi-jeung"
        firstname="Gwang-Hi"
        lastname="JEUNG"
    elif name=="Jean-Marc MATTALIA":
        halid_user="jean-marc-mattalia"
        firstname="Jean-Marc"
        lastname="MATTALIA"
    elif name=="Yannick CARISSAN":
        halid_user="yannickcarissan"
        firstname="Yannick"
        lastname="CARISSAN"
        
    now = datetime.datetime.now()
    this_year = now.year
    
    request = "https://api.archives-ouvertes.fr/search//?q=(authIdHal_s:{}%20OR%20authFullName_sci:%22{}%20{}%22)%20AND%20docType_s:ART&rows=10000&sort=producedDate_tdate%20desc&fl=docid,docType_s,authFullName_s,authAlphaLastNameFirstNameId_fs,title_s,number_s,producedDate_s,producedDateY_i,files_s,label_s,label_xml,halId_s,doiId_s,collCode_s,openAccess_bool,linkExtId_s,linkExtUrl_s,journalTitle_s".format(halid_user,firstname,lastname)
    r=requests.get(request)
    print(request)
    
    response_dec = r.json()
    
    number_of_docs = response_dec["response"]["numFound"]
    docs = response_dec["response"]["docs"]
    print("Number of documents : {}".format(number_of_docs))
    
    for doc in docs:
        doctype = doc["docType_s"]
        docid = doc["docid"]
        halid = doc["halId_s"]
        title = doc["title_s"][0]
        journalTitle = doc["journalTitle_s"]
        authors_full_name=""
        for auth in doc["authFullName_s"]:
            if len(authors_full_name)>0:
                authors_full_name = authors_full_name + ", " + auth
            else:
                authors_full_name = auth
        coll  = ""
        try:
            for c in doc["collCode_s"]:
                if len(coll)>0:
                    coll = coll + ", " + c
                else:
                    coll = c
        except:
            coll="n/a"
        date = doc["producedDate_s"]
        year = doc["producedDateY_i"]
        try:
            doiid = doc["doiId_s"]
        except:
            doiid = "n/a"
        try:
            openAccess_bool = doc["openAccess_bool"]
        except:
            openAccess_bool = None
        try:
            linkExtId_s = doc["linkExtId_s"][0]
        except:
            linkExtId_s = None
        try:
            linkExtUrl_s = doc["linkExtUrl_s"][0]
        except:
            linkExtUrl_s = None
        try:
            file_attached = doc["files_s"][0]
        except:
            file_attached = None
        if (file_attached!=None):
            hal_ok = fg.green + "\U00002714" + fg.rs
        else:
            hal_ok = fg.red + "\U00002718" + fg.rs
        dict_doc["doctype"] = doctype
        dict_doc["docid"]   = docid
        dict_doc["halid"]   = halid
        dict_doc["title"]   = title
        dict_doc["authors"] = authors_full_name
        interequipe=False
        for collaborator in collaborators_ism2:
            interequipe = interequipe or ( collaborator in authors_full_name.lower() )
        dict_doc["interequipe"] = interequipe
        dict_doc["date"]    = date
        dict_doc["year"]    = year
        dict_doc["doiid"]   = doiid
        dict_doc["hal_ok"]  = hal_ok
        dict_doc["coll"]    = coll
        dict_doc["openaccess"] = openAccess_bool
        dict_doc["linkExtId_s"] = linkExtId_s
        dict_doc["linkExtUrl_s"] = linkExtUrl_s
        dict_doc["journalTitle"] = journalTitle
        df = df.append(dict_doc, ignore_index=True)
#    print(df[["year", "doiid", "halid", "hal_ok", "coll"]].to_markdown())
    total_number_of_docs = total_number_of_docs + number_of_docs

for idx in df.index:
    doc = df.index[idx]
    authors_ctom=""
    for name in names:
        if name.lower() in authors_full_name.lower():
            authors_ctom = "{}, {}".format(authors_ctom, name)
#    df.iloc(idx)["authors_ctom"] = authors_ctom
#    df.at[idx, "authors_ctom"] = authors_ctom

df = df.drop_duplicates(["halid"])
print(df[["year", "doiid", "halid", "hal_ok"]].to_markdown)
df.to_excel("papers.xls")
conn = sql.connect('biblio.db')
df.to_sql('biblio', conn)
