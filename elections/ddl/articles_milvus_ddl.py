"""
Running file directly will drop and recreate the 'articles' collection 
in the Milvus database, with the following fields:
* id: INT64, primary key, auto increment
* title: VARCHAR(150)
* description: VARCHAR(1_000)
* text: VARCHAR(64_000)
* embedding: FLOAT_VECTOR(1536)
"""

from pymilvus import (
    connections, utility, FieldSchema,
    Collection, CollectionSchema, DataType
)

from elections import constants


ARTICLES_COLLECTION = 'articles'
DIMENSION = 1536
INDEX_PARAM = {
    'metric_type':'L2',
    'index_type':"HNSW",
    'params':{'M': 8, 'efConstruction': 64}
}

QUERY_PARAM = {
    "metric_type": "L2",
    "params": {"ef": 64},
}

# Create collection which includes the id, title, and embedding.
fields = [
    FieldSchema(name='id', dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name='title', dtype=DataType.VARCHAR, max_length=150),
    FieldSchema(name='description', dtype=DataType.VARCHAR, max_length=1_000),
    FieldSchema(name='text', dtype=DataType.VARCHAR, max_length=64_000),
    FieldSchema(name='embedding', dtype=DataType.FLOAT_VECTOR, dim=DIMENSION)
]


if __name__ == "__main__":
    # Connect to Milvus Database
    connections.connect(host=constants.MILVUS_HOST, port=constants.MILVUS_PORT)
    
    # Remove collection if it already exists
    if utility.has_collection(ARTICLES_COLLECTION):
        utility.drop_collection(ARTICLES_COLLECTION)

    schema = CollectionSchema(fields=fields)
    collection = Collection(name=ARTICLES_COLLECTION, schema=schema)

    # Create the index on the collection and load it.
    collection.create_index(field_name="embedding", index_params=INDEX_PARAM)
    
    collection.load()

