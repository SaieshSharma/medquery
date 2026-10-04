from typing import Any
from uuid import NAMESPACE_URL, uuid5

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, PointStruct, ScoredPoint, VectorParams


class QdrantVectorStore:
    def __init__(
        self,
        url: str,
        collection_name: str,
        vector_size: int,
    ) -> None:
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
        self.vector_size = vector_size

    def ensure_collection(self) -> None:
        if self.client.collection_exists(self.collection_name):
            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(
                size=self.vector_size,
                distance=Distance.COSINE,
            ),
        )

    def upsert(
        self,
        point_id: str,
        vector: list[float],
        payload: dict[str, Any],
    ) -> None:
        qdrant_id = str(uuid5(NAMESPACE_URL, point_id))

        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=qdrant_id,
                    vector=vector,
                    payload=payload,
                )
            ],
        )

    def search(
    self,
    query_vector: list[float],
    limit: int = 5,   # top k retrieval
) -> list[ScoredPoint]:
        return self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=limit,
        ).points

    def upsert_batch(
    self,
    points: list[tuple[str, list[float], dict[str, Any]]],
) -> None:
        qdrant_points = []

        for point_id, vector, payload in points:
            qdrant_id = str(uuid5(NAMESPACE_URL, point_id))

            qdrant_points.append(
                PointStruct(
                    id=qdrant_id,
                    vector=vector,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=qdrant_points,
        )