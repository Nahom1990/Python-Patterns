"""You're working on a web application that stores user-uploaded files.

Your application wants a simple storage interface:

save(filename, content) → file_id
load(file_id) → content
delete(file_id) → bool

Your existing application code should be able to work with any storage backend through that interface.

The problem

Your company currently uses an old storage library called LegacyFileStore.

You cannot modify it.

Its API looks like this:

class LegacyFileStore:

    def put_file(self, path, data):
        # stores the file
        # returns something like:
        # "uploads/abc123/profile.jpg"
        ...

    def read_file(self, path):
        # returns the file contents
        ...

    def remove_file(self, path):
        # returns:
        # "REMOVED" or "NOT_FOUND"
        ...

There are several incompatibilities between what your application wants and what the legacy library provides.

Application wants
save(filename, content)
load(file_id)
delete(file_id)
Legacy library provides
put_file(path, data)
read_file(path)
remove_file(path)

There is also an important difference:

The application thinks in terms of a file ID:

"abc123"

while the legacy system thinks in terms of a path:

"uploads/abc123/profile.jpg"

The Adapter must handle this translation.

Requirements

Build the system yourself.

1. Target

Your application should depend on an abstraction representing:

save(filename, content) → file_id
load(file_id) → content
delete(file_id) → bool
2. Adaptee

Implement the given LegacyFileStore.

You may simplify its internal behavior using a dictionary.

For example, internally it might store:

uploads/abc123/profile.jpg → "image data"
3. Adapter

Create an Adapter that makes LegacyFileStore compatible with your application's storage interface.

The Adapter should:

translate save() into put_file()
translate load() into read_file()
translate delete() into remove_file()
translate "REMOVED" into True
translate "NOT_FOUND" into False
handle the conversion between file IDs and legacy paths
4. Client

Create something like:

class UserUploadService:
    ...

The client should depend only on your application's storage interface.

It should not know that LegacyFileStore exists.

For example, conceptually:

service.upload(...)
service.download(...)
service.remove(...)
"""

from typing import Protocol, Dict, Optional
import uuid

# =====================================================================
# 1. Target (Application Abstraction Interface)
# =====================================================================
class FileStorage(Protocol):
    """Target interface expected by the application."""
    def save(self, filename: str, content: str) -> str:
        """Stores file and returns file_id."""
        ...

    def load(self, file_id: str) -> str:
        """Loads and returns content by file_id."""
        ...

    def delete(self, file_id: str) -> bool:
        """Deletes file by file_id, returning True if successful."""
        ...


# =====================================================================
# 2. Adaptee (The Legacy Storage Library - Cannot be modified)
# =====================================================================
class LegacyFileStore:
    """Old third-party or legacy library."""
    def __init__(self) -> None:
        self._storage: Dict[str, str] = {}

    def put_file(self, path: str, data: str) -> str:
        # Legacy store requires full path and stores raw data
        self._storage[path] = data
        return path

    def read_file(self, path: str) -> Optional[str]:
        return self._storage.get(path)

    def remove_file(self, path: str) -> str:
        if path in self._storage:
            del self._storage[path]
            return "REMOVED"
        return "NOT_FOUND"


# =====================================================================
# 3. Adapter (Translates between Target Interface and Adaptee)
# =====================================================================
class LegacyFileStoreAdapter:
    """
    Adapter that wraps LegacyFileStore and translates method signatures
    and ID-to-Path formats to conform to the FileStorage Protocol.
    """
    def __init__(self, legacy_store: LegacyFileStore) -> None:
        self._legacy_store = legacy_store
        # Maps application file_id -> legacy system path
        # (e.g., "abc123" -> "uploads/abc123/profile.jpg")
        self._id_to_path_map: Dict[str, str] = {}

    def save(self, filename: str, content: str) -> str:
        # 1. Generate unique file_id expected by modern application
        file_id = uuid.uuid4().hex[:8]

        # 2. Construct path required by legacy store
        path = f"uploads/{file_id}/{filename}"

        # 3. Save to legacy system & track mapping
        self._legacy_store.put_file(path, content)
        self._id_to_path_map[file_id] = path

        return file_id

    def load(self, file_id: str) -> str:
        path = self._id_to_path_map.get(file_id)
        if not path:
            raise FileNotFoundError(f"File ID '{file_id}' not found.")

        content = self._legacy_store.read_file(path)
        if content is None:
            raise FileNotFoundError(f"File content at path '{path}' missing.")

        return content

    def delete(self, file_id: str) -> bool:
        path = self._id_to_path_map.get(file_id)
        if not path:
            return False

        # Translate legacy string responses into boolean status
        status = self._legacy_store.remove_file(path)
        if status == "REMOVED":
            del self._id_to_path_map[file_id]
            return True

        return False


# =====================================================================
# 4. Client (Application Service)
# =====================================================================
class UserUploadService:
    """Client that relies ONLY on the FileStorage protocol interface."""
    def __init__(self, storage: FileStorage) -> None:
        self.storage = storage

    def upload_user_avatar(self, username: str, image_data: str) -> str:
        filename = f"{username}_avatar.png"
        file_id = self.storage.save(filename, image_data)
        print(f"[Client] Uploaded {filename} with file_id: {file_id}")
        return file_id

    def download_user_avatar(self, file_id: str) -> str:
        data = self.storage.load(file_id)
        print(f"[Client] Downloaded file_id '{file_id}': {data}")
        return data

    def remove_user_avatar(self, file_id: str) -> bool:
        success = self.storage.delete(file_id)
        print(f"[Client] Deleted file_id '{file_id}': {success}")
        return success


# =====================================================================
# Execution & Verification
# =====================================================================
if __name__ == "__main__":
    # 1. Instantiate legacy third-party system
    legacy_store = LegacyFileStore()

    # 2. Wrap it with our adapter
    adapter = LegacyFileStoreAdapter(legacy_store)

    # 3. Inject adapter into client (Client has no idea LegacyFileStore exists!)
    service = UserUploadService(storage=adapter)

    # --- Test Workflow ---
    print("--- 1. Uploading File ---")
    file_id = service.upload_user_avatar("nahom", "binary_image_bytes_here")

    print("\n--- 2. Reading File ---")
    content = service.download_user_avatar(file_id)
    assert content == "binary_image_bytes_here"

    print("\n--- 3. Checking Legacy State (Under the Hood) ---")
    legacy_path = adapter._id_to_path_map[file_id]
    print(f"Internal Legacy Path stored: {legacy_path}")
    print(f"Legacy Raw Read: {legacy_store.read_file(legacy_path)}")

    print("\n--- 4. Deleting File ---")
    deleted = service.remove_user_avatar(file_id)
    assert deleted is True

    print("\n--- 5. Verify Deletion ---")
    assert legacy_store.read_file(legacy_path) is None
    deleted_again = service.remove_user_avatar(file_id)
    assert deleted_again is False