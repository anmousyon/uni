import json
from Bio import Entrez

EMAIL = 'jlm141230@utdallas.edu'

def search(query):
    Entrez.email = EMAIL
    handle = Entrez.esearch(
        db='pubmed',
        sort='relevance',
        retmax='20',
        retmode='xml',
        term=query
    )
    results = Entrez.read(handle)
    return results

def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = EMAIL
    handle = Entrez.efetch(
        db='pubmed',
        retmode='xml',
        id=ids
    )
    results = Entrez.read(handle)
    return results

def main():
    results = search('fever')
    id_list = results['IdList']
    papers = fetch_details(id_list)
    for paper in papers:
        print(paper['MedlineCitation']['Article']['ArticleTitle'])
    print(json.dumps(papers[0], indent=2, separators=(',', ':')))

main()