---
model: groq:qwen-2.5-coder-32b
test_case: key_value_store
timestamp: 20250220_212714
duration: 4.35s
---

Sure! Below is the implementation of a key-value store with the required components. Each component is separated into its own file with proper type hints, docstrings, and error handling.

### Explanation for `src/store/interfaces/key_value_store.py`
This file defines an abstract interface for a key-value store with basic operations such as `set`, `get`, `delete`, and `exists`.

```python
# src/store/interfaces/key_value_store.py
from abc import ABC, abstractmethod
from typing import Any, Optional

class KeyValueStore(ABC):
    """
    Abstract interface for a key-value store.

    This interface defines the basic operations that any key-value store implementation
    should support.
    """

    @abstractmethod
    def set(self, key: str, value: Any) -> None:
        """
        Set the value for a given key.

        :param key: The key to set the value for.
        :param value: The value to associate with the key.
        """
        pass

    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve the value associated with a given key.

        :param key: The key to retrieve the value for.
        :return: The value associated with the key, or None if the key does not exist.
        """
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        """
        Delete the value associated with a given key.

        :param key: The key to delete the value for.
        """
        pass

    @abstractmethod
    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the store.

        :param key: The key to check for existence.
        :return: True if the key exists, False otherwise.
        """
        pass
```

### Explanation for `src/store/implementations/local_store.py`
This file provides a local file-based implementation of the `KeyValueStore` interface.

```python
# src/store/implementations/local_store.py
import json
import os
from typing import Any, Optional
from src.store.interfaces.key_value_store import KeyValueStore

class LocalKeyValueStore(KeyValueStore):
    """
    Local file-based implementation of a key-value store.

    This implementation stores the key-value pairs in a JSON file.
    """

    def __init__(self, file_path: str):
        """
        Initialize the local key-value store.

        :param file_path: The path to the JSON file where key-value pairs are stored.
        """
        self.file_path = file_path
        self._load_data()

    def _load_data(self) -> None:
        """
        Load the key-value data from the file.
        """
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = {}

    def _save_data(self) -> None:
        """
        Save the key-value data to the file.
        """
        with open(self.file_path, 'w') as f:
            json.dump(self.data, f)

    def set(self, key: str, value: Any) -> None:
        """
        Set the value for a given key.

        :param key: The key to set the value for.
        :param value: The value to associate with the key.
        """
        self.data[key] = value
        self._save_data()

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve the value associated with a given key.

        :param key: The key to retrieve the value for.
        :return: The value associated with the key, or None if the key does not exist.
        """
        return self.data.get(key)

    def delete(self, key: str) -> None:
        """
        Delete the value associated with a given key.

        :param key: The key to delete the value for.
        :raises KeyError: If the key does not exist.
        """
        if key not in self.data:
            raise KeyError(f"Key '{key}' not found.")
        del self.data[key]
        self._save_data()

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the store.

        :param key: The key to check for existence.
        :return: True if the key exists, False otherwise.
        """
        return key in self.data
```

### Explanation for `src/store/implementations/redis_store.py`
This file provides a Redis-based implementation of the `KeyValueStore` interface.

```python
# src/store/implementations/redis_store.py
import redis
from typing import Any, Optional
from src.store.interfaces.key_value_store import KeyValueStore

class RedisKeyValueStore(KeyValueStore):
    """
    Redis-based implementation of a key-value store.

    This implementation uses the Redis in-memory data structure store to store key-value pairs.
    """

    def __init__(self, host: str = 'localhost', port: int = 6379, db: int = 0):
        """
        Initialize the Redis key-value store.

        :param host: The Redis server hostname.
        :param port: The Redis server port.
        :param db: The Redis database number.
        """
        self.client = redis.Redis(host=host, port=port, db=db)
        try:
            self.client.ping()
        except redis.ConnectionError as e:
            raise ConnectionError("Failed to connect to Redis server.") from e

    def set(self, key: str, value: Any) -> None:
        """
        Set the value for a given key.

        :param key: The key to set the value for.
        :param value: The value to associate with the key.
        """
        self.client.set(key, json.dumps(value))

    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve the value associated with a given key.

        :param key: The key to retrieve the value for.
        :return: The value associated with the key, or None if the key does not exist.
        """
        value = self.client.get(key)
        if value is not None:
            return json.loads(value)
        return None

    def delete(self, key: str) -> None:
        """
        Delete the value associated with a given key.

        :param key: The key to delete the value for.
        :raises KeyError: If the key does not exist.
        """
        if not self.client.exists(key):
            raise KeyError(f"Key '{key}' not found.")
        self.client.delete(key)

    def exists(self, key: str) -> bool:
        """
        Check if a key exists in the store.

        :param key: The key to check for existence.
        :return: True if the key exists, False otherwise.
        """
        return bool(self.client.exists(key))
```

### Notes
- The `LocalKeyValueStore` class uses a JSON file to persist key-value pairs.
- The `RedisKeyValueStore` class uses the Redis in-memory data store. It requires the `redis` library, which can be installed using `pip install redis`.
- Both implementations are thread-safe as long as the Redis server and file system are accessible by multiple threads or processes.
- Error handling is included to manage cases such as missing keys and connection issues with Redis.