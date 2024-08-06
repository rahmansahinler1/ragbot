import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import globals
import time 

class EmbeddingFunctions:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI()

    def create_vector_embeddings_from_pdf(self,batch_size=500):
        pdf_embeddings = []
        total_time = 0
        sentences = globals.pdf_sentences
        globals.kpi_dict["batch_size"] = batch_size #Inputing batch_size value to kpi dictionary 
        globals.kpi_dict["sentence_amount"] = len(pdf_embeddings) #Inputing sentence_amount value to kpi dictionary
        batches = [sentences[i:i+batch_size] for i in range(0,len(sentences),batch_size)]
        
        start_time = time.time()
        for batch in batches:
            sentence_embedding = self.client.embeddings.create(
                model="text-embedding-ada-002", input=batch
            )
        end_time = time.time()
        total_time = end_time-start_time
        pdf_embeddings.extend(sentence_embedding.data) 

        globals.kpi_dict["total_emd_time"] = total_time #Inputing total_emd_time value to kpi dictionary 
        globals.kpi_dict["avg_emd_time"] = total_time/len(pdf_embeddings) #Inputing total avg_emd_time value to kpi dictionary 

        
        globals.pdf_embeddings = np.array(
            [x.embedding for x in pdf_embeddings], float
        )

    def create_vector_embedding_from_query(self, query):
        query_embedding = self.client.embeddings.create(
            model="text-embedding-ada-002", input=query
        )
        return np.array(query_embedding.data[0].embedding, float).reshape(1, -1)