"""
Check what classes are in the ontology
"""

from rdflib import Graph, Namespace, RDF, OWL, RDFS

# Load ontology
g = Graph()
g.parse("cricket_ontology_enhanced.owl", format="xml")

print("=" * 80)
print("CLASSES IN YOUR ONTOLOGY")
print("=" * 80)
print()

# Find all classes
classes = list(g.subjects(RDF.type, OWL.Class))

print(f"Total classes found: {len(classes)}")
print()

# Group by namespace
cricket_classes = []
other_classes = []

for cls in classes:
    cls_str = str(cls)
    if "cricket/ontology" in cls_str:
        cricket_classes.append(cls_str)
    else:
        other_classes.append(cls_str)

print("Cricket Ontology Classes:")
print("-" * 80)
for cls in sorted(cricket_classes):
    # Get label if available
    label = g.value(cls, RDFS.label)
    class_name = cls.split('#')[-1] if '#' in cls else cls.split('/')[-1]
    if label:
        print(f"  • {class_name} - {label}")
    else:
        print(f"  • {class_name}")

if other_classes:
    print()
    print("Other Classes:")
    print("-" * 80)
    for cls in sorted(other_classes):
        print(f"  • {cls}")

print()
print("=" * 80)
