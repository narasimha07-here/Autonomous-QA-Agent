import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader,UnstructuredMarkdownLoader,TextLoader,JSONLoader,UnstructuredHTMLLoader
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_experimental.text_splitter import SemanticChunker
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

class RAGSystem:
    def __init__(self, docs_folder: str):
        self.docs_folder = docs_folder
        self.vectorstore = None
        self.retriever = None
        self.llm = None
        self.embedding = None
        
    def load_documents(self) -> List[Document]:
        documents = [] 
        # Check if folder exists
        if not os.path.exists(self.docs_folder):
            print(f"Warning: Folder {self.docs_folder} does not exist")
            return documents    
        files = os.listdir(self.docs_folder)
        if not files:
            print(f"Warning: No files found in {self.docs_folder}")
            return documents  
        for filename in files:
            file_path = os.path.join(self.docs_folder, filename)  
            # Skip dirct
            if os.path.isdir(file_path):
                continue
            try:
                if filename.endswith('.pdf'):
                    loader = PyPDFLoader(file_path)
                elif filename.endswith('.md'):
                    loader = UnstructuredMarkdownLoader(file_path)
                elif filename.endswith('.txt'):
                    loader = TextLoader(file_path, encoding="utf-8")
                elif filename.endswith('.json'):
                    loader = JSONLoader(
                        file_path=file_path,
                        jq_schema='.',
                        text_content=False
                    )
                elif filename.endswith('.html'):
                    loader = UnstructuredHTMLLoader(file_path)
                else:
                    print(f"Unsupported file type: {filename}")
                    continue
                loaded_docs = loader.load()
                documents.extend(loaded_docs)
                print(f"✓ Loaded {filename} ({len(loaded_docs)} documents)")
                
            except Exception as e:
                print(f"✗ Error loading {filename}: {str(e)}")
                continue
        print(f"Total documents loaded: {len(documents)}")
        return documents
    
    def build_knowledge_base(self):  
        print("Starting knowledge base build...")
        print("Initializing LLM...")
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            google_api_key=os.environ["GOOGLE_API_KEY"],
            temperature=0.3
        )
        print("Initializing embeddings...")
        self.embedding = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
            encode_kwargs={'normalize_embeddings': True}
        )
        print("Loading documents...")
        documents = self.load_documents() 
        if not documents:
            raise ValueError("❌ No documents were loaded. Please upload documents first.")
        print(f"✓ Loaded {len(documents)} documents")
        print("Splitting documents into chunks...")
        splitter = SemanticChunker(embeddings=self.embedding,breakpoint_threshold_type="standard_deviation")
        chunks = splitter.split_documents(documents)
        if not chunks:
            raise ValueError("❌ No chunks created from documents.")
        print(f"✓ Created {len(chunks)} chunks")       
        print("Creating vector store...")
        self.vectorstore = Chroma.from_documents(
            documents=chunks,
            embedding=self.embedding,
            persist_directory="./chroma_db"
        )
        self.retriever = self.vectorstore.as_retriever(
            search_kwargs={"k": 5}
        )
        print("✓ Knowledge base built successfully!")
    
    def query_knowledge_base(self, question: str) -> str:
        if not self.retriever:
            raise ValueError("Knowledge base not built. Please build it first.")
        relevant_docs = self.retriever.invoke(question)
        context_parts = []
        for doc in relevant_docs:
            source_name = doc.metadata.get("source", "Unknown_Source")
            context_parts.append(f"[SOURCE: {source_name}]\n{doc.page_content}")
        context = "\n\n".join(context_parts)
        return context
    
    def generate_response(self, question: str) -> str:
        context = self.query_knowledge_base(question)
        template = """You are a QA expert. Answer the question based ONLY on the following context.
                If the context doesn't contain the answer, say "The provided documents don't contain information about this."

                Context:
                {context}

                Question: {question}

                Answer: """
        
        prompt = ChatPromptTemplate.from_template(template)
        rag_chain = (
            {"context": lambda x: context, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return rag_chain.invoke(question)
