# Modeling Decisions - Cricket Bowling Statistics Ontology

## 1. Domain Selection

### Decision: Cricket Bowling Statistics
**Rationale:**
- Rich domain with clear entities (players, teams, statistics)
- Well-defined relationships (player plays for team)
- Quantifiable metrics (wickets, economy, average)
- Available external data sources (DBpedia, Wikidata)
- Personal interest and domain knowledge

---

## 2. Ontology Design Decisions

### 2.1 Class Hierarchy

**Decision:** Create 23 classes organized in a 3-level hierarchy

**Rationale:**
- **Top level**: Reuse Schema.org (Person, SportsTeam) for interoperability
- **Mid level**: Cricket-specific classes (Player, Team, BowlingStatistics)
- **Bottom level**: Specialized classes (FastBowler, SpinBowler, performance classifications)

**Example:**
```
schema:Person
  └── cricket:Player
      ├── cricket:Bowler
      │   ├── cricket:FastBowler
      │   └── cricket:SpinBowler
      └── cricket:AllRounder
```

**Benefits:**
- Clear organization
- Easy to understand
- Supports reasoning
- Extensible for future additions

---

### 2.2 Vocabulary Reuse vs. Custom Design

**Decision:** Hybrid approach - reuse standard vocabularies + custom cricket vocabulary

**Reused Vocabularies:**
- **Schema.org**: Person, SportsTeam, name, memberOf
- **Dublin Core**: title, description, created, source, license
- **FOAF**: name
- **OWL**: sameAs, Class, ObjectProperty, DatatypeProperty

**Custom Vocabulary:**
- **cricket:** namespace for domain-specific concepts
- Custom classes: Bowler, BowlingStatistics, Match, Tournament
- Custom properties: wickets, economy, playsFor, forPlayer

**Rationale:**
- Standard vocabularies ensure interoperability
- Custom vocabulary provides domain specificity
- Balance between reuse and expressiveness
- Follows Linked Data best practices

---

### 2.3 URI Design

**Decision:** Hierarchical URI structure with meaningful paths

**Pattern:**
```
Base: http://example.org/cricket/
Ontology: http://example.org/cricket/ontology#
Players: http://example.org/cricket/resource/player/
Teams: http://example.org/cricket/resource/team/
Statistics: http://example.org/cricket/resource/stats/
```

**Rationale:**
- Clear namespace separation
- Human-readable URIs
- Easy to maintain
- Follows W3C best practices
- Supports content negotiation

**Example:**
```
http://example.org/cricket/resource/player/Shaheen_Shah_Afridi
```

---

### 2.4 Performance Classification

**Decision:** Create 4 performance classes based on wickets taken

**Classes:**
- **ExcellentPerformance**: 50+ wickets AND economy < 7.5
- **GoodPerformance**: 20-49 wickets
- **AveragePerformance**: 10-19 wickets
- **PoorPerformance**: <10 wickets

**Rationale:**
- Enables automatic classification via reasoning
- Provides meaningful categorization
- Supports analytical queries
- Demonstrates OWL reasoning capabilities

**Implementation:**
```turtle
cricket:ExcellentPerformance rdfs:subClassOf cricket:BowlingStatistics .
cricket:ExcellentPerformance rdfs:comment "Performance with 50+ wickets and economy < 7.5" .
```

---

### 2.5 Cardinality Restrictions

**Decision:** Enforce strict cardinality constraints

**Constraints:**
1. **Player playsFor exactly 1 Team**
   - Rationale: In this dataset, each player represents one team
   - Ensures data consistency
   - Prevents invalid data

2. **Team hasPlayer min 11 Players**
   - Rationale: Cricket teams need minimum 11 players
   - Enforces domain rules
   - Validates data quality

3. **BowlingStatistics forPlayer exactly 1 Player**
   - Rationale: Each statistics record belongs to one player
   - Prevents ambiguity
   - Maintains data integrity

