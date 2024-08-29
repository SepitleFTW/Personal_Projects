import itertools
import boto3
import chromadb
from chromadb.utils.embedding_functions import AmazonBedrockEmbeddingFunction


MAX_MESSAGES = 20

class ChatMessage(): #this class stores images and text messages
    def __init__(self, role, text):
        self.role = role
        self.text = text

    def get_collection(path, collection_name):
        session = boto3.Session()
        embedding_function = A

