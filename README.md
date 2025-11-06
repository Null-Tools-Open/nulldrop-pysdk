Here's the complete `README.md` file for you to copy and paste:

# NullDrop Client SDK

A Python client SDK for interacting with [NullDrop API](https://nulldrop.xyz), a secure file storage and sharing service. This SDK allows you to easily upload, list, retrieve, and delete files in the NullDrop cloud.

## Features

- **Upload files**: Upload files to NullDrop with optional public sharing.
- **List files**: Retrieve a list of files uploaded to NullDrop.
- **Get file details**: Fetch detailed information about a specific file.
- **Delete files**: Delete files from NullDrop.

## Installation

You can install the `nulldrop` SDK from PyPI using `pip`:

```bash
pip install nulldrop
````

## Setup

You will need a **NullDrop API token** to use the SDK. You can obtain this from your NullDrop account settings.

Once you have your API token, you can start using the SDK by initializing the `NullDropClient` with your API key.

### Example:

```python
from nulldrop import NullDropClient

# Initialize the client with your API key
api_key = 'your-api-key'
client = NullDropClient(api_key)
```

## Usage

### Upload a File

To upload a file to NullDrop, use the `upload` method. The file can optionally be marked as public.

```python
file_path = 'path_to_your_file.txt'
uploaded_file = client.upload(file_path)

print("File uploaded:")
print(uploaded_file)
```

### List Files

To retrieve a list of all files uploaded to your NullDrop account, use the `list_files` method:

```python
files = client.list_files()

for file in files:
    print(file)
```

### Get File Details

To retrieve details about a specific file, use the `get_file` method:

```python
file_id = 'your-file-id'
file = client.get_file(file_id)

print(f"File details: {file}")
```

### Delete a File

To delete a file from NullDrop, use the `delete_file` method:

```python
file_id = 'your-file-id-to-delete'
response = client.delete_file(file_id)

print(response)
```

## Error Handling

The SDK raises exceptions in case of errors, including:

* `NullDropError`: General error when interacting with the NullDrop API.
* `AuthenticationError`: Raised if the provided API key is invalid or missing.

Example:

```python
from nulldrop.exceptions import NullDropError, AuthenticationError

try:
    # Code that might raise an error
    files = client.list_files()
except AuthenticationError:
    print("Invalid API key!")
except NullDropError as e:
    print(f"An error occurred: {e}")
```

## License

This package is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## Additional Information

For more details about the NullDrop API, refer to the official [API Documentation](https://docs.nulldrop.xyz/).

