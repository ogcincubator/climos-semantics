import re
import sys
from pathlib import Path

from openpyxl import load_workbook
from rdflib import Namespace, URIRef, Graph, RDF, SKOS, OWL, Literal, RDFS, BNode

import warnings

from climos_utils import strip

warnings.filterwarnings("ignore")

CONCEPT_SCHEMES = [
    {
        'id': 'sandflies',
        'name': 'Sandfly species',
        'ws': 'SandflySpecies',
    },
    {
        'id': 'parasites',
        'name': 'Parasite species',
        'ws': 'ParasiteSpecies',
    },
    {
        'id': 'phleboviruses',
        'name': 'Phlebovirus species',
        'ws': 'Phleboviruses',
    }
]
CLIMOS = Namespace('https://w3id.org/climos/')
CLIMOS_PROPS = Namespace(CLIMOS['properties/'])

wb = load_workbook(filename=sys.argv[1], read_only=True, data_only=True)

g = Graph()
g.bind('climos', CLIMOS)
g.bind('climos-props', CLIMOS_PROPS)
g.add((BNode(), URIRef('http://www.opengis.net/ogc-na#targetGraph'), CLIMOS['species']))
for cs_def in CONCEPT_SCHEMES:
    ws = wb[cs_def['ws']]
    namespace = Namespace(f"https://w3id.org/climos/species/{cs_def['id']}/")
    g.bind(cs_def['id'], namespace)

    scheme = URIRef(f"https://w3id.org/climos/species/{cs_def['id']}")
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.prefLabel, Literal(cs_def['name'])))

    for i, row in enumerate(ws.rows):
        if i == 0:
            continue

        row_values = [strip(c.value) if c.value else '' for c in row]

        if not any(row_values):
            continue

        res_uri = row_values[0]
        if not res_uri or not res_uri.strip():
            raise ValueError(f"Invalid URI identifier at {cs_def['ws']} row {i}")
        if '/' in res_uri or '(' in res_uri:
            res_uri = re.sub(' ', '_', re.sub(r'\s*[(/].*', '', res_uri.lower()))
        res_uri = res_uri.lower()
        res = namespace[res_uri]
        g.add((res, RDF.type, SKOS.Concept))
        g.add((res, RDF.type, OWL.Class))
        g.add((res, SKOS.prefLabel, Literal(row_values[1])))
        g.add((res, SKOS.inScheme, scheme))
        g.add((res, SKOS.topConceptOf, scheme))
        g.add((scheme, SKOS.hasTopConcept, res))
        for cell in row[2:4]:
            if cell.value:
                g.add((res, SKOS.exactMatch, URIRef(cell.value)))
        if row_values[4]:
            for v in row_values[4].split('\n'):
                if strip(v):
                    g.add((res, RDFS.seeAlso, URIRef(strip(v))))
        g.add((res, CLIMOS_PROPS['usedInCLIMOS'], Literal(bool(strip(row_values[5]) == 'Y'))))

output_dir = Path('output')
output_dir.mkdir(parents=True, exist_ok=True)
g.serialize(output_dir / 'species.ttl')
