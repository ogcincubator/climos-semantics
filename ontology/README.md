# CLIMOS Ontology

The CLIMOS Ontology is created from different sources that are assembled here:

## CLIMOS Ontology terms Google Spreadsheet

The spreadsheet can be found
[here](https://docs.google.com/spreadsheets/d/1TVoj5XaZXaJJcT72INzI15fb-gUSZ3NiQoLr72yAmZ0/edit?usp=sharing).
It is periodically fetched and converted into RDF.

The document contains 4 sheets:

* SandflySpecies: List of sandfly species in CLIMOS, including links to DBpedia and VEuPathDB.
* ParasiteSpecies: Like the above, but for parasites.
* ObservableProperties: observable properties used throughout the ontology and/or catalog.

Please, follow these rules when editing the spreadsheet:

* Identifiers: try to use lowercase letters and underscore-separated (`_`) words. Avoid special (i.e. non-ASCII)
  characters whenever possible.
* AdditionalLinks: use only links to linked data (i.e., semantic) collections. Use the same cell for all links,
  separating them with a new line.

