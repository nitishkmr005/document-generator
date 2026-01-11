"""Tests for upload route."""

import pytest
from fastapi.testclient import TestClient
from io import BytesIO

from doc_generator.infrastructure.api.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


class TestUploadRoute:
    """Test file upload endpoint."""

    def test_upload_pdf(self, client):
        content = b"%PDF-1.4 fake pdf content"
        files = {"file": ("report.pdf", BytesIO(content), "application/pdf")}
        response = client.post("/api/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["file_id"].startswith("f_")
        assert data["filename"] == "report.pdf"
        assert data["mime_type"] == "application/pdf"
        assert data["size"] == len(content)

    def test_upload_text(self, client):
        content = b"Plain text content"
        files = {"file": ("notes.txt", BytesIO(content), "text/plain")}
        response = client.post("/api/upload", files=files)
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "notes.txt"

    def test_upload_no_file(self, client):
        response = client.post("/api/upload")
        assert response.status_code == 422  # Validation error
