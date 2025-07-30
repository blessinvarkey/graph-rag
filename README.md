# GraphRAG Knowledge Graph 

This repository uses **GraphRAG** to build a knowledge graph which ingests structured JSON, extracts entities & relationships, and enables semantic queries and graph visualizations.

---

## 📂 Project Structure

```text
├── gragtest/                  # GraphRAG project root
│   ├── input/                 # Ingested JSON files
│   │   └── input.json         # AdvisorMapping, SubmissionLog, etc.
│   ├── output/                # Generated Parquet outputs
│   ├── cache/                 # Embedding cache
│   ├── logs/                  # Indexing logs
│   ├── prompts/               # Custom prompt templates
│   ├── settings.yaml          # GraphRAG configuration (ignored)
│   └── .env                   # API keys (ignored)
├── entities.csv               # CSV export of entities
├── relationships.csv          # CSV export of relationships
├── export_to_csv.py           # Parquet → CSV script
├── .gitignore
└── README.md                  # You are here
```

---

## ⚙️ Prerequisites

- **Python 3.11+**
- **pip**
- **GraphRAG CLI** (`pip install graphrag`)
- **OpenAI API key** (set in `gragtest/.env`)
- **Neo4j** (for graph visualization)

---

## 🚀 Setup & Indexing

1. **Clone the repo**
   ```bash
   git clone https://github.com/blessinvarkey/graph-rag.git
   cd graph-rag
   ```

2. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install graphrag pandas neo4j
   ```

3. **Configure environment**
   - Copy your OpenAI key into `gragtest/.env`:
     ```env
     GRAPHRAG_API_KEY=sk-<your-new-key>
     ```

4. **Run indexing**
   ```bash
   graphrag index --root gragtest
   ```
   - Produces Parquet files in `gragtest/output`
   - Entities, relationships, text units, and community reports

---

## 🔍 Querying

- **Local search** (focused on specific entities):
  ```bash
  graphrag query -r gragtest -m local -q "Tell me about the AdvisorMapping table"
  ```

- **Global search** (aggregate summaries):
  ```bash
  graphrag query -r gragtest -m global -q "Summarize key tables and relationships"
  ```

- **Drift search** (contextual exploration):
  ```bash
  graphrag query -r gragtest -m drift -q "How has the advisor network evolved?"
  ```

---

## 📊 Export & Visualize in Neo4j

1. **Convert Parquet → CSV**
   ```bash
   python export_to_csv.py
   ```
   - Generates `entities.csv`, `relationships.csv`

2. **Copy to Neo4j import**
   ```bash
   cp entities.csv relationships.csv /usr/local/var/lib/neo4j/import/
   ```

3. **Load in Neo4j Browser**
   ```cypher
   LOAD CSV WITH HEADERS FROM 'file:///entities.csv' AS row
   CREATE (:Entity {id: row.id, name: row.name, type: row.type});

   LOAD CSV WITH HEADERS FROM 'file:///relationships.csv' AS row
   MATCH (a:Entity {id: row.source_id}), (b:Entity {id: row.target_id})
   CREATE (a)-[:RELATED {label:row.relation, weight:toFloat(row.weight)}]->(b);
   ```

4. **Explore visually** at `http://localhost:7474`.

---

## 🎨 Customization

- **Few‑shot SQL**: Add `few_shot.sql.txt` in `input/`, update `prompts/sql_generation_prompt.txt` and rerun indexing.
- **Prompt tuning**: Modify files under `prompts/` for different RAG workflows.
- **Vector store**: Swap `lancedb` for your preferred vector DB in `settings.yaml`.

---

