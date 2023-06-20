ARG HAYSTACK_BASE_IMAGE
FROM $HAYSTACK_BASE_IMAGE

CMD ["python3", "create_opensearch_index.py"]