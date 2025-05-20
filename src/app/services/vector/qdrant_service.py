from typing import List, Optional, Dict, Any
from qdrant_client import QdrantClient
from qdrant_client.http import models
from loguru import logger

from ...core.config import settings
from ...core.exceptions import (
    VectorServiceError,
    CollectionNotFoundError,
    CollectionCreateError,
    VectorOperationError,
    ServiceConnectionError
)

class QdrantService:
    def __init__(self):
        try:
            self.client = QdrantClient(
                host=settings.QDRANT_HOST,
                port=settings.QDRANT_PORT
            )
        except Exception as e:
            raise ServiceConnectionError("Qdrant", str(e))

    async def create_collection(
        self,
        collection_name: str,
        vector_size: int = 768
    ) -> None:
        """Create a new collection."""
        try:
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                    size=vector_size,
                    distance=models.Distance.COSINE
                )
            )
        except Exception as e:
            logger.error(f"Error creating collection: {e}")
            raise CollectionCreateError(f"Failed to create collection: {str(e)}")

    async def upsert_vectors(
        self,
        collection_name: str,
        vectors: List[List[float]],
        payloads: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> None:
        """Upsert vectors into collection."""
        try:
            if not self.client.collection_exists(collection_name):
                raise CollectionNotFoundError(collection_name)
                
            self.client.upsert(
                collection_name=collection_name,
                points=models.Batch(
                    ids=ids,
                    vectors=vectors,
                    payloads=payloads
                )
            )
        except CollectionNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error upserting vectors: {e}")
            raise VectorOperationError(f"Failed to upsert vectors: {str(e)}")

    async def search_vectors(
        self,
        collection_name: str,
        query_vector: List[float],
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Search for similar vectors."""
        try:
            if not self.client.collection_exists(collection_name):
                raise CollectionNotFoundError(collection_name)
                
            results = self.client.search(
                collection_name=collection_name,
                query_vector=query_vector,
                limit=limit
            )
            return [
                {
                    "id": hit.id,
                    "score": hit.score,
                    "payload": hit.payload
                }
                for hit in results
            ]
        except CollectionNotFoundError:
            raise
        except Exception as e:
            logger.error(f"Error searching vectors: {e}")
            raise VectorOperationError(f"Failed to search vectors: {str(e)}")