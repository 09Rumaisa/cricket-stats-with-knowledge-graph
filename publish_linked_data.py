"""
Publish RDF Dataset as Linked Data
Simple Flask server with content negotiation
"""

from flask import Flask, request, Response, render_template_string
from rdflib import Graph
import os

app = Flask(__name__)

# Load RDF graph
g = Graph()
if os.path.exists("bowling_stats_improved.ttl"):
    g.parse("bowling_stats_improved.ttl", format="turtle")
elif os.path.exists("bowling_stats.ttl"):
    g.parse("bowling_stats.ttl", format="turtle")
else:
    print("Error: No RDF file found!")

# HTML template for human-readable view
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Cricket Bowling Statistics - Linked Data</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; }
        h1 { color: #2c3e50; }
        .info { background: #ecf0f1; padding: 20px; border-radius: 5px; }
        .endpoint { background: #3498db; color: white; padding: 10px; margin: 10px 0; }
        code { background: #f8f9fa; padding: 2px 5px; }
    </style>
</head>
<body>
    <h1>🏏 Cricket Bowling Statistics - Linked Data</h1>
    
    <div class="info">
        <h2>Dataset Information</h2>
        <p><strong>Total Triples:</strong> {{ triples }}</p>
        <p><strong>Format:</strong> RDF (Turtle, RDF/XML, JSON-LD)</p>
        <p><strong>License:</strong> CC BY 4.0</p>
    </div>
    
    <h2>Available Endpoints</h2>
    
    <div class="endpoint">
        <strong>GET /data</strong> - Get full dataset (supports content negotiation)
    </div>
    
    <div class="endpoint">
        <strong>GET /player/{player_name}</strong> - Get player information
    </div>
    
    <div class="endpoint">
        <strong>GET /team/{team_name}</strong> - Get team information
    </div>
    
    <div class="endpoint">
        <strong>GET /sparql</strong> - SPARQL endpoint (POST queries)
    </div>
    
    <h2>Content Negotiation</h2>
    <p>Use Accept header to get different formats:</p>
    <ul>
        <li><code>text/turtle</code> - Turtle format</li>
        <li><code>application/rdf+xml</code> - RDF/XML format</li>
        <li><code>application/ld+json</code> - JSON-LD format</li>
        <li><code>text/html</code> - Human-readable HTML</li>
    </ul>
    
    <h2>Example Usage</h2>
    <pre>
# Get data in Turtle format
curl -H "Accept: text/turtle" http://localhost:5000/data

# Get data in JSON-LD format
curl -H "Accept: application/ld+json" http://localhost:5000/data

# Query with SPARQL
curl -X POST http://localhost:5000/sparql \\
  -H "Content-Type: application/sparql-query" \\
  -d "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
    </pre>
    
    <h2>Links to External Datasets</h2>
    <ul>
        <li><a href="http://dbpedia.org/resource/Cricket">DBpedia - Cricket</a></li>
        <li><a href="http://www.wikidata.org/entity/Q5375">Wikidata - Cricket</a></li>
    </ul>
</body>
</html>
"""

@app.route('/')
def index():
    """Home page with dataset information"""
    return render_template_string(HTML_TEMPLATE, triples=len(g))

@app.route('/data')
def get_data():
    """Get full dataset with content negotiation"""
    accept = request.headers.get('Accept', 'text/turtle')
    
    if 'application/rdf+xml' in accept:
        return Response(g.serialize(format='xml'), mimetype='application/rdf+xml')
    elif 'application/ld+json' in accept or 'application/json' in accept:
        return Response(g.serialize(format='json-ld'), mimetype='application/ld+json')
    elif 'text/html' in accept:
        return index()
    else:  # Default to Turtle
        return Response(g.serialize(format='turtle'), mimetype='text/turtle')

@app.route('/player/<player_name>')
def get_player(player_name):
    """Get information about a specific player"""
    # Replace underscores with spaces for search
    search_name = player_name.replace('_', ' ')
    
    # Query for player data
    query = f"""
    PREFIX cricket: <http://example.org/cricket/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    CONSTRUCT {{
        ?player ?p ?o .
        ?stats ?sp ?so .
    }}
    WHERE {{
        ?player rdfs:label ?name .
        FILTER(CONTAINS(LCASE(?name), LCASE("{search_name}")))
        ?player ?p ?o .
        OPTIONAL {{
            ?stats cricket:forPlayer ?player ;
                   ?sp ?so .
        }}
    }}
    """
    
    result_graph = g.query(query).graph
    
    accept = request.headers.get('Accept', 'text/turtle')
    if 'application/rdf+xml' in accept:
        return Response(result_graph.serialize(format='xml'), mimetype='application/rdf+xml')
    elif 'application/ld+json' in accept:
        return Response(result_graph.serialize(format='json-ld'), mimetype='application/ld+json')
    else:
        return Response(result_graph.serialize(format='turtle'), mimetype='text/turtle')

@app.route('/team/<team_name>')
def get_team(team_name):
    """Get information about a specific team"""
    # Replace underscores with spaces for search
    search_name = team_name.replace('_', ' ')
    
    query = f"""
    PREFIX cricket: <http://example.org/cricket/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    CONSTRUCT {{
        ?team ?p ?o .
        ?player ?pp ?po .
    }}
    WHERE {{
        ?team rdfs:label ?name .
        FILTER(CONTAINS(LCASE(?name), LCASE("{search_name}")))
        ?team ?p ?o .
        OPTIONAL {{
            ?player cricket:playsFor ?team ;
                    ?pp ?po .
        }}
    }}
    """
    
    result_graph = g.query(query).graph
    
    accept = request.headers.get('Accept', 'text/turtle')
    if 'application/rdf+xml' in accept:
        return Response(result_graph.serialize(format='xml'), mimetype='application/rdf+xml')
    elif 'application/ld+json' in accept:
        return Response(result_graph.serialize(format='json-ld'), mimetype='application/ld+json')
    else:
        return Response(result_graph.serialize(format='turtle'), mimetype='text/turtle')

@app.route('/sparql', methods=['GET', 'POST'])
def sparql_endpoint():
    """SPARQL endpoint for querying the dataset"""
    if request.method == 'POST':
        query = request.data.decode('utf-8')
    else:
        query = request.args.get('query', '')
    
    if not query:
        return Response("No query provided", status=400)
    
    try:
        results = g.query(query)
        
        # Return results in SPARQL JSON format
        return Response(results.serialize(format='json'), mimetype='application/sparql-results+json')
    except Exception as e:
        return Response(f"Query error: {str(e)}", status=400)

if __name__ == '__main__':
    print("🚀 Starting Linked Data Server...")
    print(f"📊 Loaded {len(g)} triples")
    print("🌐 Server running at http://localhost:5000")
    print("\nPress Ctrl+C to stop")
    app.run(debug=True, port=5000)
