# Competency Questions for Cricket Bowling Statistics Ontology

## Overview
Competency questions define what queries the ontology should be able to answer. These questions guide the ontology design and validate that the knowledge base is complete.

---

## Category 1: Player Information

**CQ1:** Who are all the cricket players in the dataset?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
SELECT ?player
WHERE { ?player a cricket:Player }
```

**CQ2:** Which team does a specific player play for?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?teamName
WHERE {
    ?player a cricket:Player ;
            rdfs:label ?playerName ;
            cricket:playsFor ?team .
    ?team rdfs:label ?teamName .
    FILTER(CONTAINS(?playerName, "Shaheen"))
}
```

**CQ3:** What are the names of all players?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName
WHERE {
    ?player a cricket:Player ;
            rdfs:label ?playerName .
}
ORDER BY ?playerName
```

**CQ4:** How many players are there per team?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?teamName (COUNT(?player) AS ?playerCount)
WHERE {
    ?player a cricket:Player ;
            cricket:playsFor ?team .
    ?team rdfs:label ?teamName .
}
GROUP BY ?teamName
ORDER BY DESC(?playerCount)
```

---

## Category 2: Bowling Performance

**CQ5:** What are the bowling statistics for a specific player?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?wickets ?economy ?average ?strikeRate
WHERE {
    ?player rdfs:label "Shaheen Shah Afridi" .
    ?stats cricket:forPlayer ?player ;
           cricket:wickets ?wickets ;
           cricket:economy ?economy ;
           cricket:average ?average ;
           cricket:strikeRate ?strikeRate .
}
```

**CQ6:** Who is the top wicket-taker?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?wickets
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:wickets ?wickets .
    ?player rdfs:label ?playerName .
}
ORDER BY DESC(?wickets)
LIMIT 1
```

**CQ7:** Which players have taken more than 50 wickets?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?wickets
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:wickets ?wickets .
    ?player rdfs:label ?playerName .
    FILTER(?wickets > 50)
}
ORDER BY DESC(?wickets)
```

**CQ8:** Who has the best economy rate (minimum 20 wickets)?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?economy ?wickets
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:economy ?economy ;
           cricket:wickets ?wickets .
    ?player rdfs:label ?playerName .
    FILTER(?wickets >= 20)
}
ORDER BY ASC(?economy)
LIMIT 1
```

**CQ9:** What is the average bowling economy rate across all players?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
SELECT (AVG(?economy) AS ?avgEconomy)
WHERE {
    ?stats cricket:economy ?economy .
}
```

**CQ10:** Which players have a strike rate better than 20?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?strikeRate
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:strikeRate ?strikeRate .
    ?player rdfs:label ?playerName .
    FILTER(?strikeRate < 20)
}
ORDER BY ASC(?strikeRate)
```

---

## Category 3: Achievements

**CQ11:** Which players have taken 5-wicket hauls?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?fiveWickets ?bestBowling
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:fiveWickets ?fiveWickets ;
           cricket:bestBowlingInnings ?bestBowling .
    ?player rdfs:label ?playerName .
    FILTER(?fiveWickets > 0)
}
ORDER BY DESC(?fiveWickets)
```

**CQ12:** What is the best bowling figure in an innings?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?bestBowling ?wickets
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:bestBowlingInnings ?bestBowling ;
           cricket:wickets ?wickets .
    ?player rdfs:label ?playerName .
}
ORDER BY DESC(?wickets)
LIMIT 1
```

**CQ13:** How many 4-wicket hauls does each player have?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?fourWickets
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:fourWickets ?fourWickets .
    ?player rdfs:label ?playerName .
    FILTER(?fourWickets > 0)
}
ORDER BY DESC(?fourWickets)
```

---

## Category 4: Team Statistics

**CQ14:** What are all the teams in the dataset?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?teamName
WHERE {
    ?team a cricket:Team ;
          rdfs:label ?teamName .
}
```