**Implementation:**
```turtle
cricket:Player rdfs:subClassOf [
    a owl:Restriction ;
    owl:onProperty cricket:playsFor ;
    owl:cardinality 1
] .
```

---

### 2.6 Functional Properties

**Decision:** Define functional properties for unique identifiers

**Properties:**
- **playerID**: Uniquely identifies a player (inverse functional)
- **teamID**: Uniquely identifies a team (inverse functional)
- **birthDate**: A player has exactly one birth date (functional)
- **jerseyNumber**: A player has exactly one jersey number (functional)

**Rationale:**
- Ensures uniqueness
- Supports entity resolution
- Enables data validation
- Demonstrates OWL expressiveness

---

### 2.7 Advanced OWL Features

**Decision:** Include union, intersection, and complement classes

**Union Class:**
```turtle
cricket:ActivePlayer owl:unionOf (cricket:Bowler cricket:AllRounder cricket:WicketKeeper)
```
- Represents any player who actively participates in bowling/fielding

**Intersection Class:**
```turtle
cricket:EliteBowler owl:intersectionOf (cricket:Bowler cricket:ExcellentPerformance)
```
- Represents bowlers with excellent performance

**Complement Class:**
```turtle
cricket:NonBowler owl:complementOf cricket:Bowler
```
- Represents players who are not bowlers

**Rationale:**
- Demonstrates OWL 2 capabilities
- Enables complex reasoning
- Supports advanced queries
- Shows understanding of ontology design

---

## 3. Data Conversion Decisions

### 3.1 Datatype Selection

**Decision:** Use appropriate XSD datatypes for each property

**Mappings:**
- **Matches**: xsd:integer (whole numbers)
- **Wickets, Overs, Economy**: xsd:float (decimal values)
- **Player Name**: xsd:string
- **Span**: xsd:string (time period as text)

**Rationale:**
- Ensures data accuracy
- Enables numeric operations
- Supports SPARQL filtering
- Follows RDF best practices

---

### 3.2 Missing Data Handling

**Decision:** Omit triples for missing values rather than using null/empty

**Rationale:**
- RDF open-world assumption
- Cleaner data model
- Avoids ambiguity
- Standard practice in Linked Data

**Example:**
```turtle
# If a player has no 5-wicket hauls, omit the triple entirely
# Rather than: cricket:fiveWickets 0
```

---

### 3.3 URI Generation

**Decision:** Generate URIs from player/team names with underscores

**Pattern:**
```
"Shaheen Shah Afridi" → player:Shaheen_Shah_Afridi
"Lahore Qalandars" → team:Lahore_Qalanders
```

**Rationale:**
- Human-readable
- URL-safe (no spaces)
- Consistent naming
- Easy to debug

---

## 4. External Linking Decisions

### 4.1 Link Selection

**Decision:** Link to DBpedia and Wikidata using owl:sameAs

**Rationale:**
- DBpedia provides Wikipedia content
- Wikidata provides structured identifiers
- Both are widely used in Linked Data
- Enables federated queries
- Demonstrates 5-star Linked Open Data

---

### 4.2 Coverage Strategy

**Decision:** Link famous/international players (22% coverage) and all teams (100%)

**Rationale:**
- Not all domestic players have Wikipedia pages
- Manual linking is time-consuming
- Focus on high-value entities
- Realistic for project scope
- Demonstrates the concept effectively

---

### 4.3 Link Verification

**Decision:** Manually verify each external link

**Process:**
1. Search DBpedia/Wikidata for entity
2. Verify it's the correct person/team
3. Extract canonical URI
4. Add owl:sameAs triple
5. Test link accessibility

**Rationale:**
- Ensures accuracy
- Prevents false matches
- Maintains data quality
- Follows best practices

---

## 5. Reasoning Decisions

### 5.1 Reasoner Selection

**Decision:** Use HermiT reasoner in Protégé

**Rationale:**
- Supports OWL 2 DL
- Handles complex axioms
- Provides explanations
- Well-tested and reliable
- Free and open-source

---

### 5.2 Reasoning Goals

**Decision:** Use reasoning for automatic classification

