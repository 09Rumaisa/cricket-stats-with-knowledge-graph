"""
Query RDF Dataset using SPARQL
"""

from rdflib import Graph

def load_and_query_rdf(rdf_file):
    """Load RDF file and execute sample queries"""
    
    # Load the RDF graph
    print(f"Loading RDF dataset from {rdf_file}...")
    g = Graph()
    g.parse(rdf_file, format='turtle')
    print(f"Loaded {len(g)} triples\n")
    
    # Query 1: Top 10 wicket-takers
    print("=" * 80)
    print("Query 1: Top 10 Wicket-Takers")
    print("=" * 80)
    
    query1 = """
    PREFIX cricket: <http://example.org/cricket/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?playerName ?teamName ?wickets ?matches
    WHERE {
      ?stats a cricket:BowlingStatistics ;
             cricket:forPlayer ?player ;
             cricket:forTeam ?team ;
             cricket:wickets ?wickets ;
             cricket:matches ?matches .
      ?player rdfs:label ?playerName .
      ?team rdfs:label ?teamName .
    }
    ORDER BY DESC(?wickets)
    LIMIT 10
    """
    
    results = g.query(query1)
    print(f"{'Player':<25} {'Team':<20} {'Wickets':<10} {'Matches':<10}")
    print("-" * 80)
    for row in results:
        print(f"{str(row.playerName):<25} {str(row.teamName):<20} {float(row.wickets):<10.0f} {float(row.matches):<10.0f}")
    
    # Query 2: Best economy rates (min 20 wickets)
    print("\n" + "=" * 80)
    print("Query 2: Best Economy Rates (minimum 20 wickets)")
    print("=" * 80)
    
    query2 = """
    PREFIX cricket: <http://example.org/cricket/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?playerName ?teamName ?economy ?wickets
    WHERE {
      ?stats a cricket:BowlingStatistics ;
             cricket:forPlayer ?player ;
             cricket:forTeam ?team ;
             cricket:economy ?economy ;
             cricket:wickets ?wickets .
      ?player rdfs:label ?playerName .
      ?team rdfs:label ?teamName .
      FILTER(?wickets >= 20)
    }
    ORDER BY ASC(?economy)
    LIMIT 10
    """
    
    results = g.query(query2)
    print(f"{'Player':<25} {'Team':<20} {'Economy':<10} {'Wickets':<10}")
    print("-" * 80)
    for row in results:
        print(f"{str(row.playerName):<25} {str(row.teamName):<20} {float(row.economy):<10.2f} {float(row.wickets):<10.0f}")
    
    # Query 3: Players with 5-wicket hauls
    print("\n" + "=" * 80)
    print("Query 3: Players with 5-Wicket Hauls")
    print("=" * 80)
    
    query3 = """
    PREFIX cricket: <http://example.org/cricket/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?playerName ?teamName ?fiveWickets ?bbi
    WHERE {
      ?stats a cricket:BowlingStatistics ;
             cricket:forPlayer ?player ;
             cricket:forTeam ?team ;
             cricket:fiveWickets ?fiveWickets ;
             cricket:bestBowlingInnings ?bbi .
      ?player rdfs:label ?playerName .
      ?team rdfs:label ?teamName .
      FILTER(?fiveWickets > 0)
    }
    ORDER BY DESC(?fiveWickets)
    """
    
    results = g.query(query3)
    print(f"{'Player':<25} {'Team':<20} {'5-Wickets':<12} {'Best Figures':<15}")
    print("-" * 80)
    for row in results:
        print(f"{str(row.playerName):<25} {str(row.teamName):<20} {float(row.fiveWickets):<12.0f} {str(row.bbi):<15}")
    
    # Query 4: Team-wise summary
    print("\n" + "=" * 80)
    print("Query 4: Team-wise Bowling Statistics Summary")
    print("=" * 80)
    
    query4 = """
    PREFIX cricket: <http://example.org/cricket/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?teamName (COUNT(DISTINCT ?player) AS ?totalPlayers) (SUM(?wickets) AS ?totalWickets) (AVG(?economy) AS ?avgEconomy)
    WHERE {
      ?stats a cricket:BowlingStatistics ;
             cricket:forPlayer ?player ;
             cricket:forTeam ?team ;
             cricket:wickets ?wickets ;
             cricket:economy ?economy .
      ?team rdfs:label ?teamName .
    }
    GROUP BY ?teamName
    ORDER BY DESC(?totalWickets)
    """
    
    results = g.query(query4)
    print(f"{'Team':<25} {'Players':<10} {'Total Wickets':<15} {'Avg Economy':<15}")
    print("-" * 80)
    for row in results:
        print(f"{str(row.teamName):<25} {int(row.totalPlayers):<10} {float(row.totalWickets):<15.0f} {float(row.avgEconomy):<15.2f}")

if __name__ == "__main__":
    rdf_file = "bowling_stats.ttl"
    load_and_query_rdf(rdf_file)
