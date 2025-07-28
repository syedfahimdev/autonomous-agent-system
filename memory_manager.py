import os
import json
import pickle
from datetime import datetime
from typing import List, Dict, Any
from langchain.memory import ConversationBufferMemory
import config

class MemoryManager:
    def __init__(self):
        self.memory_path = config.MEMORY_PATH
        self.conversation_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        self.vector_store = None
        self._load_memory()
    
    def _load_memory(self):
        """Load existing memory from disk"""
        try:
            # Load conversation memory
            memory_file = os.path.join(self.memory_path, "conversation_memory.json")
            if os.path.exists(memory_file):
                with open(memory_file, 'r') as f:
                    memory_data = json.load(f)
                    self.conversation_memory.chat_memory.messages = memory_data.get("messages", [])
            
            # Try to initialize FAISS if OpenAI API key is available
            if config.OPENAI_API_KEY and config.OPENAI_API_KEY != "your_openai_api_key_here":
                try:
                    from langchain_community.vectorstores import FAISS
                    from langchain_openai import OpenAIEmbeddings
                    from langchain.schema import Document
                    
                    self.embeddings = OpenAIEmbeddings(openai_api_key=config.OPENAI_API_KEY)
                    
                    # Load FAISS index
                    faiss_path = config.FAISS_INDEX_PATH
                    if os.path.exists(faiss_path):
                        self.vector_store = FAISS.load_local(faiss_path, self.embeddings)
                    else:
                        # Create initial document to initialize FAISS
                        initial_doc = Document(
                            page_content="Initial memory document",
                            metadata={
                                'task_id': 'initial',
                                'timestamp': datetime.now().isoformat(),
                                'task_type': 'system',
                                'result': 'System initialization'
                            }
                        )
                        self.vector_store = FAISS.from_documents([initial_doc], self.embeddings)
                        print("✅ FAISS vector store initialized successfully")
                        
                except Exception as e:
                    print(f"⚠️ Could not initialize FAISS: {e}")
                    self.vector_store = None
            else:
                print("⚠️ OpenAI API key not configured, FAISS will be disabled")
                self.vector_store = None
                
        except Exception as e:
            print(f"Warning: Could not load memory: {e}")
            self.vector_store = None
    
    def save_memory(self):
        """Save memory to disk"""
        try:
            # Save conversation memory
            memory_file = os.path.join(self.memory_path, "conversation_memory.json")
            memory_data = {
                "messages": [msg.dict() for msg in self.conversation_memory.chat_memory.messages],
                "last_updated": datetime.now().isoformat()
            }
            with open(memory_file, 'w') as f:
                json.dump(memory_data, f, indent=2)
            
            # Save FAISS index
            if self.vector_store:
                faiss_path = config.FAISS_INDEX_PATH
                self.vector_store.save_local(faiss_path)
            
        except Exception as e:
            print(f"Warning: Could not save memory: {e}")
    
    def add_task_memory(self, task_id: str, task_data: Dict[str, Any]):
        """Add task data to memory"""
        try:
            # Add to conversation memory
            self.conversation_memory.chat_memory.add_user_message(
                f"Task {task_id}: {task_data.get('prompt', '')}"
            )
            
            # Add to vector store for semantic search if available
            if self.vector_store:
                from langchain.schema import Document
                doc = Document(
                    page_content=task_data.get('prompt', ''),
                    metadata={
                        'task_id': task_id,
                        'timestamp': datetime.now().isoformat(),
                        'task_type': task_data.get('type', 'general'),
                        'result': task_data.get('result', '')
                    }
                )
                self.vector_store.add_documents([doc])
            
            # Save memory
            self.save_memory()
            
        except Exception as e:
            print(f"Warning: Could not add task memory: {e}")
    
    def search_similar_tasks(self, query: str, k: int = 5) -> List[Dict]:
        """Search for similar tasks in memory"""
        try:
            if not self.vector_store:
                return []
            
            docs = self.vector_store.similarity_search(query, k=k)
            return [
                {
                    'content': doc.page_content,
                    'metadata': doc.metadata
                }
                for doc in docs
            ]
        except Exception as e:
            print(f"Warning: Could not search memory: {e}")
            return []
    
    def get_task_history(self, limit: int = 10) -> List[Dict]:
        """Get recent task history"""
        try:
            messages = self.conversation_memory.chat_memory.messages[-limit:]
            return [
                {
                    'role': msg.type,
                    'content': msg.content,
                    'timestamp': datetime.now().isoformat()
                }
                for msg in messages
            ]
        except Exception as e:
            print(f"Warning: Could not get task history: {e}")
            return [] 