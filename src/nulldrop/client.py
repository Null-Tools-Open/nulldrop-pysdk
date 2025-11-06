import requests
from .exceptions import NullDropError, AuthenticationError


def format_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024**2:
        return f"{size_bytes / 1024:.2f} KB"
    elif size_bytes < 1024**3:
        return f"{size_bytes / 1024**2:.2f} MB"
    return f"{size_bytes / 1024**3:.2f} GB"


class NDFile(dict):
    def __str__(self):
        size = format_size(self.get("size", 0))
        return (
            f"📄 {self.get('name', 'Unnamed')} "
            f"({size}) - {self.get('url')}"
        )

    __repr__ = __str__


class NullDropClient:

    def __init__(self, api_key: str, base_url: str = "https://nulldrop.xyz/api/v1"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}"
        })

    def _request(self, method: str, path: str, **kwargs):
        """ Helper method to send a request to the API. """
        url = f"{self.base_url}{path}"
        res = self.session.request(method, url, **kwargs)

        if res.status_code == 401:
            raise AuthenticationError("Invalid or missing API key.")

        if not res.ok:
            raise NullDropError(
                f"API error: {res.status_code} - {res.text}"
            )

        if res.text.strip() == "":
            return {}

        try:
            return res.json()
        except Exception:
            raise NullDropError("Server did not return valid JSON.")

    # --------------------
    # File Operations
    # --------------------

    def upload(self, file_path: str, public: bool = True) -> NDFile:
        """ Upload a file to the NullDrop API. """
        payload = {"isPublic": "true" if public else "false"}

        with open(file_path, "rb") as f:
            res = self._request(
                "POST",
                "/upload",
                data=payload,
                files={"file": f},
            )

        data = res.get("data", {})
        file = data

        return NDFile({
            "id": file.get("id"),
            "name": file.get("filename"),
            "size": file.get("size", 0),
            "type": file.get("mimeType", "unknown"),
            "url": file.get("downloadUrl"),
            "share_url": file.get("shareUrl"),
            "uploaded_at": file.get("uploadedAt"),
        })

    def list_files(self):
        """ List all uploaded files. """
        res = self._request("GET", "/files")
        data = res.get("data", {})
        files = data.get("files", [])
        return [NDFile({
            "id": f.get("id"),
            "name": f.get("filename"),
            "size": f.get("size", 0),
            "type": f.get("mimeType", "unknown"),
            "url": f.get("downloadUrl"),
            "share_url": f.get("shareUrl"),
            "uploaded_at": f.get("uploadedAt"),
        }) for f in files]

    def get_file(self, file_id: str) -> NDFile:
        """ Get a specific file's details by its ID. """
        res = self._request("GET", f"/files/{file_id}")
        data = res.get("data", {})
        file = data.get("file")
        if not file:
            raise NullDropError(f"File not found: {file_id}")
        return NDFile({
            "id": file.get("id"),
            "name": file.get("filename"),
            "size": file.get("size", 0),
            "type": file.get("mimeType", "unknown"),
            "url": file.get("downloadUrl"),
            "share_url": file.get("shareUrl"),
            "uploaded_at": file.get("uploadedAt"),
        })

    def delete_file(self, file_id: str) -> bool:
        """ Delete a file by its ID using the API v1. """
        res = self._request("DELETE", f"/files/{file_id}")

        data = res.get("data", {})
        success = res.get("success", False)

        if not success:
            raise NullDropError(f"Failed to delete file: {file_id}")

        # API v1 returns {"success": true, "data": "..."}
        return True
