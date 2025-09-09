import os, json, asyncio
from typing import Dict, Any
from ..config import settings

class JsonStore:
    """
    Very simple JSON store that mirrors Mongo documents into
    data/{collection}.json as a dict: {id: document}
    """
    def __init__(self) -> None:
        self.data_dir = settings.JSON_DATA_DIR
        os.makedirs(self.data_dir, exist_ok=True)

    def _path(self, key: str) -> str:
        return os.path.join(self.data_dir, f"{key}.json")

    async def _read(self, key: str) -> Dict[str, Any]:
        path = self._path(key)
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    async def _write(self, key: str, data: Dict[str, Any]) -> None:
        path = self._path(key)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2, default=str)

    async def upsert(self, key: str, id: str, doc: Dict[str, Any]) -> None:
        data = await self._read(key)
        data[id] = doc
        await self._write(key, data)

    async def delete(self, key: str, id: str) -> None:
        data = await self._read(key)
        if id in data:
            del data[id]
            await self._write(key, data)
