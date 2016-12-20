from Bio import Medline, Entrez
from pprint import pprint
import sys
import cPickle as pickle
import multiprocessing as mp
import os, glob

#pmids = ['26878240', '18665331', '18661158', '18627489', '18627452', '18612381']
Entrez.email = 'bdo311@gmail.com'
#handle = Entrez.efetch(db="pubmed", id=pmids, rettype="medline", retmode="text")

def simplify(info):
    record = {}
    article = info['MedlineCitation']['Article']

    record["pmid"] = int(info['MedlineCitation']['PMID'])
#     record["title"] = article['ArticleTitle']
    try: record["journal"] = article['Journal']['Title']
    except: record["journal"] = ""
#     try: record["jabbr"] = article['Journal']['ISOAbbreviation']
#     except: record["jabbr"] = ""
    #record["year"] = article['Journal']['JournalIssue']['PubDate']['Year']
    try:
        record["yr"] = dict(info['PubmedData']['History'][0])['Year']
        record["mo"] = dict(info['PubmedData']['History'][0])['Month']
    except:
        record["yr"] = ""
        record["mo"] = ""
    record["keywords"] = info['MedlineCitation']['KeywordList']
    try:
        record["authors"] = []
        for au in article["AuthorList"]:
            record["authors"].append([au["LastName"], au["ForeName"], au["Initials"], au["AffiliationInfo"]])
    except: pass
    return record
    
def process_citations(z):
    print z
    if glob.glob("../data/pubmed/pubmed_{}.pkl".format(z)): return
    pmids = [str(i) for i in range(z, z + 10000)]
    handle = Entrez.efetch(db="pubmed", id=pmids, retmode="xml")
    #records = Medline.parse(handle)
    records = Entrez.read(handle)["PubmedArticle"]
    #print records
    # fields = ('PMID', 'AU', 'FAU', 'AD', 'IRAD', 'DP', 'TI', 'JT', 'TA', 'OT', 'PT', 'AID')
    # all_records = []
    
    records_slim = [simplify(x) for x in list(records)]
    pickle.dump(records_slim, open("../data/pubmed/pubmed_{}.pkl".format(z), 'w'))
    
if not glob.glob("../data/pubmed/"): os.mkdir("../data/pubmed")
p = mp.Pool(5)
p.map(process_citations, range(0, 29000000, 10000))    