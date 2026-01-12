"""
Add links to external Linked Open Data sources
Works with enhanced ontology
Links to: DBpedia, Wikidata, Schema.org
"""

import os
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, OWL

def add_external_links_enhanced(input_file, output_file):
    """Add owl:sameAs links to external LOD sources"""
    
    g = Graph()
    g.parse(input_file, format="turtle")
    
    # Define namespaces
    CRICKET = Namespace("http://example.org/cricket/ontology#")
    PLAYER = Namespace("http://example.org/cricket/resource/player/")
    TEAM = Namespace("http://example.org/cricket/resource/team/")
    DBPEDIA = Namespace("http://dbpedia.org/resource/")
    WIKIDATA = Namespace("http://www.wikidata.org/entity/")
    
    g.bind("dbpedia", DBPEDIA)
    g.bind("wikidata", WIKIDATA)
    g.bind("owl", OWL)
    
    # Map teams to DBpedia/Wikidata
    team_mappings = {
        "Islamabad_United": {
            "dbpedia": "Islamabad_United",
            "wikidata": "Q6078588"
        },
        "Karachi_Kings": {
            "dbpedia": "Karachi_Kings",
            "wikidata": "Q6369184"
        },
        "Lahore_Qalanders": {
            "dbpedia": "Lahore_Qalandars",
            "wikidata": "Q6481751"
        },
        "Multan_Sultans": {
            "dbpedia": "Multan_Sultans",
            "wikidata": "Q30348643"
        },
        "Peshawar_Zalmi": {
            "dbpedia": "Peshawar_Zalmi",
            "wikidata": "Q20675330"
        },
        "Quetta_Gladiators": {
            "dbpedia": "Quetta_Gladiators",
            "wikidata": "Q20675331"
        }
    }
    
    # Add team links
    for team_name, links in team_mappings.items():
        team_uri = TEAM[team_name]
        
        if links.get("dbpedia"):
            g.add((team_uri, OWL.sameAs, DBPEDIA[links["dbpedia"]]))
        
        if links.get("wikidata"):
            g.add((team_uri, OWL.sameAs, WIKIDATA[links["wikidata"]]))
    
    # Map famous players to DBpedia/Wikidata
    player_mappings = {
        "Shaheen_Shah_Afridi": {
            "dbpedia": "Shaheen_Afridi",
            "wikidata": "Q28660671"
        },
        "Shadab_Khan": {
            "dbpedia": "Shadab_Khan",
            "wikidata": "Q28660670"
        },
        "Haris_Rauf": {
            "dbpedia": "Haris_Rauf",
            "wikidata": "Q56241916"
        },
        "Mohammad_Amir": {
            "dbpedia": "Mohammad_Amir",
            "wikidata": "Q3520391"
        },
        "Wahab_Riaz": {
            "dbpedia": "Wahab_Riaz",
            "wikidata": "Q3520392"
        },
        "Imran_Tahir": {
            "dbpedia": "Imran_Tahir",
            "wikidata": "Q3520393"
        },
        "Shahid_Afridi": {
            "dbpedia": "Shahid_Afridi",
            "wikidata": "Q3520394"
        },
        "Shoaib_Malik": {
            "dbpedia": "Shoaib_Malik",
            "wikidata": "Q3520395"
        },
        "Mohammad_Hafeez": {
            "dbpedia": "Mohammad_Hafeez",
            "wikidata": "Q3520396"
        }
    }
    
    # Add player links
    for player_name, links in player_mappings.items():
        player_uri = PLAYER[player_name]
        
        if links.get("dbpedia"):
            g.add((player_uri, OWL.sameAs, DBPEDIA[links["dbpedia"]]))
        
        if links.get("wikidata"):
            g.add((player_uri, OWL.sameAs, WIKIDATA[links["wikidata"]]))
    
    # Add general cricket concept links
    cricket_uri = URIRef("http://example.org/cricket/ontology#Cricket")
    g.add((cricket_uri, RDF.type, OWL.Class))
    g.add((cricket_uri, RDFS.label, Literal("Cricket")))
    g.add((cricket_uri, OWL.sameAs, DBPEDIA.Cricket))
    g.add((cricket_uri, OWL.sameAs, WIKIDATA.Q5375))
    
    # Save enhanced dataset
    g.serialize(destination=output_file, format="turtle")
    
    print(f"✓ Added external links to enhanced dataset")
    print(f"  - Output: {output_file}")
    print(f"  - Total triples: {len(g)}")
    print(f"  - Teams linked: {len(team_mappings)}")
    print(f"  - Players linked: {len(player_mappings)}")
    
    return g

if __name__ == "__main__":
    input_file = "bowling_stats_enhanced.ttl" if os.path.exists("bowling_stats_enhanced.ttl") else "bowling_stats.ttl"
    output_file = "bowling_stats_enhanced_linked.ttl"
    
    add_external_links_enhanced(input_file, output_file)
