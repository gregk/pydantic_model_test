---
model: anthropic:claude-3-5-sonnet-latest
test_case: key_value_store
timestamp: 20250220_212714
duration: 10.86s
---

I'll create a key-value store implementation with the requested specifications. Here's the implementation split into three files:

First, let's look at the abstract interface that defines the basic operations for our key-value store:

`src/store/interfaces/key_value_store.py`:
```python
from abc import ABC, abstractmethod
from typing import Any, Optional, List


class KeyValueStore(ABC):
    """Abstract interface for key-value store implementations."""

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """Store a value with the given key.

        Args:
            key: The key to store the value under
            value: The value to store

        Raises:
            ValueError: If the key is empty or invalid
        """
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Retrieve a value for the given key.

        Args:
            key: The key to look up

        Returns:
            The value associated with the key, or None if not found

        Raises:
            ValueError: If the key is empty or invalid
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a key-value pair.

        Args:
            key: The key to delete

        Returns:
            True if the key was deleted, False if it didn't exist

        Raises:
            ValueError: If the key is empty or invalid
        """
        pass

    @abstractmethod
    def list_keys(self) -> List[str]:
        """List all available keys in the store.

        Returns:
            A list of all keys in the store
        """
        pass

    @abstractmethod
    def clear(self) -> None:
        """Remove all key-value pairs from the store."""
        pass
```

Next, here's the local file-based implementation that stores data in a JSON file:

`src/store/implementations/local_store.py`:
```python
import json
import os
from typing import Any, Optional, List
from ..interfaces.key_value_store import KeyValueStore


class LocalStore(KeyValueStore):
    """A file-based implementation of the key-value store."""

    def __init__(self, file_path: str):
        """Initialize the local store with a file path.

        Args:
            file_path: Path to the JSON file that will store the data
        """
        self.file_path = file_path
        self._ensure_store_exists()

    def _ensure_store_exists(self) -> None:
        """Create the store file if it doesn't exist."""
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump({}, f)

    def _read_store(self) -> dict:
        """Read the current state of the store.

        Returns:
            The store contents as a dictionary
        """
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    def _write_store(self, data: dict) -> None:
        """Write data to the store.

        Args:
            data: The dictionary to write to the store
        """
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

    def set(self, key: str, value: Any) -> None:
        if not key or not isinstance(key, str):
            raise ValueError("Key must be a non-empty string")
        
        store = self._read_store()
        store[key] = value
        self._write_store(store)

    def get(self, key: str) -> Optional[Any]:
        if not key or not isinstance(key, str):
            raise ValueError("Key must be a non-empty string")
        
        store = self._read_store()
        return store.get(key)

    def delete(self, key: str) -> bool:
        if not key or not isinstance(key, str):
            raise ValueError("Key must be a non-empty string")
        
        store = self._read_store()
        if key in store:
            del store[key]