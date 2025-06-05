from Bio import Entrez
import itertools
from collections import Counter

Entrez.email = "your_email@example.com"

def get_concept_graph(query, retmax=50):
    # 1. Recherche d’articles
    handle = Entrez.esearch(db="pubmed", term=query, retmax=retmax)
    record = Entrez.read(handle)
    ids = record["IdList"]

    # 2. Récupération MeSH Terms
    handle = Entrez.efetch(db="pubmed", id=",".join(ids), rettype="medline", retmode="text")
    records = handle.read().split("\n\n")

    mesh_lists = []
    for rec in records:
        terms = []
        for line in rec.split("\n"):
            if line.startswith("MH  - "):
                terms.append(line[6:].strip())
        if terms:
            mesh_lists.append(terms)

    # 3. Cooccurrence
    pair_counts = Counter()
    for terms in mesh_lists:
        pairs = itertools.combinations(sorted(set(terms)), 2)
        pair_counts.update(pairs)

    # 4. Génération de graphe en JSON
    nodes = set()
    edges = []
    for (a, b), w in pair_counts.items():
        nodes.add(a)
        nodes.add(b)
        edges.append({"source": a, "target": b, "weight": w})

    return {
        "nodes": [{"id": node} for node in nodes],
        "edges": edges
    }
