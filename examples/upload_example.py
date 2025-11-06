from nulldrop import NullDropClient
import os
import sys


def main():
    # Replace this with your real API key
    API_KEY = "YOUR_API_KEY"
    file_path = os.path.join("extra", "text.txt")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        sys.exit(1)

    client = NullDropClient(API_KEY)

    print("Uploading file:", file_path)
    try:
        result = client.upload(file_path)
    except Exception as exc:
        print("Upload failed:", exc)
        sys.exit(1)

    print("\nUpload successful:")
    print(result)


if __name__ == "__main__":
    main()
