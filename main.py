import wikipedia
import chromadb
import openai

class ObamaQA():

    def __init__(self, openAiApiKey, chromaDb):

        openai.api_key = openAiApiKey

        self.client = chromadb.Client()

        self.collection = self.client.create_collection(name="obamaWiki")

        self.fetchParagraphs("Barack Obama")

    def fetchParagraphs(self, person):
        page = wikipedia.page(person)
        paragraphs = []
        for paragraph in page.content.split('\n'):
            paragraphs.append(paragraph)

        self.collection.add(
            documents=paragraphs,
            ids=[f"paragraph {i}" for i in range(len(paragraphs))]  
        )

    
    def getRelevantInfoToQuery(self, query):
        # self.collection.query is part of the ChromaDB library, which is responsible for querying the database to retrieve 
        # relevant documents based on the provided input. Although it has same name as query (class function), it does not call 
        # the query class function (that's a class function for the class not the chromaDb obejct)
        results = self.collection.query(
            query_texts=[query],  
            n_results=3 
        )
        return results
    
    def query(self, query):
        relevant_info = self.getRelevantInfoToQuery(query)
        return relevant_info  
