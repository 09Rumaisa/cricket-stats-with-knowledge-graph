"""
Enhanced CSV to RDF Converter using the Enhanced Ontology
"""

import csv
from datetime import datetime
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, RDFS, XSD, OWL, DCTERMS, FOAF

# Define namespaces
CRICKET = Namespace("http://example.org/cricket/ontology#")
PLAYER = Namespace("http://example.org/cricket/resource/player/")
TEAM = Namespace("http://example.org/cricket/resource/team/")
STATS = Namespace("http://example.org/cricket/resource/stats/")
SCHEMA = Namespace("http://schema.org/")
DBPEDIA = Namespace("http://dbpedia.org/resource/")

def clean_uri_string(s):
    """Clean string for use in URI following RFC 3986"""
    return s.replace(" ", "_").replace(".", "").replace("/", "_").replace("'", "")

def convert_to_float(value):
    """Convert string to float, return None if empty or invalid"""
    try:
        return float(value) if value and value.strip() else None
    except ValueError:
        return None

def classify_performance(wickets, economy):
    """Classify performance based on statistics"""
    if wickets and economy:
        if wickets >= 50 and economy < 7.5:
            return CRICKET.ExcellentPerformance
        elif wickets >= 20:
            return CRICKET.GoodPerformance
        elif wickets >= 10:
            return CRICKET.AveragePerformance
        else:
            return CRICKET.PoorPerformance
    return CRICKET.BowlingStatistics

def add_provenance(g, dataset_uri):
    
    # Use VOID vocabulary for dataset
    VOID = Namespace("http://rdfs.org/ns/void#")
    g.bind("void", VOID)
    
    g.add((dataset_uri, RDF.type, VOID.Dataset))
    g.add((dataset_uri, DCTERMS.title, Literal("Cricket Bowling Statistics Dataset", lang="en")))
    g.add((dataset_uri, DCTERMS.description, Literal("PSL bowling statistics using enhanced ontology", lang="en")))
    g.add((dataset_uri, DCTERMS.created, Literal(datetime.now().isoformat(), datatype=XSD.dateTime)))
    g.add((dataset_uri, DCTERMS.creator, Literal("Cricket Statistics Project")))
    g.add((dataset_uri, DCTERMS.source, Literal("bowlingAvg_clean.csv")))
    g.add((dataset_uri, DCTERMS.license, URIRef("http://creativecommons.org/licenses/by/4.0/")))

