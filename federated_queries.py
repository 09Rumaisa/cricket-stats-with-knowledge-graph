"""
Federated SPARQL Queries
Query local dataset + external sources (DBpedia, Wikidata)
"""

from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph
import json

def query_local_and_dbpedia():
    """
    Federated query combining local data with DBpedia
    Gets player statistics and their Wikipedia abstracts
    """
    
    # Load local graph
    g = Graph()
    try:
        g.parse("bowling_stats_enhanced_linked.ttl", format="turtle")
    except:
        try:
            g.parse("bowling_stats_linked.ttl", format="turtle")
        except:
            g.parse("bowling_stats_enhanced.ttl", format="turtle")
    
    print("=" * 80)
    print("Federated Query 1: Local Data + DBpedia")
    print("Get player statistics with Wikipedia information")
    print("=" * 80)
    
    # This query would work if we had a SPARQL endpoint
    # For demonstration, we'll query DBpedia separately
    
    query = """
    PREFIX cricket: <http://example.org/cricket/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX owl: <http://www.w3.org/2001/02/22-rdf-syntax-ns#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    
    SELECT ?playerName ?wickets ?dbpediaResource ?abstract
    WHERE {
        # Local data
        ?player a cricket:Player ;
                rdfs:label ?playerName .
        ?stats cricket:forPlayer ?player ;
               cricket:wickets ?wickets .
        
        # Link to DBpedia
        OPTIONAL {
            ?player owl:sameAs ?dbpediaResource .
            FILTER(STRSTARTS(STR(?dbpediaResource), "http://dbpedia.org/"))
            
            # Federated query to DBpedia
            SERVICE <http://dbpedia.org/sparql> {
                ?dbpediaResource dbo:abstract ?abstract .
                FILTER(LANG(?abstract) = "en")
            }
        }
    }
    ORDER BY DESC(?wickets)
    LIMIT 10
    """
    
    print("\nQuery:")
    print(query)
    print("\nNote: This requires a SPARQL endpoint. See example below for manual federation.\n")

def query_dbpedia_for_players():
    """Query DBpedia for cricket player information"""
    
    print("=" * 80)
    print("Example: Querying DBpedia for Cricket Players")
    print("=" * 80)
    
    sparql = SPARQLWrapper("http://dbpedia.org/sparql")
    
    query = """
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX dbp: <http://dbpedia.org/property/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?player ?name ?birthDate ?country
    WHERE {
        ?player a dbo:Cricketer ;
                rdfs:label ?name ;
                dbo:birthDate ?birthDate .
        OPTIONAL { ?player dbo:country ?country }
        
        FILTER(LANG(?name) = "en")
        FILTER(CONTAINS(?name, "Shaheen") || CONTAINS(?name, "Afridi"))
    }
    LIMIT 5
    """
    
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    
    try:
        results = sparql.query().convert()
        
        print("\nResults from DBpedia:")
        print("-" * 80)
        for result in results["results"]["bindings"]:
            name = result.get("name", {}).get("value", "N/A")
            birth = result.get("birthDate", {}).get("value", "N/A")
            country = result.get("country", {}).get("value", "N/A")
            print(f"Player: {name}")
            print(f"  Birth Date: {birth}")
            print(f"  Country: {country}")
            print()
    except Exception as e:
        print(f"Error querying DBpedia: {e}")
        print("Note: DBpedia endpoint may be unavailable or rate-limited")

