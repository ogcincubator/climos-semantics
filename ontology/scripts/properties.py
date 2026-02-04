import re
import sys
from pathlib import Path
from typing import Any

from openpyxl import load_workbook
from rdflib import Namespace, URIRef, Graph, RDF, SKOS, OWL, Literal, RDFS

import warnings
warnings.filterwarnings("ignore")


CONCEPT_SCHEMES: list[dict[str, Any]] = [
    {
        'id': 'trap',
        'name': 'Trap properties',
        'ws': 'TrapProperties',
    },
    {
        'id': 'observation',
        'name': 'Observation properties',
        'ws': 'ObservationProperties',
    }
]

CLIMOS = Namespace('https://w3id.org/climos/')
CLIMOS_PROPS = Namespace(CLIMOS['properties/'])
CLIMOS_VOCABS = Namespace(CLIMOS['vocabs/'])

wb = load_workbook(filename=sys.argv[1], read_only=True, data_only=True)

output_dir = Path('output')
output_dir.mkdir(parents=True, exist_ok=True)

for cs_def in CONCEPT_SCHEMES:
    ws = wb[cs_def['ws']]

    g = Graph()
    g.bind('climos', CLIMOS)
    g.bind('climos-props', CLIMOS_PROPS)

    namespace = Namespace(f"https://w3id.org/climos/properties/{cs_def['id']}/")
    g.bind(cs_def['id'], namespace)

    scheme = URIRef(f"https://w3id.org/climos/properties/{cs_def['id']}")
    g.add((scheme, RDF.type, SKOS.ConceptScheme))
    g.add((scheme, SKOS.prefLabel, Literal(cs_def['name'])))

    for i, row in enumerate(ws.rows):
        if i == 0:
            continue

        row_values = [c.value.strip() if c.value else '' for c in row]

        if not any(row_values):
            continue

        res_uri = row_values[0].lower()
        if not res_uri or not res_uri.strip():
            raise ValueError(f"Invalid URI identifier at {cs_def['ws']} row {i}")
        if '/' in res_uri or '(' in res_uri:
            res_uri = re.sub(' ', '_', re.sub(r'\s*[(/].*', '', res_uri.lower()))
        res = namespace[res_uri]
        g.add((res, RDF.type, SKOS.Concept))
        g.add((res, RDF.type, RDF.Property))
        g.add((res, SKOS.inScheme, scheme))
        g.add((res, SKOS.topConceptOf, scheme))
        g.add((scheme, SKOS.hasTopConcept, res))
        g.add((res, SKOS.prefLabel, Literal(row_values[1])))
        if row_values[2]:
            g.add((res, SKOS.definition, Literal(row_values[2])))

        if len(row_values) > 3 and row_values[3]:
            g.add((res, RDFS.range, CLIMOS_VOCABS[row_values[3]]))
        if len(row_values) > 4 and row_values[4]:
            g.add((res, RDFS.seeAlso, URIRef(row_values[3])))
        if len(row_values) > 5 and row_values[5] and row_values[5].strip() == 'Y':
            g.add((res, CLIMOS_PROPS['usedInCLIMOS'], Literal(True)))


    fn = output_dir.joinpath(f"props-{cs_def['id']}.ttl")
    g.serialize(fn)
