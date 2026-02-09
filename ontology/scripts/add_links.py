import time
from argparse import ArgumentParser
from pathlib import Path
from typing import cast
from urllib.parse import urljoin

from rdflib import Graph, RDF, SKOS, URIRef, RDFS, Literal, Variable, BNode

import requests
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:147.0) Gecko/20100101 Firefox/147.0',
}

OPENBIODIV_QUERY = '''
SELECT distinct ?s WHERE {
    SERVICE <https://graph.openbiodiv.net/repositories/openbiodiv-v2> {
        ?s <http://rs.tdwg.org/dwc/terms/genus> "__GENUS__" ;
          <http://rs.tdwg.org/dwc/terms/specificEpithet> "__EPITHET__" ;
        .
    }
}
'''


if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument("file", nargs='+', help="Input file", type=Path)
    args = parser.parse_args()

    for fn in args.file:
        g = Graph().parse(fn)
        links_g = Graph()

        for s in g.subjects(RDF.type, SKOS.Concept):
            label = str(cast(Literal, g.value(s, SKOS.prefLabel)).value)
            print(label)

            r = requests.get(
                'https://www.ecdc.europa.eu/en/search',
                params={
                    's': label,
                    'items_per_page': 50,
                },
                headers=HEADERS,
            )
            soup = BeautifulSoup(r.text, 'html.parser')

            links = soup.css.select('.view-content .node .card__header a.card-link')
            if links:
                links_g.add((s, RDFS.seeAlso, URIRef(r.url)))
                for link in links:
                    links_g.add((s, RDFS.seeAlso, URIRef(urljoin(r.url, link['href']))))

            if (name_parts := label.split(' ')) and len(name_parts) == 2:
                bindings = links_g.query(OPENBIODIV_QUERY
                              .replace('__GENUS__', name_parts[0])
                              .replace('__EPITHET__', name_parts[1])
                ).bindings
                if bindings:
                    for binding in bindings:
                        links_g.add((s, SKOS.exactMatch, binding.get(Variable('s'))))

            time.sleep(3)

        links_g.add((BNode(),
                     URIRef('http://www.opengis.net/ogc-na#targetGraph'),
                     URIRef('https://w3id.org/climos/species-links')))
        links_g.serialize(fn.with_stem(f"{fn.stem}_links"))


