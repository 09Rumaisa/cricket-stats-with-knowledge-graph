# Cricket Bowling Statistics Knowledge Graph

A semantic web pipeline that builds an OWL ontology for Pakistan Super League bowling data, converts the cleaned CSV into RDF, enriches it with external links (DBpedia/Wikidata), validates competency questions, and ships visualizations plus a small web dashboard.

## Repository Highlights
- Ontology authoring: [create_enhanced_ontology.py](create_enhanced_ontology.py) defines 23 classes, cardinalities, enumerations, unions/intersections, complements, functional and inverse-functional properties, and saves OWL/Turtle outputs.
- Data conversion: [improved_converter_enhanced.py](improved_converter_enhanced.py) maps `bowlingAvg_clean.csv` to RDF, classifies performance (Excellent/Good/Average/Poor), and emits Turtle/RDF/XML/JSON-LD.
- External linking: [add_external_links_enhanced.py](add_external_links_enhanced.py) and [add_more_external_links.py](add_more_external_links.py) attach `owl:sameAs` links for PSL teams and notable players to DBpedia/Wikidata.
- Validation: [validate_competency_questions.py](validate_competency_questions.py) checks coverage of the competency questions in [COMPETENCY_QUESTIONS.md](COMPETENCY_QUESTIONS.md).
- Federated queries: [federated_queries.py](federated_queries.py) writes examples to [federated_queries.sparql](federated_queries.sparql) and demonstrates DBpedia/Wikidata calls.
- Visuals: [create_visualizations.py](create_visualizations.py) renders PNG charts; [visualize_graph_networkx.py](visualize_graph_networkx.py) draws ontology/data/link graphs.
- Apps: [publish_linked_data.py](publish_linked_data.py) serves the graph with content negotiation; [cricket_stats_professional_app.py](cricket_stats_professional_app.py) offers a PSL bowling dashboard over the RDF graph.

## Prerequisites
- Python 3.10+ recommended
- Install dependencies: `pip install -r requirements.txt`

## Quickstart
1. Ensure the input CSV `bowlingAvg_clean.csv` is present in the repo root.
2. Run the full pipeline: `python run_enhanced_pipeline.py`
   - Generates `cricket_ontology_enhanced.owl`, `cricket_ontology_enhanced.ttl`, `bowling_stats_enhanced.{ttl,rdf,jsonld}`, and `bowling_stats_enhanced_linked.ttl`.
3. (Optional) Expand external links: `python add_more_external_links.py` to add more `owl:sameAs` mappings for famous PSL players.
4. Validate questions: `python validate_competency_questions.py` to confirm all competency categories are answerable.

## Key Scripts & Usage
- Ontology creation: `python create_enhanced_ontology.py` to regenerate the ontology files.
- CSV → RDF: `python improved_converter_enhanced.py` if you just want fresh RDF outputs without the full pipeline.
- External links: `python add_external_links_enhanced.py` (baseline links) then `python add_more_external_links.py` (extended coverage).
- Visualization bundle: `python create_visualizations.py` to create `viz_*.png` charts; `python visualize_graph_networkx.py` for graph diagrams and stats.
- Query helpers: `python query_rdf.py` runs sample SPARQL queries over the dataset; see [sample_queries.sparql](sample_queries.sparql) for reusable snippets.
- Federated examples: `python federated_queries.py` to regenerate `federated_queries.sparql` and optionally hit DBpedia.
- Linked Data server: `python publish_linked_data.py` starts a Flask app with `/data`, `/player/<name>`, `/team/<name>`, and `/sparql` endpoints (defaults to `bowling_stats_improved.ttl` or `bowling_stats.ttl`).
- Dashboard: `python cricket_stats_professional_app.py` launches a PSL bowling UI (top wicket takers, best economies, 5-fors, team stats, search) backed by the RDF graph with DBpedia/Wikidata links.

## Data & Outputs
- Input: `bowlingAvg_clean.csv` (PSL bowling statistics).
- Ontology artifacts: `cricket_ontology_enhanced.owl`, `cricket_ontology_enhanced.ttl`.
- RDF datasets: `bowling_stats_enhanced.ttl`, `bowling_stats_enhanced.rdf`, `bowling_stats_enhanced.jsonld`, `bowling_stats_enhanced_linked.ttl`.
- Visuals: `viz_*.png` charts plus `ontology_class_hierarchy_graph.png`, `data_relationships_graph.png`, `external_links_graph.png`.

## SPARQL Resources
- Competency coverage and queries: [COMPETENCY_QUESTIONS.md](COMPETENCY_QUESTIONS.md)
- Local query snippets: [sample_queries.sparql](sample_queries.sparql)
- Federated patterns: [federated_queries.sparql](federated_queries.sparql)

## Notes
- Namespaces center on `http://example.org/cricket/ontology#` with player/team/stats resources under corresponding paths.
- Functional/inverse-functional properties, cardinalities, unions/intersections, complements, and enumeration (TeamType) are modeled to meet the coursework requirements.
- External links use `owl:sameAs` to DBpedia and Wikidata URIs to enable federated querying and richer UI linking.
