# Haystack Generative QA Pipelines with SageMaker Jumpstart
This repo is a showcase of how you can use models deployed on AWS SageMaker Jumpstart in your Haystack Gen AI pipelines.

## The Data
This showcase includes some documents we've crawled form the OpenSearch website and documentation pages. 
You can index these into your own `OpenSearchDocumentStore` using `opensearch_indexing_pipeline.ipynb`.

## The Model
For this demo, we deployed the `falcon-40b-instruct` model on SageMaker Jumpstart. Once deployed, you can use your own credentials in the `PromptNode`.
To deploy a model on JumpStart, simply login to your AWS account and go to the Studio on SageMaker. 
Navigate to JumpStart and deploy `falcon-40b-instruct`. This may take a few minutes:
<img width="949" alt="image" src="https://github.com/deepset-ai/haystack-sagemaker/assets/15802862/b7a1adee-eb9c-4258-b3e0-bf5942f9c960">

## Indexing Documents to OpenSearch
To run the scripts and notebooks provided here, first clone the repo and install the requirements.
```bash
git clone git@github.com:deepset-ai/haystack-sagemaker.git
cd haystack-sagemaker
pip instaall -r requirements.txt
```

### Starting an OpenSearch service
#### Option 1: OpenSearch service on AWS
**Requirements:** An AWS account and AWS CLI

You can use the provided CloudFormation template `opsearch-index.yaml` to deploy an OpenSearch service on AWS.

Set the `--stack-name` and `OSPassword` to your preferred values and run the following.
You may also change the dedault `OSDomainName` and `OSUsername` values, set to `opensearch-haystack-domain` and `admin` respecively, in `opensearch-index.yaml`

```bash
aws cloudformation create-stack --stack-name HaystackOpensearch --template-body file://cloudformation/opensearch-index.yaml --parameters ParameterKey=InstanceType,ParameterValue=r5.large.search ParameterKey=InstanceCount,ParameterValue=3 ParameterKey=OSPassword,ParameterValue=Password123!
```
You can then retrieve your OpenSearch host required to [Write documents](##write-documents) by running:
```bash
aws cloudformation describe-stacks --stack-name HaystackOpensearch --query "Stacks[0].Outputs[?OutputKey=='OpenSearchEndpoint'].OutputValue" --output text
```
#### Option 2: Local OpenSearch service
**Requirements:** Docker

Another option is to have a local OpenSearch service. For this, you may simply run:
```python
from haystack.utils import launch_opensearch

launch_opensearch()
```
This will start an OpenSearch service on `localhost:9200`

## Writing documents
You can use a Haystack indexing pipeline to prepare and write documents to an `OpenSearchDocumentStore`.
1. Set your environment variables:
```bash
export OPENSEARCH_HOST='your_opensearch_host'
export OPENSEARCH_PORT='your_opensearch_port'
export OPENSEARCH_USERNAME='your_opensearch_username'
export OPENSEARCH_PASSWORD='your_opensearch_password'
```
2. Use the indexing pipeline to write the preprocessed documsnts to your OpenSearch index:
## Option 1:
For this demo, we've prepared documents which have been crawled from the OpenSearch documenation and website. As an example of how you may use an S3 bucket, we've also mde them available [here](https://haystack-public-demo-files.s3.eu-central-1.amazonaws.com/haystack-sagemaker-demo/opensearch-documentation-2.7.json) and [here](https://haystack-public-demo-files.s3.eu-central-1.amazonaws.com/haystack-sagemaker-demo/opensearch-website.json)

Run `python opensearch_indexing_pipeline.py --fetch-files` to fetch these 2 files from S3 or modify the sourcecode in `opensearch_indexing_pipeline.py` to fetch your own files from an S3 bucket. This will fetch the specified files from the S3 bucket, and put them in `data/`. The script will then preprocess and prepare `Documents` from these files, and write them to your `OpenSearchDocumentStore`.

## Option 2:
Run `python opensearch_indexing_pipeline.py`

This will write the same files, already available in `data/`, to your `OpenSearchDocumentStore`


## The RAG Pipleine
Haystack has two main types of pipelines: an indexing pipeline, and a query pipeline.

An indexing pipeline prepares and writes documents to a `DocumentStore` so that they are in a format which is useable by your choice of NLP pipeline and language models.

A query pipeline on the other hand is any combination of Haystack nodes that may consume a user query and result in a response.
Here, you will find a retrieval augmented question answering pipeine in `gen_qa_pipeline.ipynb`:

