# Haystack Generative QA Pipelines with SageMaker Jumpstart
This repo is a showcase of how you can use models deployed on AWS SageMaker Jumpstart in your Haystack Gen AI pipelines.

## The Data
This showcase includes some documents we've crawled form the OpenSearch website and documentation pages. 
You can index these into your own `OpenSearchDocumentStore` using `opensearch_indexing_pipeline.ipynb`.

## The Model
For this demo, we deployed the `falcon-40b-instruct` model on SageMaker Jumpstart. Once deployed, you can use your own credentials in the `PromptNode` in `gen_qa_pipeline.ipynb`

## The RAG Pipleine
Haystack has two main types of pipelines: an indexing pipeline, and a query pipeline.

An indexing pipeline prepares and writes documents to a `DocumentStore` so that they are in a format which is useable by your choice of NLP pipeline and language models.

A query pipeline on the other hand is any combination of Haystack nodes that may consume a user query and result in a response.
Here, you will find a retrieval augmented question answering pipeine in `gen_qa_pipeline.ipynb`:

