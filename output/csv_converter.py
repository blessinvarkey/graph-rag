import pandas as pd

# read graphs
entities = pd.read_parquet("entities.parquet")
rels     = pd.read_parquet("relationships.parquet")

# write CSVs
entities.to_csv("neo4j_import/entities.csv", index=False)
rels.to_csv("neo4j_import/relationships.csv", index=False)
