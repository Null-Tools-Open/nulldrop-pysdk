import requests
from typing import List, Optional, Dict, Any
from .exceptions import AuthenticationError, APIError, NotFoundError


class NullDropClient:
    def __init__(self, api_key: str, base_url: str = "https://nulldrop.xyz/api/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.api_key}"
        }

    def _handle_response(self, resp: requests.Response) -> Any:
        if resp.status_code == 401:
            raise AuthenticationError("Invalid API key.")
        if resp.status_code == 404:
            raise NotFoundError("File not found.")
        if resp.status_code >= 400:
            raise APIError(f"Error {resp.status_code}: {resp.text}")
        return resp.json()

    def upload(self, file_path: str) -> Dict[str, Any]:
        url = f"{self.base_url}/upload"
        with open(file_path, "rb") as f:
            files = {"file": f}
            resp = requests.post(url, headers=self._headers(), files=files)
        return self._handle_response(resp)

    def list_files(self) -> List[Dict[str, Any]]:
        url = f"{self.base_url}/files"
        resp = requests.get(url, headers=self._headers())
        return self._handle_response(resp)

    def get_file(self, file_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/files/{file_id}"
        resp = requests.get(url, headers=self._headers())
        return self._handle_response(resp)

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        url = f"{self.base_url}/files/{file_id}"
        resp = requests.delete(url, headers=self._headers())
        return self._handle_response(resp)