def create_federated_query_examples():
    """Create example federated queries for documentation"""
    
    queries = {
        "Query 1: Local + DBpedia - Player Info": """
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2001/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>

SELECT ?playerName ?wickets ?birthDate ?abstract
WHERE {
    # Local dataset
    ?player a cricket:Player ;
            rdfs:label ?playerName ;
            owl:sameAs ?dbpediaURI .
    ?stats cricket:forPlayer ?player ;
           cricket:wickets ?wickets .
    
    # DBpedia
    SERVICE <http://dbpedia.org/sparql> {
        ?dbpediaURI dbo:birthDate ?birthDate ;
                    dbo:abstract ?abstract .
        FILTER(LANG(?abstract) = "en")
    }
}
ORDER BY DESC(?wickets)
LIMIT 10
""",
        
        "Query 2: Local + Wikidata - Team Info": """
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2001/02/22-rdf-syntax-ns#>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX wd: <http://www.wikidata.org/entity/>

SELECT ?teamName ?totalWickets ?inception ?country
WHERE {
    # Local dataset
    ?team a cricket:Team ;
          rdfs:label ?teamName ;
          owl:sameAs ?wikidataURI .
    
    {
        SELECT ?team (SUM(?wickets) as ?totalWickets)
        WHERE {
            ?stats cricket:forTeam ?team ;
                   cricket:wickets ?wickets .
        }
        GROUP BY ?team
    }
    
    # Wikidata
    SERVICE <https://query.wikidata.org/sparql> {
        ?wikidataURI wdt:P571 ?inception ;
                     wdt:P17 ?countryURI .
        ?countryURI rdfs:label ?country .
        FILTER(LANG(?country) = "en")
    }
}
ORDER BY DESC(?totalWickets)
""",
        
        "Query 3: Compare Local Stats with DBpedia Career Stats": """
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2001/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX dbp: <http://dbpedia.org/property/>

SELECT ?playerName ?localWickets ?careerWickets ?economy
WHERE {
    # Local PSL statistics
    ?player a cricket:Player ;
            rdfs:label ?playerName ;
            owl:sameAs ?dbpediaURI .
    ?stats cricket:forPlayer ?player ;
           cricket:wickets ?localWickets ;
           cricket:economy ?economy .
    
    # DBpedia career statistics
    SERVICE <http://dbpedia.org/sparql> {
        ?dbpediaURI dbp:bowling ?careerWickets .
    }
    
    FILTER(?localWickets > 50)
}
ORDER BY DESC(?localWickets)
""",
        
        "Query 4: Multi-source Federation": """
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX owl: <http://www.w3.org/2001/02/22-rdf-syntax-ns#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX schema: <http://schema.org/>

SELECT ?playerName ?wickets ?dbpediaAbstract ?wikidataImage ?teamName
WHERE {
    # Local data
    ?player a cricket:Player ;
            rdfs:label ?playerName ;
            cricket:playsFor ?team .
    ?team rdfs:label ?teamName .
    ?stats cricket:forPlayer ?player ;
           cricket:wickets ?wickets .
    
    # DBpedia for biography
    OPTIONAL {
        ?player owl:sameAs ?dbpediaURI .
        FILTER(STRSTARTS(STR(?dbpediaURI), "http://dbpedia.org/"))
        
        SERVICE <http://dbpedia.org/sparql> {
            ?dbpediaURI dbo:abstract ?dbpediaAbstract .
            FILTER(LANG(?dbpediaAbstract) = "en")
        }
    }
    
    # Wikidata for images
    OPTIONAL {
        ?player owl:sameAs ?wikidataURI .
        FILTER(STRSTARTS(STR(?wikidataURI), "http://www.wikidata.org/"))
        
        SERVICE <https://query.wikidata.org/sparql> {
            ?wikidataURI wdt:P18 ?wikidataImage .
        }
    }
}
ORDER BY DESC(?wickets)
LIMIT 20
"""
    }
    
    # Save queries to file
    with open("federated_queries.sparql", "w") as f:
        for title, query in queries.items():
            f.write(f"# {title}\n")
            f.write("# " + "=" * 70 + "\n\n")
            f.write(query)
            f.write("\n\n" + "=" * 80 + "\n\n")
    
    print("=" * 80)
    print("Federated SPARQL Query Examples Created")
    print("=" * 80)
    print("\nSaved to: federated_queries.sparql")
    print("\nThese queries demonstrate:")
    print("  1. Combining local bowling stats with DBpedia player biographies")
    print("  2. Enriching team data with Wikidata information")
    print("  3. Comparing local tournament stats with career statistics")
    print("  4. Multi-source federation (Local + DBpedia + Wikidata)")
    print("\nNote: Requires SPARQL endpoint to execute federated queries")

if __name__ == "__main__":
    # Create example queries
    create_federated_query_examples()
    
    print("\n")
    
    # Try querying DBpedia
    try:
        query_dbpedia_for_players()
    except Exception as e:
        print(f"Could not query DBpedia: {e}")
    
    print("\n")
    
    # Show federated query structure
    query_local_and_dbpedia()
