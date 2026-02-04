import re
import sys
from pathlib import Path

from openpyxl import load_workbook
from rdflib import Namespace, URIRef, Graph, RDF, SKOS, OWL, Literal, RDFS

from climos_utils import strip

import warnings
warnings.filterwarnings("ignore")


CLIMOS = Namespace('https://w3id.org/climos/')
CLIMOS_VOCABS = Namespace(CLIMOS['vocabs/'])

wb = load_workbook(filename=sys.argv[1], read_only=True, data_only=True)


vocabs_ws = wb['Vocabularies']
terms_ws = wb['Terms']

graphs: dict[str, tuple[Graph, Namespace]] = {}

for i, row in enumerate(vocabs_ws.rows):
    if i == 0:
        continue

    row_values = [strip(c.value) if c.value else '' for c in row]

    if not any(row_values):
        continue

    res_uri = row_values[0].capitalize()
    res = CLIMOS_VOCABS[res_uri]

    g = Graph()
    g.bind('climos', CLIMOS)
    g.bind('climos-vocabs', CLIMOS_VOCABS)
    g.bind(res_uri, str(res) + '/')

    g.add((res, RDF.type, SKOS.ConceptScheme))
    g.add((res, RDF.type, OWL.Class))
    g.add((res, SKOS.prefLabel, Literal(row_values[1])))
    if row_values[2]:
        g.add((res, SKOS.definition, Literal(row_values[2])))

    graphs[res_uri] = g, Namespace(str(res) + '/')

for i, row in enumerate(terms_ws.rows):
    if i == 0:
        continue

    row_values = [c.value.strip() if c.value else '' for c in row]

    if not any(row_values):
        continue

    vocab_uri = row_values[0].capitalize()
    g, namespace = graphs[vocab_uri]

    res_uri = row_values[1].lower()
    res = namespace[res_uri]

    g.add((res, RDF.type, SKOS.Concept))
    g.add((res, RDF.type, CLIMOS_VOCABS[vocab_uri]))
    g.add((res, SKOS.prefLabel, Literal(row_values[2])))

    if len(row_values) > 3 and row_values[3]:
        g.add((res, SKOS.broader, namespace[row_values[3]]))
        g.add((namespace[row_values[3]], SKOS.narrower, res))
    else:
        g.add((res, SKOS.topConceptOf, CLIMOS_VOCABS[vocab_uri]))
        g.add((CLIMOS_VOCABS[vocab_uri], SKOS.hasTopConcept, res))

    if len(row_values) > 4 and row_values[4]:
        g.add((res, SKOS.definition, Literal(row_values[4])))

    if len(row_values) > 5 and row_values[5]:
        for v in row_values[5].split('\n'):
            if strip(v):
                g.add((res, RDFS.seeAlso, URIRef(strip(v))))

output_dir = Path('output')
output_dir.mkdir(parents=True, exist_ok=True)

for g, namespace in graphs.values():
    fn = output_dir.joinpath(re.sub(r'.*/([^/]+)/?$', 'vocab-\\1', str(namespace))).with_suffix('.ttl')
    g.serialize(fn)