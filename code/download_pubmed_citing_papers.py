from Bio import Entrez
import cPickle as pickle
import multiprocessing as mp
import os, glob

Entrez.email = 'bdo311@gmail.com'
    
def process_citations(z):
    print z
    if glob.glob("../data/pubmed_citations/citations_{}.pkl".format(z)): return
    pmids = [str(i) for i in range(z, z + 10000)]
    handle = Entrez.elink(dbfrom="pubmed", id=pmids, cmd="neighbor", retmode="xml", linkname="pubmed_pubmed_citedin")
    records = Entrez.read(handle)

    pmids = [int(rec['IdList'][0]) for rec in list(records)]
    citing_papers = [[int(paper['Id']) for paper in rec['LinkSetDb'][0]['Link']] if rec['LinkSetDb'] else [] for rec in list(records)]

    records_slim = dict(zip(pmids, citing_papers))
    pickle.dump(records_slim, open("../data/pubmed_citations/citations_{}.pkl".format(z), 'w'))
    
if not glob.glob("../data/pubmed_citations/"): os.mkdir("../data/pubmed_citations")
p = mp.Pool(24)
p.map(process_citations, range(0, 29000000, 10000))    