from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pubmed import get_concept_graph

app = FastAPI()

# Pour autoriser le frontend React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Remplace par ton frontend plus tard
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(query: str = Query(..., min_length=3)):
    graph = get_concept_graph(query)
    return graph
