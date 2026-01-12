"""
Visualize RDF Graph using NetworkX and Matplotlib
Creates a network diagram of your ontology
"""

import networkx as nx
import matplotlib.pyplot as plt
from rdflib import Graph, Namespace
from rdflib.namespace import RDF, RDFS, OWL

def visualize_ontology_structure():
    """Visualize the ontology class hierarchy"""
    
    print("Loading ontology...")
    g = Graph()
    g.parse("cricket_ontology_enhanced.ttl", format="turtle")
    
    # Create directed graph
    G = nx.DiGraph()
    
    # Add class hierarchy edges
    for s, p, o in g.triples((None, RDFS.subClassOf, None)):
        if isinstance(s, str) or isinstance(o, str):
            continue
        
        # Get class names
        s_name = str(s).split('#')[-1].split('/')[-1]
        o_name = str(o).split('#')[-1].split('/')[-1]
        
        # Skip owl:Thing for cleaner visualization
        if o_name != "Thing" and s_name != "Thing":
            G.add_edge(o_name, s_name)
    
    # Create visualization
    plt.figure(figsize=(16, 12))
    
    # Use hierarchical layout
    pos = nx.spring_layout(G, k=2, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, 
                          node_color='lightblue',
                          node_size=3000,
                          alpha=0.9)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          arrows=True,
                          arrowsize=20,
                          width=2)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos,
                           font_size=10,
                           font_weight='bold')
    
    plt.title("Cricket Ontology Class Hierarchy", fontsize=16, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('ontology_class_hierarchy_graph.png', dpi=300, bbox_inches='tight')
    print("✓ Created: ontology_class_hierarchy_graph.png")
    plt.close()

def visualize_data_relationships():
    """Visualize relationships in the actual data"""
    
    print("\nLoading data...")
    g = Graph()
    g.parse("bowling_stats_enhanced_linked.ttl", format="turtle")
    
    CRICKET = Namespace("http://example.org/cricket/ontology#")
    
    # Create graph
    G = nx.DiGraph()
    
    # Add player-team relationships (sample)
    count = 0
    for s, p, o in g.triples((None, CRICKET.playsFor, None)):
        if count >= 20:  # Limit to 20 for readability
            break
        
        # Get labels
        player_label = g.value(s, RDFS.label)
        team_label = g.value(o, RDFS.label)
        
        if player_label and team_label:
            G.add_edge(str(player_label), str(team_label), label="playsFor")
            count += 1
    
    # Create visualization
    plt.figure(figsize=(16, 12))
    
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Separate nodes by type
    players = [n for n in G.nodes() if any(G.has_edge(n, t) for t in G.nodes())]
    teams = [n for n in G.nodes() if any(G.has_edge(p, n) for p in G.nodes())]
    
    # Draw team nodes (larger, different color)
    team_nodes = [n for n in G.nodes() if n in teams]
    nx.draw_networkx_nodes(G, pos,
                          nodelist=team_nodes,
                          node_color='orange',
                          node_size=4000,
                          alpha=0.9,
                          label='Teams')
    
    # Draw player nodes
    player_nodes = [n for n in G.nodes() if n not in teams]
    nx.draw_networkx_nodes(G, pos,
                          nodelist=player_nodes,
                          node_color='lightgreen',
                          node_size=2000,
                          alpha=0.9,
                          label='Players')
    
    # Draw edges
    nx.draw_networkx_edges(G, pos,
                          edge_color='gray',
                          arrows=True,
                          arrowsize=15,
                          width=1.5)
    
    # Draw labels
    nx.draw_networkx_labels(G, pos,
                           font_size=8,
                           font_weight='bold')
    
    plt.title("Player-Team Relationships (Sample)", fontsize=16, fontweight='bold')
    plt.legend(scatterpoints=1)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('data_relationships_graph.png', dpi=300, bbox_inches='tight')
    print("✓ Created: data_relationships_graph.png")
    plt.close()

def visualize_external_links():
    """Visualize external links to DBpedia/Wikidata"""
    
    print("\nVisualizing external links...")
    g = Graph()
    g.parse("bowling_stats_enhanced_linked.ttl", format="turtle")
    
    G = nx.DiGraph()
    
    # Add external links
    count = 0
    for s, p, o in g.triples((None, OWL.sameAs, None)):
        if count >= 15:  # Limit for readability
            break
        
        # Get label
        label = g.value(s, RDFS.label)
        if label:
            local_name = str(label)
            external = str(o)
            
            if "dbpedia" in external:
                external_name = "DBpedia: " + external.split('/')[-1]
            elif "wikidata" in external:
                external_name = "Wikidata: " + external.split('/')[-1]
            else:
                external_name = external.split('/')[-1]
            
            G.add_edge(local_name, external_name, label="sameAs")
            count += 1
    
    # Create visualization
    plt.figure(figsize=(16, 12))
    
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    # Identify node types
    local_nodes = [n for n in G.nodes() if not n.startswith("DBpedia:") and not n.startswith("Wikidata:")]
    dbpedia_nodes = [n for n in G.nodes() if n.startswith("DBpedia:")]
    wikidata_nodes = [n for n in G.nodes() if n.startswith("Wikidata:")]
    
    # Draw nodes by type
    nx.draw_networkx_nodes(G, pos,
                          nodelist=local_nodes,
                          node_color='lightblue',
                          node_size=3000,
                          alpha=0.9,
                          label='Local Data')
    
    nx.draw_networkx_nodes(G, pos,
                          nodelist=dbpedia_nodes,
                          node_color='orange',
                          node_size=3000,
                          alpha=0.9,
                          label='DBpedia')
    
    nx.draw_networkx_nodes(G, pos,
                          nodelist=wikidata_nodes,
                          node_color='lightgreen',
                          node_size=3000,
                          alpha=0.9,
                          label='Wikidata')
    
    # Draw edges
    nx.draw_networkx_edges(G, pos,
                          edge_color='red',
                          arrows=True,
                          arrowsize=15,
                          width=2,
                          style='dashed')
    
    # Draw labels
    nx.draw_networkx_labels(G, pos,
                           font_size=7,
                           font_weight='bold')
    
    plt.title("External Links (owl:sameAs)", fontsize=16, fontweight='bold')
    plt.legend(scatterpoints=1)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('external_links_graph.png', dpi=300, bbox_inches='tight')
    print("✓ Created: external_links_graph.png")
    plt.close()

def print_graph_statistics():
    """Print validation statistics"""
    
    print("\n" + "=" * 80)
    print("GRAPH VALIDATION STATISTICS")
    print("=" * 80)
    
    # Load ontology
    g_onto = Graph()
    g_onto.parse("cricket_ontology_enhanced.ttl", format="turtle")
    
    # Load data
    g_data = Graph()
    g_data.parse("bowling_stats_enhanced_linked.ttl", format="turtle")
    
    # Count classes
    classes = len(list(g_onto.subjects(RDF.type, OWL.Class)))
    print(f"\nOntology Classes: {classes}")
    
    # Count properties
    obj_props = len(list(g_onto.subjects(RDF.type, OWL.ObjectProperty)))
    data_props = len(list(g_onto.subjects(RDF.type, OWL.DatatypeProperty)))
    print(f"Object Properties: {obj_props}")
    print(f"Data Properties: {data_props}")
    
    # Count instances
    CRICKET = Namespace("http://example.org/cricket/ontology#")
    players = len(list(g_data.subjects(RDF.type, CRICKET.Player)))
    teams = len(list(g_data.subjects(RDF.type, CRICKET.Team)))
    stats = len(list(g_data.subjects(RDF.type, CRICKET.BowlingStatistics)))
    
    print(f"\nData Instances:")
    print(f"  Players: {players}")
    print(f"  Teams: {teams}")
    print(f"  Statistics: {stats}")
    
    # Count external links
    external_links = len(list(g_data.triples((None, OWL.sameAs, None))))
    print(f"\nExternal Links (owl:sameAs): {external_links}")
    
    # Total triples
    print(f"\nTotal Triples:")
    print(f"  Ontology: {len(g_onto)}")
    print(f"  Data: {len(g_data)}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print("=" * 80)
    print("RDF GRAPH VISUALIZATION AND VALIDATION")
    print("=" * 80)
    
    # Generate visualizations
    visualize_ontology_structure()
    visualize_data_relationships()
    visualize_external_links()
    
    # Print statistics
    print_graph_statistics()
    
    print("\n" + "=" * 80)
    print("VISUALIZATION COMPLETE!")
    print("=" * 80)
    print("\nGenerated files:")
    print("  1. ontology_class_hierarchy_graph.png - Class hierarchy")
    print("  2. data_relationships_graph.png - Player-Team relationships")
    print("  3. external_links_graph.png - Links to DBpedia/Wikidata")
    print("\nUse these visualizations in your report!")
    print("=" * 80)
