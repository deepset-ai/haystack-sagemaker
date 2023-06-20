# Haystack Genertative QA Pipelines with SageMaker
This repo is a showcase of how you can use models deployed on AWS SageMaker in your Haystack Gen AI pipelines.

## The Data
This showcase includes some documents we've crawled form the OpenSearch website and documentation pages. They've been indexed into an `OpenSearchDocumentStore` 
with the `create_opensearch_index.py` script.
The raw data is in the `/data` folder. Feel free to re-use them for your own testing and demos 🎉

## The Model
For this demo, we've deployed the falcon-40b-instruct model on AWS SageMaker with the JumpStart program which makes the deployment process really smooth.
