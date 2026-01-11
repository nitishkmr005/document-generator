"""Storage service for uploads and outputs."""

import secrets
import time
from pathlib import Path


class StorageService:
    """Manages temporary uploads and generated outputs."""

    def __init__(
        self,
        upload_dir: Path = Path("src/output/uploads"),
        output_dir: Path = Path("src/output/generated"),
        base_url: str = "/api/download",
    ):
        """Initialize storage service.

        Args:
            upload_dir: Directory for temporary uploads
            output_dir: Directory for generated outputs
            base_url: Base URL for download links
        """
        self.upload_dir = Path(upload_dir)
        self.output_dir = Path(output_dir)
        self.base_url = base_url

        # Ensure directories exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Track upload metadata
        self._uploads: dict[str, dict] = {}

    def save_upload(
        self,
        content: bytes,
        filename: str,
        mime_type: str,
    ) -> str:
        """Save uploaded file and return file_id.

        Args:
            content: File content bytes
            filename: Original filename
            mime_type: MIME type of file

        Returns:
            Unique file ID (f_...)
        """
        file_id = f"f_{secrets.token_hex(12)}"
        ext = Path(filename).suffix
        storage_path = self.upload_dir / f"{file_id}{ext}"

        storage_path.write_bytes(content)

        self._uploads[file_id] = {
            "filename": filename,
            "mime_type": mime_type,
            "path": storage_path,
            "created_at": time.time(),
        }

        return file_id

    def get_upload_path(self, file_id: str) -> Path:
        """Get path to uploaded file.

        Args:
            file_id: File ID from save_upload

        Returns:
            Path to the file

        Raises:
            FileNotFoundError: If file_id not found
        """
        if file_id not in self._uploads:
            raise FileNotFoundError(f"Upload not found: {file_id}")
        return self._uploads[file_id]["path"]

    def get_upload_content(self, file_id: str) -> bytes:
        """Get content of uploaded file.

        Args:
            file_id: File ID from save_upload

        Returns:
            File content bytes

        Raises:
            FileNotFoundError: If file_id not found
        """
        path = self.get_upload_path(file_id)
        return path.read_bytes()

    def get_upload_metadata(self, file_id: str) -> dict:
        """Get metadata for uploaded file.

        Args:
            file_id: File ID from save_upload

        Returns:
            Metadata dict with filename, mime_type, path, created_at

        Raises:
            FileNotFoundError: If file_id not found
        """
        if file_id not in self._uploads:
            raise FileNotFoundError(f"Upload not found: {file_id}")
        return self._uploads[file_id].copy()

    def save_output(
        self,
        content: bytes,
        filename: str,
    ) -> Path:
        """Save generated output file.

        Args:
            content: Generated file content
            filename: Output filename

        Returns:
            Path to saved file
        """
        # Add timestamp to ensure uniqueness
        timestamp = int(time.time())
        stem = Path(filename).stem
        ext = Path(filename).suffix
        unique_filename = f"{stem}_{timestamp}{ext}"

        output_path = self.output_dir / unique_filename
        output_path.write_bytes(content)

        return output_path

    def get_download_url(self, output_path: Path) -> str:
        """Generate download URL for output file.

        Args:
            output_path: Path to the output file

        Returns:
            Download URL with token
        """
        # Generate a simple token (in production, use signed URLs)
        token = secrets.token_urlsafe(16)
        filename = output_path.name
        return f"{self.base_url}/{filename}?token={token}"

    def cleanup_upload(self, file_id: str) -> None:
        """Remove uploaded file.

        Args:
            file_id: File ID to remove
        """
        if file_id in self._uploads:
            path = self._uploads[file_id]["path"]
            if path.exists():
                path.unlink()
            del self._uploads[file_id]

    def cleanup_expired_uploads(self, max_age_seconds: int = 3600) -> int:
        """Remove uploads older than max_age.

        Args:
            max_age_seconds: Maximum age in seconds (default 1 hour)

        Returns:
            Number of files cleaned up
        """
        now = time.time()
        expired = []

        for file_id, metadata in self._uploads.items():
            if now - metadata["created_at"] > max_age_seconds:
                expired.append(file_id)

        for file_id in expired:
            self.cleanup_upload(file_id)

        return len(expired)
