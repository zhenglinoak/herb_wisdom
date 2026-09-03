from pydantic import BaseModel
from typing import Optional


class DocMetadata(BaseModel):
    drug_name: Optional[str] = ""
    disease: Optional[str] = ""
    source: Optional[str] = ""


class RetrievedDoc(BaseModel):
    id: str
    metadata: DocMetadata
    page_content: str


class DocsPayload(BaseModel):
    vector_docs: list[RetrievedDoc] = []
    bm25_docs: list[RetrievedDoc] = []