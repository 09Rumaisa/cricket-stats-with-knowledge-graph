"""
Professional Cricket Statistics Dashboard
End User Application with Graph Backend - Linked to DBpedia & Wikidata
"""

from flask import Flask, render_template_string, request, jsonify
from rdflib import Graph, Namespace
from rdflib.namespace import OWL, RDFS, RDF
import os

app = Flask(__name__)

# Load RDF graph
g = Graph()
if os.path.exists("bowling_stats_enhanced_linked.ttl"):
    g.parse("bowling_stats_enhanced_linked.ttl", format="turtle")
elif os.path.exists("bowling_stats_enhanced.ttl"):
    g.parse("bowling_stats_enhanced.ttl", format="turtle")

print(f"✓ Loaded {len(g)} triples")
print(f"✓ External links: {len(list(g.triples((None, OWL.sameAs, None))))}")

# HTML Template will be added via fsAppend
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>PSL Cricket Statistics Dashboard</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .header {
            text-align: center;
            color: white;
            padding: 30px 0;
            margin-bottom: 30px;
        }
        
        .header h1 {
            font-size: 42px;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header .subtitle {
            font-size: 16px;
            opacity: 0.9;
        }
        
        .badges {
            display: flex;
            justify-content: center;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        
        .badge {
            padding: 8px 16px;
            border-radius: 20px;
            font-size: 13px;
            font-weight: 600;
        }
        
        .badge-rdf { background: #4CAF50; color: white; }
        .badge-dbpedia { background: #FF5722; color: white; }
        .badge-wikidata { background: #00BCD4; color: white; }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .stats-overview {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            text-align: center;
            transition: transform 0.3s;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        
        .stat-card .icon {
            font-size: 36px;
            margin-bottom: 10px;
        }
        
        .stat-card .number {
            font-size: 42px;
            font-weight: bold;
            color: #1e3c72;
            margin: 10px 0;
        }
        
        .stat-card .label {
            color: #666;
            font-size: 14px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }
        
        .tab-button {
            padding: 12px 24px;
            background: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 15px;
            font-weight: 600;
            transition: all 0.3s;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .tab-button:hover {
            background: #f0f0f0;
        }
        
        .tab-button.active {
            background: #1e3c72;
            color: white;
        }
        
        .tab-content {
            display: none;
            background: white;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .tab-content.active {
            display: block;
            animation: fadeIn 0.3s;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .section-title {
            font-size: 24px;
            color: #1e3c72;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 3px solid #1e3c72;
        }
        
        .search-box {
            margin-bottom: 25px;
            display: flex;
            gap: 10px;
        }
        
        .search-box input {
            flex: 1;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #ddd;
            border-radius: 8px;
            transition: border-color 0.3s;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: #1e3c72;
        }
        
        .search-box button {
            padding: 12px 30px;
            background: #1e3c72;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .search-box button:hover {
            background: #2a5298;
        }
        
        table {
            width: 100%;
            border-collapse: collapse;
        }
        
        thead {
            background: #1e3c72;
            color: white;
        }
        
        th {
            padding: 15px;
            text-align: left;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 13px;
            letter-spacing: 0.5px;
        }
        
        td {
            padding: 15px;
            border-bottom: 1px solid #eee;
        }
        
        tbody tr:hover {
            background: #f8f9fa;
        }
        
        .rank {
            font-weight: bold;
            color: #1e3c72;
            font-size: 18px;
        }
        
        .rank-1 { color: #FFD700; }
        .rank-2 { color: #C0C0C0; }
        .rank-3 { color: #CD7F32; }
        
        .player-name {
            font-weight: 600;
            color: #333;
        }
        
        .external-link {
            display: inline-block;
            padding: 4px 10px;
            margin: 2px;
            background: #1e3c72;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-size: 12px;
            transition: background 0.3s;
        }
        
        .external-link:hover {
            background: #2a5298;
        }
        
        .no-links {
            color: #999;
            font-size: 13px;
        }
        
        .highlight-box {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin: 20px 0;
            border-radius: 4px;
        }
        
        .highlight-box strong {
            color: #1976D2;
        }
        
        .footer {
            text-align: center;
            color: white;
            padding: 30px 0;
            margin-top: 40px;
        }
        
        .footer p {
            margin: 5px 0;
            opacity: 0.9;
        }
        
        @media (max-width: 768px) {
            .header h1 { font-size: 28px; }
            .stats-overview { grid-template-columns: 1fr 1fr; }
            .tabs { flex-direction: column; }
            table { font-size: 14px; }
            th, td { padding: 10px; }
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🏏 PSL Cricket Statistics Dashboard</h1>
        <p class="subtitle">Pakistan Super League Bowling Analytics</p>
        <div class="badges">
            <span class="badge badge-rdf">RDF Graph Backend</span>
            <span class="badge badge-dbpedia">Linked to DBpedia</span>
            <span class="badge badge-wikidata">Linked to Wikidata</span>
        </div>
    </div>
    
    <div class="container">
        <!-- Overview Stats -->
        <div class="stats-overview">
            <div class="stat-card">
                <div class="icon">👥</div>
                <div class="number">{{ total_players }}</div>
                <div class="label">Total Players</div>
            </div>
            <div class="stat-card">
                <div class="icon">🏆</div>
                <div class="number">{{ total_teams }}</div>
                <div class="label">PSL Teams</div>
            </div>
            <div class="stat-card">
                <div class="icon">🎯</div>
                <div class="number">{{ total_wickets }}</div>
                <div class="label">Total Wickets</div>
            </div>
            <div class="stat-card">
                <div class="icon">🔗</div>
                <div class="number">{{ external_links }}</div>
                <div class="label">External Links</div>
            </div>
            <div class="stat-card">
                <div class="icon">📊</div>
                <div class="number">{{ total_triples }}</div>
                <div class="label">RDF Triples</div>
            </div>
        </div>
        
        <!-- Tabs -->
        <div class="tabs">
            <button class="tab-button active" onclick="showTab('wickets')">🎯 Top Wicket Takers</button>
            <button class="tab-button" onclick="showTab('economy')">💰 Best Economy Rates</button>
            <button class="tab-button" onclick="showTab('fivewickets')">🌟 5-Wicket Hauls</button>
            <button class="tab-button" onclick="showTab('teams')">🏆 Team Statistics</button>
            <button class="tab-button" onclick="showTab('search')">🔍 Search Players</button>
        </div>
        
        <!-- Tab 1: Top Wicket Takers -->
        <div id="wickets" class="tab-content active">
            <h2 class="section-title">Top 20 Wicket Takers</h2>
            <div class="highlight-box">
                <strong>🔗 Linked Open Data:</strong> Click on Wikipedia or Wikidata links to explore additional information about players from external knowledge bases.
            </div>
            <table>
                <thead>
                    <tr>
                        <th style="width: 60px;">Rank</th>
                        <th>Player</th>
                        <th>Team</th>
                        <th style="width: 100px;">Wickets</th>
                        <th style="width: 100px;">Economy</th>
                        <th style="width: 100px;">Avg</th>
                        <th style="width: 200px;">External Links</th>
                    </tr>
                </thead>
                <tbody>
                    {% for player in top_wickets %}
                    <tr>
                        <td class="rank {% if loop.index <= 3 %}rank-{{ loop.index }}{% endif %}">
                            #{{ loop.index }}
                        </td>
                        <td class="player-name">{{ player.name }}</td>
                        <td>{{ player.team }}</td>
                        <td><strong>{{ player.wickets }}</strong></td>
                        <td>{{ player.economy }}</td>
                        <td>{{ player.average }}</td>
                        <td>
                            {% if player.dbpedia %}
                            <a href="{{ player.dbpedia }}" target="_blank" class="external-link">📖 Wikipedia</a>
                            {% endif %}
                            {% if player.wikidata %}
                            <a href="{{ player.wikidata }}" target="_blank" class="external-link">🗃️ Wikidata</a>
                            {% endif %}
                            {% if not player.dbpedia and not player.wikidata %}
                            <span class="no-links">No links</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- Tab 2: Best Economy -->
        <div id="economy" class="tab-content">
            <h2 class="section-title">Best Economy Rates (Min 20 Wickets)</h2>
            <table>
                <thead>
                    <tr>
                        <th style="width: 60px;">Rank</th>
                        <th>Player</th>
                        <th>Team</th>
                        <th style="width: 100px;">Economy</th>
                        <th style="width: 100px;">Wickets</th>
                        <th style="width: 100px;">Overs</th>
                        <th style="width: 200px;">External Links</th>
                    </tr>
                </thead>
                <tbody>
                    {% for player in best_economy %}
                    <tr>
                        <td class="rank {% if loop.index <= 3 %}rank-{{ loop.index }}{% endif %}">
                            #{{ loop.index }}
                        </td>
                        <td class="player-name">{{ player.name }}</td>
                        <td>{{ player.team }}</td>
                        <td><strong>{{ player.economy }}</strong></td>
                        <td>{{ player.wickets }}</td>
                        <td>{{ player.overs }}</td>
                        <td>
                            {% if player.dbpedia %}
                            <a href="{{ player.dbpedia }}" target="_blank" class="external-link">📖 Wikipedia</a>
                            {% endif %}
                            {% if player.wikidata %}
                            <a href="{{ player.wikidata }}" target="_blank" class="external-link">🗃️ Wikidata</a>
                            {% endif %}
                            {% if not player.dbpedia and not player.wikidata %}
                            <span class="no-links">No links</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- Tab 3: 5-Wicket Hauls -->
        <div id="fivewickets" class="tab-content">
            <h2 class="section-title">Players with 5-Wicket Hauls</h2>
            <table>
                <thead>
                    <tr>
                        <th>Player</th>
                        <th>Team</th>
                        <th style="width: 120px;">5-Wicket Hauls</th>
                        <th style="width: 150px;">Best Figures</th>
                        <th style="width: 100px;">Total Wickets</th>
                        <th style="width: 200px;">External Links</th>
                    </tr>
                </thead>
                <tbody>
                    {% for player in five_wickets %}
                    <tr>
                        <td class="player-name">{{ player.name }}</td>
                        <td>{{ player.team }}</td>
                        <td><strong>{{ player.five_wickets }}</strong></td>
                        <td>{{ player.best }}</td>
                        <td>{{ player.wickets }}</td>
                        <td>
                            {% if player.dbpedia %}
                            <a href="{{ player.dbpedia }}" target="_blank" class="external-link">📖 Wikipedia</a>
                            {% endif %}
                            {% if player.wikidata %}
                            <a href="{{ player.wikidata }}" target="_blank" class="external-link">🗃️ Wikidata</a>
                            {% endif %}
                            {% if not player.dbpedia and not player.wikidata %}
                            <span class="no-links">No links</span>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- Tab 4: Team Stats -->
        <div id="teams" class="tab-content">
            <h2 class="section-title">Team-wise Bowling Statistics</h2>
            <table>
                <thead>
                    <tr>
                        <th>Team</th>
                        <th style="width: 100px;">Players</th>
                        <th style="width: 120px;">Total Wickets</th>
                        <th style="width: 120px;">Avg Economy</th>
                        <th style="width: 120px;">Avg Strike Rate</th>
                        <th style="width: 200px;">External Links</th>
                    </tr>
                </thead>
                <tbody>
                    {% for team in team_stats %}
                    <tr>
                        <td class="player-name">{{ team.name }}</td>
                        <td>{{ team.players }}</td>
                        <td><strong>{{ team.wickets }}</strong></td>
                        <td>{{ team.economy }}</td>
                        <td>{{ team.strike_rate }}</td>
                        <td>
                            {% if team.dbpedia %}
                            <a href="{{ team.dbpedia }}" target="_blank" class="external-link">📖 Wikipedia</a>
                            {% endif %}
                            {% if team.wikidata %}
                            <a href="{{ team.wikidata }}" target="_blank" class="external-link">🗃️ Wikidata</a>
                            {% endif %}
                        </td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
        
        <!-- Tab 5: Search -->
        <div id="search" class="tab-content">
            <h2 class="section-title">Search Players</h2>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="Enter player name (e.g., Shaheen, Haris, Shadab...)">
                <button onclick="searchPlayer()">Search</button>
            </div>
            <div id="searchResults"></div>
        </div>
    </div>
    
    <div class="footer">
        <p><strong>🌐 Linked Open Data Architecture</strong></p>
        <p>Local RDF Graph ↔️ owl:sameAs ↔️ DBpedia (Wikipedia) & Wikidata</p>
        <p style="margin-top: 15px; font-size: 14px;">
            Powered by SPARQL queries on semantic web graph | {{ total_triples }} RDF triples
        </p>
    </div>
    
    <script>
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Remove active from all buttons
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            
            // Activate button
            event.target.classList.add('active');
        }
        
        function searchPlayer() {
            const query = document.getElementById('searchInput').value;
            if (!query) {
                alert('Please enter a player name');
                return;
            }
            
            fetch('/api/search?q=' + encodeURIComponent(query))
                .then(response => response.json())
                .then(data => {
                    if (data.length === 0) {
                        document.getElementById('searchResults').innerHTML = 
                            '<p style="text-align: center; padding: 40px; color: #999;">No players found matching "' + query + '"</p>';
                        return;
                    }
                    
                    let html = '<table><thead><tr><th>Player</th><th>Team</th><th>Wickets</th><th>Economy</th><th>Average</th><th>External Links</th></tr></thead><tbody>';
                    data.forEach(player => {
                        let links = '';
                        if (player.dbpedia) {
                            links += `<a href="${player.dbpedia}" target="_blank" class="external-link">📖 Wikipedia</a> `;
                        }
                        if (player.wikidata) {
                            links += `<a href="${player.wikidata}" target="_blank" class="external-link">🗃️ Wikidata</a>`;
                        }
                        if (!links) links = '<span class="no-links">No links</span>';
                        
                        html += `<tr>
                            <td class="player-name">${player.name}</td>
                            <td>${player.team}</td>
                            <td><strong>${player.wickets}</strong></td>
                            <td>${player.economy}</td>
                            <td>${player.average}</td>
                            <td>${links}</td>
                        </tr>`;
                    });
                    html += '</tbody></table>';
                    document.getElementById('searchResults').innerHTML = html;
                });
        }
        
        // Allow Enter key to search
        document.addEventListener('DOMContentLoaded', function() {
            document.getElementById('searchInput').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    searchPlayer();
                }
            });
        });
    </script>
</body>
</html>
"""

def get_external_links(resource_uri):
    """Get DBpedia and Wikidata links"""
    links = {'dbpedia': None, 'wikidata': None}
    for s, p, o in g.triples((resource_uri, OWL.sameAs, None)):
        link = str(o)
        if 'dbpedia.org' in link:
            links['dbpedia'] = link
        elif 'wikidata.org' in link:
            links['wikidata'] = link
    return links

@app.route('/')
def index():
    """Main dashboard"""
    
    CRICKET = Namespace("http://example.org/cricket/ontology#")
    
    # Count stats
    total_players = len(list(g.subjects(RDF.type, CRICKET.Player)))
    total_teams = len(list(g.subjects(RDF.type, CRICKET.Team)))
    external_links_count = len(list(g.triples((None, OWL.sameAs, None))))
    
    # Total wickets
    query_wickets = """
    PREFIX cricket: <http://example.org/cricket/ontology#>
    SELECT (SUM(?wickets) AS ?total)
    WHERE { ?stats cricket:wickets ?wickets }
    """
    total_wickets = int(float(list(g.query(query_wickets))[0][0]))
    
    # Top 20 wicket takers
    query_top = """
    PREFIX cricket: <http://example.org/cricket/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?player ?name ?team ?wickets ?economy ?average
    WHERE {
        ?stats cricket:forPlayer ?player ;
               cricket:forTeam ?teamRes ;
               cricket:wickets ?wickets ;
               cricket:economy ?economy ;
               cricket:average ?average .
        ?player rdfs:label ?name .
        ?teamRes rdfs:label ?team .
    }
    ORDER BY DESC(?wickets)
    LIMIT 20
    """
    
    top_wickets = []
    for row in g.query(query_top):
        links = get_external_links(row[0])
        top_wickets.append({
            'name': str(row[1]),
            'team': str(row[2]),
            'wickets': int(float(row[3])),
            'economy': f"{float(row[4]):.2f}",
            'average': f"{float(row[5]):.2f}",
            'dbpedia': links['dbpedia'],
            'wikidata': links['wikidata']
        })
    
    # Best economy rates
    query_economy = """
    PREFIX cricket: <http://example.org/cricket/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?player ?name ?team ?economy ?wickets ?overs
    WHERE {
        ?stats cricket:forPlayer ?player ;
               cricket:forTeam ?teamRes ;
               cricket:economy ?economy ;
               cricket:wickets ?wickets ;
               cricket:overs ?overs .
        ?player rdfs:label ?name .
        ?teamRes rdfs:label ?team .
        FILTER(?wickets >= 20)
    }
    ORDER BY ASC(?economy)
    LIMIT 20
    """
    
    best_economy = []
    for row in g.query(query_economy):
        links = get_external_links(row[0])
        best_economy.append({
            'name': str(row[1]),
            'team': str(row[2]),
            'economy': f"{float(row[3]):.2f}",
            'wickets': int(float(row[4])),
            'overs': f"{float(row[5]):.1f}",
            'dbpedia': links['dbpedia'],
            'wikidata': links['wikidata']
        })
    
    # 5-wicket hauls
    query_five = """
    PREFIX cricket: <http://example.org/cricket/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?player ?name ?team ?fiveWkts ?best ?wickets
    WHERE {
        ?stats cricket:forPlayer ?player ;
               cricket:forTeam ?teamRes ;
               cricket:fiveWickets ?fiveWkts ;
               cricket:bestBowlingInnings ?best ;
               cricket:wickets ?wickets .
        ?player rdfs:label ?name .
        ?teamRes rdfs:label ?team .
        FILTER(?fiveWkts > 0)
    }
    ORDER BY DESC(?fiveWkts) DESC(?wickets)
    """
    
    five_wickets = []
    for row in g.query(query_five):
        links = get_external_links(row[0])
        five_wickets.append({
            'name': str(row[1]),
            'team': str(row[2]),
            'five_wickets': int(float(row[3])),
            'best': str(row[4]),
            'wickets': int(float(row[5])),
            'dbpedia': links['dbpedia'],
            'wikidata': links['wikidata']
        })
    
    # Team stats
    query_teams = """
    PREFIX cricket: <http://example.org/cricket/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?team ?teamName 
           (COUNT(DISTINCT ?player) AS ?players)
           (SUM(?wickets) AS ?totalWickets)
           (AVG(?economy) AS ?avgEconomy)
           (AVG(?strikeRate) AS ?avgSR)
    WHERE {
        ?stats cricket:forPlayer ?player ;
               cricket:forTeam ?team ;
               cricket:wickets ?wickets ;
               cricket:economy ?economy ;
               cricket:strikeRate ?strikeRate .
        ?team rdfs:label ?teamName .
    }
    GROUP BY ?team ?teamName
    ORDER BY DESC(?totalWickets)
    """
    
    team_stats = []
    for row in g.query(query_teams):
        links = get_external_links(row[0])
        team_stats.append({
            'name': str(row[1]),
            'players': int(row[2]),
            'wickets': int(float(row[3])),
            'economy': f"{float(row[4]):.2f}",
            'strike_rate': f"{float(row[5]):.2f}",
            'dbpedia': links['dbpedia'],
            'wikidata': links['wikidata']
        })
    
    return render_template_string(
        HTML_TEMPLATE,
        total_players=total_players,
        total_teams=total_teams,
        total_wickets=total_wickets,
        external_links=external_links_count,
        total_triples=len(g),
        top_wickets=top_wickets,
        best_economy=best_economy,
        five_wickets=five_wickets,
        team_stats=team_stats
    )

@app.route('/api/search')
def search():
    """Search API"""
    query_text = request.args.get('q', '')
    
    sparql_query = f"""
    PREFIX cricket: <http://example.org/cricket/ontology#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    
    SELECT ?player ?name ?team ?wickets ?economy ?average
    WHERE {{
        ?stats cricket:forPlayer ?player ;
               cricket:forTeam ?teamRes ;
               cricket:wickets ?wickets ;
               cricket:economy ?economy ;
               cricket:average ?average .
        ?player rdfs:label ?name .
        ?teamRes rdfs:label ?team .
        FILTER(CONTAINS(LCASE(?name), LCASE("{query_text}")))
    }}
    ORDER BY DESC(?wickets)
    LIMIT 50
    """
    
    results = []
    for row in g.query(sparql_query):
        links = get_external_links(row[0])
        results.append({
            'name': str(row[1]),
            'team': str(row[2]),
            'wickets': int(float(row[3])),
            'economy': f"{float(row[4]):.2f}",
            'average': f"{float(row[5]):.2f}",
            'dbpedia': links['dbpedia'],
            'wikidata': links['wikidata']
        })
    
    return jsonify(results)

if __name__ == '__main__':
    print("=" * 80)
    print("PSL CRICKET STATISTICS - PROFESSIONAL DASHBOARD")
    print("=" * 80)
    print(f"\n✓ Loaded {len(g)} RDF triples")
    print(f"✓ External links: {len(list(g.triples((None, OWL.sameAs, None))))}")
    print("\n🌐 Starting professional web application...")
    print("📊 Open your browser at: http://localhost:5000")
    print("\nFeatures:")
    print("  • Top 20 Wicket Takers")
    print("  • Best Economy Rates")
    print("  • 5-Wicket Hauls")
    print("  • Team Statistics")
    print("  • Player Search")
    print("  • Links to DBpedia & Wikidata")
    print("\nPress Ctrl+C to stop")
    print("=" * 80)
    
    app.run(debug=True, port=5000)
