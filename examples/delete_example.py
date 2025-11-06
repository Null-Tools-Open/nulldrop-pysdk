from nulldrop import NullDropClient

API_KEY = "YOUR_API_KEY"
FILE_ID = "YOUR_FILE_ID"

client = NullDropClient(API_KEY)

success = client.delete_file(FILE_ID)
print(f"File {FILE_ID} deleted successfully: {success}")