**CQ15:** What is the total number of wickets taken by each team?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?teamName (SUM(?wickets) AS ?totalWickets)
WHERE {
    ?stats cricket:forTeam ?team ;
           cricket:wickets ?wickets .
    ?team rdfs:label ?teamName .
}
GROUP BY ?teamName
ORDER BY DESC(?totalWickets)
```

**CQ16:** Which team has the best average economy rate?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?teamName (AVG(?economy) AS ?avgEconomy)
WHERE {
    ?stats cricket:forTeam ?team ;
           cricket:economy ?economy .
    ?team rdfs:label ?teamName .
}
GROUP BY ?teamName
ORDER BY ASC(?avgEconomy)
LIMIT 1
```

**CQ17:** How many players does each team have?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?teamName (COUNT(DISTINCT ?player) AS ?playerCount)
WHERE {
    ?player cricket:playsFor ?team .
    ?team rdfs:label ?teamName .
}
GROUP BY ?teamName
```

---

## Category 5: Comparative Analysis

**CQ18:** Compare bowling statistics of two players
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?wickets ?economy ?average
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:wickets ?wickets ;
           cricket:economy ?economy ;
           cricket:average ?average .
    ?player rdfs:label ?playerName .
    FILTER(?playerName IN ("Shaheen Shah Afridi", "Haris Rauf"))
}
```

**CQ19:** Which players have better economy than the average?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?economy
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:economy ?economy .
    ?player rdfs:label ?playerName .
    
    {
        SELECT (AVG(?e) AS ?avgEconomy)
        WHERE { ?s cricket:economy ?e }
    }
    
    FILTER(?economy < ?avgEconomy)
}
ORDER BY ASC(?economy)
```

**CQ20:** Rank teams by average strike rate
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?teamName (AVG(?strikeRate) AS ?avgStrikeRate)
WHERE {
    ?stats cricket:forTeam ?team ;
           cricket:strikeRate ?strikeRate .
    ?team rdfs:label ?teamName .
}
GROUP BY ?teamName
ORDER BY ASC(?avgStrikeRate)
```

---

## Category 6: Performance Classification

**CQ21:** Which players have excellent performance (50+ wickets, economy < 7.5)?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?wickets ?economy
WHERE {
    ?stats a cricket:ExcellentPerformance ;
           cricket:forPlayer ?player ;
           cricket:wickets ?wickets ;
           cricket:economy ?economy .
    ?player rdfs:label ?playerName .
}
ORDER BY DESC(?wickets)
```

**CQ22:** How many players fall into each performance category?
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
SELECT ?category (COUNT(?stats) AS ?count)
WHERE {
    ?stats rdf:type ?category .
    FILTER(?category IN (cricket:ExcellentPerformance, cricket:GoodPerformance, 
                         cricket:AveragePerformance, cricket:PoorPerformance))
}
GROUP BY ?category
```

---

## Category 7: External Linking (Linked Open Data)

**CQ23:** Which players have links to DBpedia?
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?dbpediaLink
WHERE {
    ?player rdfs:label ?playerName ;
            owl:sameAs ?dbpediaLink .
    FILTER(CONTAINS(STR(?dbpediaLink), "dbpedia"))
}
```

**CQ24:** Which teams have links to Wikidata?
```sparql
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX cricket: <http://example.org/cricket/ontology#>
SELECT ?teamName ?wikidataLink
WHERE {
    ?team a cricket:Team ;
          rdfs:label ?teamName ;
          owl:sameAs ?wikidataLink .
    FILTER(CONTAINS(STR(?wikidataLink), "wikidata"))
}
```

**CQ25:** Get player statistics with external Wikipedia links
```sparql
PREFIX cricket: <http://example.org/cricket/ontology#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?playerName ?wickets ?dbpediaLink
WHERE {
    ?stats cricket:forPlayer ?player ;
           cricket:wickets ?wickets .
    ?player rdfs:label ?playerName ;
            owl:sameAs ?dbpediaLink .
    FILTER(CONTAINS(STR(?dbpediaLink), "dbpedia"))
}
ORDER BY DESC(?wickets)
```

---

## Summary

These competency questions cover:
- **Player Information** (5 questions)
- **Bowling Performance** (6 questions)
- **Achievements** (3 questions)
- **Team Statistics** (4 questions)
- **Comparative Analysis** (3 questions)
- **Performance Classification** (2 questions)
- **External Linking** (3 questions)

**Total: 26 Competency Questions**

All questions can be answered using SPARQL queries on the RDF graph, demonstrating that the ontology is complete and fit for purpose.