**Goals:**
1. Classify players into performance categories
2. Infer class hierarchy
3. Validate cardinality constraints
4. Check consistency
5. Discover implicit relationships

**Example:**
- Player with 87 wickets and 7.98 economy → Automatically classified as ExcellentPerformance

---

## 6. Serialization Decisions

### 6.1 Multiple Formats

**Decision:** Provide Turtle, RDF/XML, and JSON-LD formats

**Rationale:**
- **Turtle**: Human-readable, easy to edit
- **RDF/XML**: Standard format, widely supported
- **JSON-LD**: Web-friendly, JavaScript compatible
- Maximizes accessibility
- Demonstrates format flexibility

---

### 6.2 Primary Format

**Decision:** Use Turtle as primary format

**Rationale:**
- Most readable
- Easier to debug
- Preferred by developers
- Compact syntax
- Good for version control

---

## 7. Query Design Decisions

### 7.1 Competency Questions

**Decision:** Define 26 competency questions covering all aspects

**Categories:**
1. Player information (5 questions)
2. Bowling performance (6 questions)
3. Achievements (3 questions)
4. Team statistics (4 questions)
5. Comparative analysis (3 questions)
6. Performance classification (2 questions)
7. External linking (3 questions)

**Rationale:**
- Validates ontology completeness
- Guides design decisions
- Demonstrates query capabilities
- Covers all use cases

---

### 7.2 SPARQL Complexity

**Decision:** Include both simple and complex queries

**Simple:**
```sparql
SELECT ?player WHERE { ?player a cricket:Player }
```

**Complex:**
```sparql
SELECT ?playerName (AVG(?economy) AS ?avgEcon)
WHERE { ... }
GROUP BY ?playerName
HAVING (AVG(?economy) < 8.0)
```

**Rationale:**
- Shows range of capabilities
- Demonstrates SPARQL features
- Supports different user needs
- Educational value

---

## 8. Application Design Decisions

### 8.1 Web Interface

**Decision:** Create Flask-based web application

**Rationale:**
- Lightweight framework
- Python integration with RDFLib
- Easy to deploy
- Supports REST API
- Good for demonstrations

---

### 8.2 Content Negotiation

**Decision:** Implement content negotiation for different RDF formats

**Supported:**
- text/turtle → Turtle format
- application/rdf+xml → RDF/XML format
- application/ld+json → JSON-LD format
- text/html → Human-readable HTML

**Rationale:**
- Follows Linked Data principles
- Supports different clients
- Demonstrates best practices
- Enables machine-to-machine communication

---

## 9. Documentation Decisions

### 9.1 Documentation Structure

**Decision:** Create separate documents for different aspects

**Documents:**
1. CONCEPTUAL_MODEL.md - Ontology design
2. DATASET_DESCRIPTION.md - Data details
3. EXTERNAL_LINKING.md - External connections
4. COMPETENCY_QUESTIONS.md - Query examples
5. MODELING_DECISIONS.md - This document

**Rationale:**
- Clear organization
- Easy to navigate
- Comprehensive coverage
- Professional presentation

---

## 10. Validation Decisions

### 10.1 Validation Strategy

**Decision:** Multi-level validation approach

**Levels:**
1. **Syntactic**: Valid RDF/OWL syntax
2. **Semantic**: Consistent ontology (reasoner)
3. **Pragmatic**: Answers competency questions
4. **External**: Valid external links

**Rationale:**
- Comprehensive quality assurance
- Catches different types of errors
- Ensures usability
- Demonstrates thoroughness

---

## Summary

These modeling decisions were made to create a:
- **Well-structured** ontology with clear hierarchy
- **Interoperable** system using standard vocabularies
- **Expressive** model with advanced OWL features
- **Practical** solution that answers real questions
- **Linked** dataset connected to external sources
- **Validated** knowledge base with reasoning support

The decisions balance theoretical rigor with practical usability, demonstrating understanding of semantic web technologies while creating a functional cricket statistics knowledge base.
