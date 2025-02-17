# CLIMOS Ontology

The CLIMOS Ontology is created from different sources that are assembled here:

## CLIMOS Ontology terms Google Spreadsheet

The spreadsheet can be found
[here](https://myogc1-my.sharepoint.com/:x:/g/personal/avillar_ogc_org/Ee4D7-XcVddNoKwi7F1tuuYBuxDX_u7ZaQI5QLjzqmxTgQ?e=4rp8xX).
It is periodically fetched and converted into RDF. The password to access this file can be found in the CLIMOS
SharePoint, inside 
[Documents » 03_General » WP3 Forecasting, Early Warning System and Tools » Editing the CLIMOS Ontology Spreadsheet.docx](https://ihmt.sharepoint.com/:w:/r/sites/CLIMOSProject/Documentos%20Partilhados/03_General/WP3%20Forecasting,%20Early%20Warning%20System%20and%20Tools/Editing%20the%20CLIMOS%20Ontology%20spreadsheet.docx?d=w2e0588ca736e4d11a4aaa9d88aefe3f1&csf=1&web=1&e=MPKLwz).

The document contains the following sheets:

* `SandflySpecies`: List of sandfly species in CLIMOS, including links to DBpedia and VEuPathDB.
* `ParasiteSpecies`: Like the above, but for parasites.
* `TrapProperties`: Properties for defining traps.
* `ObservationProperties`: observable properties used throughout the ontology and/or catalog.
* `Vocabularies`: List of controlled vocabularies.
* `Terms`: List of terms for the controlled vocabularies.

Please, follow these rules when editing the spreadsheet:

* Identifiers
  * Try to use lowercase letters and underscore-separated (`_`) words. Avoid special (i.e. non-ASCII)
    characters whenever possible.
  * Identifiers must generally be unique. For "Terms", identifiers must be unique within a given Vocabulary.
* AdditionalLinks: use only links to linked data (i.e., semantic) collections. Use the same cell for all links,
  separating them with a new line.
  * Examples (please copy the "ID" field/URL when using these):
    * [openBiodiv](https://openbiodiv.net/)
    * [NCBI Organismal Classification](https://bioportal.bioontology.org/ontologies/NCBITAXON?p=classes&conceptid=5661)
    * [Systematized Nomenclature of Medicine, Intl.](http://purl.bioontology.org/ontology/SNMI/L-50481)
    * [SNOMED CT](https://bioportal.bioontology.org/ontologies/SNOMEDCT?p=classes&conceptid=16043006)
    * [GBIF](https://www.gbif.org/species/3235457)
