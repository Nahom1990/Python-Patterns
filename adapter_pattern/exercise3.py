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