def convert_csv_to_rdf_enhanced(csv_file, output_file):
    """Convert CSV to RDF using enhanced ontology"""
    
    g = Graph()
    
    # Bind namespaces
    g.bind("cricket", CRICKET)
    g.bind("player", PLAYER)
    g.bind("team", TEAM)
    g.bind("stats", STATS)
    g.bind("schema", SCHEMA)
    g.bind("owl", OWL)
    g.bind("dcterms", DCTERMS)
    g.bind("foaf", FOAF)
    g.bind("dbpedia", DBPEDIA)
    
    # Add dataset metadata
    dataset_uri = URIRef("http://example.org/cricket/dataset/bowling-statistics")
    add_provenance(g, dataset_uri)
    
    # Read CSV file
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for idx, row in enumerate(reader):
            player_name = row['Player']
            team_name = row['Team Name']
            
            # Create URIs
            player_uri = PLAYER[clean_uri_string(player_name)]
            team_uri = TEAM[clean_uri_string(team_name)]
            stats_uri = STATS[f"bowling_stats_{idx}"]
            
            # Get statistics for classification
            wickets = convert_to_float(row['Wkts'])
            economy = convert_to_float(row['Econ'])
            
            # Classify performance
            performance_class = classify_performance(wickets, economy)
            
            # Player information (using enhanced ontology)
            g.add((player_uri, RDF.type, CRICKET.Player))
            g.add((player_uri, RDF.type, CRICKET.Bowler))  # All are bowlers in this dataset
            g.add((player_uri, RDF.type, SCHEMA.Person))
            g.add((player_uri, FOAF.name, Literal(player_name, datatype=XSD.string)))
            g.add((player_uri, RDFS.label, Literal(player_name, lang="en")))
            g.add((player_uri, CRICKET.playsFor, team_uri))
            g.add((player_uri, SCHEMA.memberOf, team_uri))
            
            # Team information (using enhanced ontology)
            g.add((team_uri, RDF.type, CRICKET.Team))
            g.add((team_uri, RDF.type, CRICKET.PSLTeam))  # PSL team type
            g.add((team_uri, RDF.type, SCHEMA.SportsTeam))
            g.add((team_uri, SCHEMA.name, Literal(team_name, datatype=XSD.string)))
            g.add((team_uri, RDFS.label, Literal(team_name, lang="en")))
            g.add((team_uri, SCHEMA.sport, DBPEDIA.Cricket))
            g.add((team_uri, CRICKET.hasPlayer, player_uri))  # Inverse property
            
            # Bowling statistics (with performance classification)
            g.add((stats_uri, RDF.type, CRICKET.BowlingStatistics))
            g.add((stats_uri, RDF.type, performance_class))  # Add performance classification
            g.add((stats_uri, CRICKET.forPlayer, player_uri))
            g.add((stats_uri, CRICKET.forTeam, team_uri))
            # Link to dataset using Dublin Core
            g.add((stats_uri, DCTERMS.source, dataset_uri))
            
            # Add span
            if row['Span']:
                g.add((stats_uri, CRICKET.span, Literal(row['Span'], datatype=XSD.string)))
            
            # Add numeric statistics with proper datatypes
            numeric_fields = {
                'Mat': ('matches', XSD.integer),
                'Inns': ('innings', XSD.float),
                'Overs': ('overs', XSD.float),
                'Mdns': ('maidens', XSD.float),
                'Runs': ('runsConceded', XSD.float),
                'Wkts': ('wickets', XSD.float),
                'Ave': ('average', XSD.float),
                'Econ': ('economy', XSD.float),
                'SR': ('strikeRate', XSD.float),
                '4': ('fourWickets', XSD.float),
                '5': ('fiveWickets', XSD.float),
                'Ct': ('catches', XSD.integer),
                'St': ('stumpings', XSD.integer)
            }
            
            for csv_field, (rdf_property, datatype) in numeric_fields.items():
                value = convert_to_float(row[csv_field])
                if value is not None:
                    g.add((stats_uri, CRICKET[rdf_property], Literal(value, datatype=datatype)))
            
            # Add best bowling innings
            if row['BBI']:
                g.add((stats_uri, CRICKET.bestBowlingInnings, Literal(row['BBI'], datatype=XSD.string)))
    
    # Serialize to multiple formats
    g.serialize(destination=output_file, format='turtle')
    g.serialize(destination=output_file.replace('.ttl', '.rdf'), format='xml')
    g.serialize(destination=output_file.replace('.ttl', '.jsonld'), format='json-ld')
    
    print(f"✓ Enhanced RDF dataset created successfully!")
    print(f"  - Turtle: {output_file}")
    print(f"  - RDF/XML: {output_file.replace('.ttl', '.rdf')}")
    print(f"  - JSON-LD: {output_file.replace('.ttl', '.jsonld')}")
    print(f"  - Total triples: {len(g)}")
    
    # Count performance classifications
    excellent = len(list(g.subjects(RDF.type, CRICKET.ExcellentPerformance)))
    good = len(list(g.subjects(RDF.type, CRICKET.GoodPerformance)))
    average = len(list(g.subjects(RDF.type, CRICKET.AveragePerformance)))
    poor = len(list(g.subjects(RDF.type, CRICKET.PoorPerformance)))
    
    print(f"\n  Performance Classifications:")
    print(f"    - Excellent: {excellent}")
    print(f"    - Good: {good}")
    print(f"    - Average: {average}")
    print(f"    - Poor: {poor}")
    
    return g

if __name__ == "__main__":
    input_csv = "bowlingAvg_clean.csv"
    output_rdf = "bowling_stats_enhanced.ttl"
    
    graph = convert_csv_to_rdf_enhanced(input_csv, output_rdf)
