import boto3
import os
import sys
from haystack import Pipeline
from haystack.document_stores import OpenSearchDocumentStore
from haystack.nodes import EmbeddingRetriever, JsonConverter, PreProcessor
from config import OPENSEARCH_HOST, OPENSEARCH_PORT, OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD

def fetch_files():
    s3 = boto3.client('s3')
    s3.download_file('haystack-public-demo-files', 'haystack-sagemaker-demo/opensearch-documentation-2.7.json', 'data/opensearch-documentation-2.7.json')
    s3.download_file('haystack-public-demo-files', 'haystack-sagemaker-demo/opensearch-website.json', 'data/opensearch-website.json')

def write_documents():
    doc_store = OpenSearchDocumentStore(host=OPENSEARCH_HOST, port=OPENSEARCH_PORT, username=OPENSEARCH_USERNAME, password=OPENSEARCH_PASSWORD, embedding_dim=384)
    
    converter = JsonConverter()
    preprocessor = PreProcessor (
            clean_empty_lines=True, 
            split_by='word',
            split_respect_sentence_boundary=True,
            split_length=80,
            split_overlap=20
        )
    retriever = EmbeddingRetriever(document_store=doc_store, embedding_model="sentence-transformers/all-MiniLM-L12-v2", devices=["mps"], top_k=5)

    indexing_pipeline = Pipeline()
    indexing_pipeline.add_node(component=converter, name="Converter", inputs=["File"])
    indexing_pipeline.add_node(component=preprocessor, name="Preprocessor", inputs=["Converter"])
    indexing_pipeline.add_node(component=retriever, name="Retriever", inputs=["Preprocessor"])
    indexing_pipeline.add_node(component=doc_store, name="DocumentStore", inputs=["Retriever"])
    
    files_to_index = ["data/" + f for f in os.listdir("data")]
    indexing_pipeline.run(file_paths=files_to_index)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--fetch-files" :
        fetch_files()
    write_documents()