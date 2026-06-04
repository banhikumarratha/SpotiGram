"""
In-memory DNA repository — implements DNARepositoryPort.
Used in development/testing.  A future phase can swap this for a Redis or
Postgres-backed implementation without touching any application code.
"""
from typing import Dict, Optional
from domain.models import MusicDNA
from domain.ports import DNARepositoryPort


class InMemoryDNARepository(DNARepositoryPort):
    def __init__(self):
        self._store: Dict[str, MusicDNA] = {}

    async def get(self, user_id: str) -> Optional[MusicDNA]:
        return self._store.get(user_id)

    async def save(self, dna: MusicDNA) -> None:
        self._store[user_id := dna.user_id] = dna
