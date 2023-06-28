import warnings

from haystack import Pipeline
from haystack.document_stores import OpenSearchDocumentStore
from haystack.nodes import AnswerParser, EmbeddingRetriever, PromptNode, PromptTemplate
from haystack.utils import print_answers
from config import OPENSEARCH_HOST, OPENSEARCH_PORT, OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD, SAGEMAKER_MODEL_ENDPOINT, AWS_PROFILE_NAME, AWS_REGION_NAME

warnings.filterwarnings("ignore")

def start_query_pipeline():
    doc_store = OpenSearchDocumentStore(host=OPENSEARCH_HOST, port=OPENSEARCH_PORT, username=OPENSEARCH_USERNAME, password=OPENSEARCH_PASSWORD, embedding_dim=384)

    question_answering = PromptTemplate(prompt="Given the context please answer the question. If the answer is not contained within the context below, say 'I don't know'.\n" 
                                                "Context: {join(documents)};\n Question: {query};\n Answer: ", output_parser=AnswerParser(reference_pattern=r"Document\[(\d+)\]"))

    gen_qa_prompt = PromptNode(default_prompt_template=question_answering,  max_length=200, model_name_or_path=SAGEMAKER_MODEL_ENDPOINT, model_kwargs={"aws_profile_name": AWS_PROFILE_NAME, 
                                                                                                                                       "aws_region_name": AWS_REGION_NAME})
    retriever = EmbeddingRetriever(document_store=doc_store, embedding_model="sentence-transformers/all-MiniLM-L12-v2", devices=["mps"])

    pipe = Pipeline()
    pipe.add_node(component=retriever, name="Retriever", inputs=['Query'])
    pipe.add_node(component=gen_qa_prompt, name="GenQAWPromptNode", inputs=["Retriever"])
    return pipe

if __name__ == "__main__":
    print('Starting up the query pipeline...')
    query_pipeline = start_query_pipeline()

    while True:
        query = input("Ask a question: ")
        result = query_pipeline.run(query, params={"Retriever":{"top_k": 5}})
        print(result['answers'][0].answer)