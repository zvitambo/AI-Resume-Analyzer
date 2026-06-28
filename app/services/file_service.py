"""
Purpose: Handles uploaded files before they are parsed.

Responsibilities:
- Detect file type from extension
- Validate allowed extensions
- Read file bytes safely
- Save temporary files if needed
- Route files to appropriate parser

Why it exists:
File-handling concerns should be separate from resume parsing logic.

Usage in this project:
If a user uploads:
- .pdf → route to PDF parser
- .docx → route to DOCX parser

This service decides routing and validates files.
"""

import os
import mimetypes
import tempfile
from enum import Enum
from pathlib import Path
from typing import Optional, Tuple, BinaryIO
from io import BytesIO

from app.core.exceptions import ValidationException
from app.core.logging import logger


class FileType(str, Enum):
    """Supported file types for resume and job description parsing"""
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"


class FileService:
    """Service for handling uploaded file operations"""
    
    # Allowed file extensions (without dot)
    ALLOWED_EXTENSIONS = {FileType.PDF.value, FileType.DOCX.value, FileType.TXT.value}
    
    # MIME type mappings
    MIME_TYPE_MAP = {
        "application/pdf": FileType.PDF.value,
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": FileType.DOCX.value,
        "text/plain": FileType.TXT.value,
    }
    
    # Max file size in bytes (25 MB)
    MAX_FILE_SIZE = 25 * 1024 * 1024
    
    @staticmethod
    def get_file_extension(filename: str) -> str:
        """
        Extract file extension from filename.
        
        Args:
            filename: Name of the file
            
        Returns:
            File extension without the dot, lowercase
        """
        if not filename:
            return ""
        return Path(filename).suffix.lstrip(".").lower()
    
    @staticmethod
    def detect_file_type(filename: str) -> Optional[FileType]:
        """
        Detect file type from filename extension.
        
        Args:
            filename: Name of the file
            
        Returns:
            FileType enum or None if not recognized
        """
        extension = FileService.get_file_extension(filename)
        
        try:
            return FileType(extension)
        except ValueError:
            return None
    
    @staticmethod
    def is_extension_allowed(filename: str) -> bool:
        """
        Check if file extension is allowed.
        
        Args:
            filename: Name of the file
            
        Returns:
            True if extension is allowed, False otherwise
        """
        extension = FileService.get_file_extension(filename)
        return extension in FileService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def validate_file(
        filename: str,
        file_size: int,
        content: Optional[bytes] = None
    ) -> Tuple[bool, str]:
        """
        Validate file based on extension and size.
        
        Args:
            filename: Name of the file
            file_size: Size of the file in bytes
            content: Optional file content for additional validation
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not filename:
            return False, "Filename is required"
        
        # Check extension
        if not FileService.is_extension_allowed(filename):
            extension = FileService.get_file_extension(filename)
            allowed = ", ".join(FileService.ALLOWED_EXTENSIONS)
            return False, f"File type '.{extension}' not allowed. Allowed types: {allowed}"
        
        # Check file size
        if file_size > FileService.MAX_FILE_SIZE:
            max_mb = FileService.MAX_FILE_SIZE / (1024 * 1024)
            actual_mb = file_size / (1024 * 1024)
            return False, f"File size ({actual_mb:.1f} MB) exceeds maximum ({max_mb:.0f} MB)"
        
        # Check if file is empty
        if file_size == 0:
            return False, "File is empty"
        
        return True, ""
    
    @staticmethod
    def read_file_bytes(file_path: str) -> bytes:
        """
        Read file bytes safely from disk.
        
        Args:
            file_path: Path to the file
            
        Returns:
            File contents as bytes
            
        Raises:
            ValidationException: If file cannot be read
        """
        try:
            with open(file_path, "rb") as f:
                content = f.read()
            logger.info(f"Successfully read file: {file_path} ({len(content)} bytes)")
            return content
        except FileNotFoundError:
            error_msg = f"File not found: {file_path}"
            logger.error(error_msg)
            raise ValidationException(error_msg)
        except IOError as e:
            error_msg = f"Error reading file {file_path}: {str(e)}"
            logger.error(error_msg)
            raise ValidationException(error_msg)
    
    @staticmethod
    def read_file_bytes_from_stream(file_stream: BinaryIO) -> bytes:
        """
        Read file bytes from a file stream (e.g., uploaded file).
        
        Args:
            file_stream: Binary file stream
            
        Returns:
            File contents as bytes
            
        Raises:
            ValidationException: If file cannot be read
        """
        try:
            content = file_stream.read()
            logger.info(f"Successfully read file from stream ({len(content)} bytes)")
            return content
        except Exception as e:
            error_msg = f"Error reading file from stream: {str(e)}"
            logger.error(error_msg)
            raise ValidationException(error_msg)
    
    @staticmethod
    def save_temporary_file(
        content: bytes,
        filename: str,
        temp_dir: Optional[str] = None
    ) -> str:
        """
        Save uploaded file to a temporary location.
        
        Args:
            content: Binary file content
            filename: Original filename (used to preserve extension)
            temp_dir: Optional temporary directory path
            
        Returns:
            Path to the saved temporary file
            
        Raises:
            ValidationException: If file cannot be saved
        """
        try:
            # Determine temporary directory
            if temp_dir is None:
                temp_dir = tempfile.gettempdir()
            
            # Create temp directory if needed
            Path(temp_dir).mkdir(parents=True, exist_ok=True)
            
            # Get file extension
            extension = FileService.get_file_extension(filename)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(
                dir=temp_dir,
                suffix=f".{extension}",
                delete=False
            ) as tmp_file:
                tmp_file.write(content)
                temp_path = tmp_file.name
            
            logger.info(f"Saved temporary file: {temp_path}")
            return temp_path
            
        except Exception as e:
            error_msg = f"Error saving temporary file: {str(e)}"
            logger.error(error_msg)
            raise ValidationException(error_msg)
    
    @staticmethod
    def cleanup_temporary_file(file_path: str) -> bool:
        """
        Delete a temporary file.
        
        Args:
            file_path: Path to the temporary file
            
        Returns:
            True if deleted successfully, False otherwise
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Deleted temporary file: {file_path}")
                return True
            else:
                logger.warning(f"Temporary file not found: {file_path}")
                return False
        except Exception as e:
            logger.error(f"Error deleting temporary file {file_path}: {str(e)}")
            return False
    
    @staticmethod
    def process_uploaded_file(
        filename: str,
        content: bytes,
        temp_dir: Optional[str] = None
    ) -> Tuple[FileType, str]:
        """
        Process an uploaded file: validate, save, and return routing information.
        
        This is the main orchestrator method for file handling.
        
        Args:
            filename: Name of the uploaded file
            content: Binary file content
            temp_dir: Optional temporary directory for saving files
            
        Returns:
            Tuple of (FileType, temporary_file_path)
            
        Raises:
            ValidationException: If validation fails
        """
        file_size = len(content)
        
        # Validate file
        is_valid, error_message = FileService.validate_file(
            filename,
            file_size,
            content
        )
        
        if not is_valid:
            logger.warning(f"File validation failed: {error_message}")
            raise ValidationException(error_message)
        
        # Detect file type
        file_type = FileService.detect_file_type(filename)
        if file_type is None:
            error_msg = f"Could not detect file type for: {filename}"
            logger.error(error_msg)
            raise ValidationException(error_msg)
        
        # Save temporary file
        temp_file_path = FileService.save_temporary_file(content, filename, temp_dir)
        
        logger.info(f"File processed successfully: {filename} -> {file_type.value}")
        
        return file_type, temp_file_path


# For backwards compatibility, create module-level functions
def validate_file_extension(filename: str) -> bool:
    """Validate that file extension is allowed"""
    return FileService.is_extension_allowed(filename)


def get_file_type(filename: str) -> Optional[str]:
    """Get file type from filename"""
    file_type = FileService.detect_file_type(filename)
    return file_type.value if file_type else None


def read_uploaded_file(file_stream: BinaryIO) -> bytes:
    """Read bytes from uploaded file stream"""
    return FileService.read_file_bytes_from_stream(file_stream)


def save_file_temp(content: bytes, filename: str) -> str:
    """Save file to temp location"""
    return FileService.save_temporary_file(content, filename)


def cleanup_file(file_path: str) -> bool:
    """Clean up temporary file"""
    return FileService.cleanup_temporary_file(file_path)