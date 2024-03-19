from langchain.schema import Document
from langchain.document_loaders.text import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings 
from langchain.vectorstores.chroma import Chroma  
from langchain.prompts import ChatPromptTemplate
from langchain_openai.llms import OpenAI
import os
from dotenv import load_dotenv
from logger import Logger


load_dotenv()

CHROMA_PATH = "chroma"

# def main():
#     generate_data_store()


def generate_data_store(question):
    documents = load_documents('faq.txt')
    chunks = split_text(documents)
    save_to_chroma(chunks)
    response = get_db_response(question)
    return response


def load_documents(text_pdf):
    try:
        loader = TextLoader(file_path=text_pdf, encoding = 'UTF-8')
        documents = loader.load()
        Logger.info({'message': 'Documents loaded sucessfully.'})
        return documents
    except Exception as err:
        Logger.error({'Documents failed to loaded': err})


def split_text(documents: list[Document]):
    try:
        text_splitter = RecursiveCharacterTextSplitter(
            separators=["\n\n", "\n", ".", " "],
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = text_splitter.split_documents(documents)
        Logger.info({'message': f'Split {len(documents)} documents into {len(chunks)} chunks.'})
        return chunks
    except Exception as err:
        Logger.error({'message': f'Open-Ai failed to split {len(documents)} documents into {len(chunks)} chunks.', 'error': err})


def save_to_chroma(chunks: list[Document]):
    # Create a new DB from the documents.
    try:
        db = Chroma.from_documents(
            chunks, OpenAIEmbeddings(api_key=os.environ.get('OPEN_AI_KEY')), persist_directory=CHROMA_PATH
        )
        db.persist()
        Logger.info({'message': f'Saved {len(chunks)} chunks to {CHROMA_PATH}.'})
    except Exception as err:
        Logger.error({'message': f'Open-Ai failed to save {len(chunks)} chunks to {CHROMA_PATH}.', 'error': err})

def get_db_response(question):
    try:

        PROMPT_TEMPLATE = """
        Answer the question based only on the following context:

        {context}

        ---

        Answer the question based on the above context: {question}
        """
        query_text = question

        # Prepare the DB.
        db = Chroma(persist_directory=CHROMA_PATH, embedding_function=OpenAIEmbeddings(api_key=os.environ.get('OPEN_AI_KEY')))

        # Search the DB.
        results = db.similarity_search_with_relevance_scores(query_text, k=3)

        if len(results) == 0 or results[0][1] < 0.5:
            Logger.info({'message': 'Sorry, I can not understand please say something'})
            return 'Sorry, I can not understand please say something'

        context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
        prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
        prompt = prompt_template.format(context=context_text, question=query_text)
        print('==========input=============',len(prompt.split()))

        model = OpenAI(api_key=os.environ.get('OPEN_AI_KEY'))
        response_text = model.predict(prompt)

        response_text = str(response_text).strip()
        print('-------output------',len(response_text.split()))
        # sources = [doc.metadata.get("source", None) for doc, _score in results]
        # formatted_response = f"Response: {response_text}\nSources: {sources}"

        Logger.info({'message': 'Formatted response fetched from chroma-db', 'response': response_text})
        return response_text
    except Exception as err:
        Logger.error({'message': 'Open-Ai failed to fetch data from chroma-db', 'error': err})

# if __name__ == "__main__":
    # chat_demo = gr.ChatInterface(generate_data_store)
    # chat_demo.launch()
    # main()
