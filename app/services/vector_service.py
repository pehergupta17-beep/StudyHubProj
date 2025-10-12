import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import uuid
from typing import List, Dict, Optional
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VectorService:
    def __init__(self):
        self.persist_directory = os.getenv('CHROMA_PERSIST_DIRECTORY', './chroma_db')

        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=self.persist_directory,
            settings=Settings(anonymized_telemetry=False)
        )

        # Initialize sentence transformer for embeddings
        try:
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("Sentence transformer loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load sentence transformer: {e}")
            self.encoder = None

        # Create or get collections
        self._init_collections()

    def _init_collections(self):
        """Initialize ChromaDB collections"""
        try:
            # Collection for conversation history
            self.conversations_collection = self.client.get_or_create_collection(
                name="conversations",
                metadata={"description": "Student conversation history"}
            )

            # Collection for study resources and knowledge
            self.knowledge_collection = self.client.get_or_create_collection(
                name="study_knowledge",
                metadata={"description": "Study tips, resources, and educational content"}
            )

            # Collection for user context and preferences
            self.user_context_collection = self.client.get_or_create_collection(
                name="user_context",
                metadata={"description": "User preferences and learning patterns"}
            )

            logger.info("ChromaDB collections initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize collections: {e}")

    def store_conversation(self, user_id: str, user_message: str, bot_response: str,
                         conversation_context: Optional[Dict] = None) -> bool:
        """
        Store a conversation exchange in the vector database

        Args:
            user_id: Unique identifier for the user
            user_message: The user's input message
            bot_response: The bot's response
            conversation_context: Additional context about the conversation

        Returns:
            True if stored successfully, False otherwise
        """
        if not self.encoder:
            return False

        try:
            # Create combined text for embedding
            combined_text = f"User: {user_message}\nBot: {bot_response}"

            # Generate embedding
            embedding = self.encoder.encode(combined_text).tolist()

            # Prepare metadata
            metadata = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "user_message_length": len(user_message),
                "response_length": len(bot_response),
                "conversation_type": "chat"
            }

            if conversation_context:
                metadata.update(conversation_context)

            # Store in collection
            conversation_id = str(uuid.uuid4())
            self.conversations_collection.add(
                ids=[conversation_id],
                embeddings=[embedding],
                documents=[combined_text],
                metadatas=[metadata]
            )

            logger.info(f"Stored conversation for user {user_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to store conversation: {e}")
            return False

    def get_relevant_conversations(self, user_id: str, query: str, limit: int = 5) -> List[Dict]:
        """
        Retrieve relevant past conversations for context

        Args:
            user_id: Unique identifier for the user
            query: Current user query to find relevant past conversations
            limit: Maximum number of conversations to return

        Returns:
            List of relevant conversation dictionaries
        """
        if not self.encoder:
            return []

        try:
            # Generate embedding for the query
            query_embedding = self.encoder.encode(query).tolist()

            # Search for relevant conversations
            results = self.conversations_collection.query(
                query_embeddings=[query_embedding],
                where={"user_id": user_id},
                n_results=limit,
                include=["documents", "metadatas", "distances"]
            )

            relevant_conversations = []
            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    distance = results['distances'][0][i] if results['distances'] else 1.0

                    # Only include conversations with reasonable similarity
                    if distance < 0.8:  # Adjust threshold as needed
                        relevant_conversations.append({
                            'content': doc,
                            'metadata': metadata,
                            'similarity': 1 - distance
                        })

            return relevant_conversations

        except Exception as e:
            logger.error(f"Failed to retrieve relevant conversations: {e}")
            return []

    def store_study_knowledge(self, title: str, content: str, category: str,
                            tags: Optional[List[str]] = None) -> bool:
        """
        Store study-related knowledge in the vector database

        Args:
            title: Title of the knowledge item
            content: The actual content/information
            category: Category (e.g., "study_tips", "time_management", "motivation")
            tags: Optional list of tags for better categorization

        Returns:
            True if stored successfully, False otherwise
        """
        if not self.encoder:
            return False

        try:
            # Generate embedding for the content
            combined_text = f"{title}\n{content}"
            embedding = self.encoder.encode(combined_text).tolist()

            # Prepare metadata
            metadata = {
                "title": title,
                "category": category,
                "timestamp": datetime.now().isoformat(),
                "content_length": len(content)
            }

            if tags:
                metadata["tags"] = ",".join(tags)

            # Store in knowledge collection
            knowledge_id = str(uuid.uuid4())
            self.knowledge_collection.add(
                ids=[knowledge_id],
                embeddings=[embedding],
                documents=[combined_text],
                metadatas=[metadata]
            )

            logger.info(f"Stored knowledge: {title}")
            return True

        except Exception as e:
            logger.error(f"Failed to store knowledge: {e}")
            return False

    def search_study_knowledge(self, query: str, category: Optional[str] = None, limit: int = 3) -> List[Dict]:
        """
        Search for relevant study knowledge

        Args:
            query: Search query
            category: Optional category filter
            limit: Maximum number of results

        Returns:
            List of relevant knowledge items
        """
        if not self.encoder:
            return []

        try:
            # Generate embedding for the query
            query_embedding = self.encoder.encode(query).tolist()

            # Prepare where clause
            where_clause = {}
            if category:
                where_clause["category"] = category

            # Search for relevant knowledge
            results = self.knowledge_collection.query(
                query_embeddings=[query_embedding],
                where=where_clause if where_clause else None,
                n_results=limit,
                include=["documents", "metadatas", "distances"]
            )

            knowledge_items = []
            if results and results['documents']:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    distance = results['distances'][0][i] if results['distances'] else 1.0

                    knowledge_items.append({
                        'content': doc,
                        'metadata': metadata,
                        'similarity': 1 - distance
                    })

            return knowledge_items

        except Exception as e:
            logger.error(f"Failed to search knowledge: {e}")
            return []

    def update_user_context(self, user_id: str, context_data: Dict) -> bool:
        """
        Update or create user context information

        Args:
            user_id: Unique identifier for the user
            context_data: Dictionary containing user context information

        Returns:
            True if updated successfully, False otherwise
        """
        try:
            # Check if user context already exists
            existing = self.user_context_collection.get(
                where={"user_id": user_id},
                include=["documents", "metadatas"]
            )

            context_text = json.dumps(context_data, default=str)
            metadata = {
                "user_id": user_id,
                "timestamp": datetime.now().isoformat(),
                "context_keys": ",".join(context_data.keys())
            }

            if existing and existing['ids']:
                # Update existing context
                context_id = existing['ids'][0]
                self.user_context_collection.update(
                    ids=[context_id],
                    documents=[context_text],
                    metadatas=[metadata]
                )
            else:
                # Create new context
                if self.encoder:
                    embedding = self.encoder.encode(context_text).tolist()
                    context_id = str(uuid.uuid4())
                    self.user_context_collection.add(
                        ids=[context_id],
                        embeddings=[embedding],
                        documents=[context_text],
                        metadatas=[metadata]
                    )

            return True

        except Exception as e:
            logger.error(f"Failed to update user context: {e}")
            return False

    def get_user_context(self, user_id: str) -> Optional[Dict]:
        """
        Retrieve user context information

        Args:
            user_id: Unique identifier for the user

        Returns:
            User context dictionary or None if not found
        """
        try:
            results = self.user_context_collection.get(
                where={"user_id": user_id},
                include=["documents", "metadatas"]
            )

            if results and results['documents']:
                context_text = results['documents'][0]
                return json.loads(context_text)

            return None

        except Exception as e:
            logger.error(f"Failed to get user context: {e}")
            return None

    def initialize_study_knowledge(self):
        """Initialize the database with basic study knowledge"""
        study_tips = [
            {
                "title": "Active Recall Technique",
                "content": "Instead of just re-reading notes, test yourself by covering the material and trying to remember key points. This strengthens memory formation and identifies knowledge gaps.",
                "category": "study_techniques",
                "tags": ["memory", "retention", "testing"]
            },
            {
                "title": "Spaced Repetition",
                "content": "Review material at increasing intervals (1 day, 3 days, 1 week, 2 weeks). This method leverages the psychological spacing effect for long-term retention.",
                "category": "study_techniques",
                "tags": ["memory", "retention", "scheduling"]
            },
            {
                "title": "Pomodoro Technique for Students",
                "content": "Study for 25 minutes with complete focus, then take a 5-minute break. After 4 cycles, take a longer 15-30 minute break. This prevents burnout and maintains concentration.",
                "category": "time_management",
                "tags": ["focus", "breaks", "productivity"]
            },
            {
                "title": "Creating a Study Environment",
                "content": "Designate a specific area for studying, keep it organized and free from distractions. Good lighting, comfortable temperature, and necessary supplies help maintain focus.",
                "category": "study_environment",
                "tags": ["focus", "organization", "environment"]
            }
        ]

        for tip in study_tips:
            self.store_study_knowledge(
                title=tip["title"],
                content=tip["content"],
                category=tip["category"],
                tags=tip.get("tags", [])
            )

# Global instance
vector_service = VectorService()