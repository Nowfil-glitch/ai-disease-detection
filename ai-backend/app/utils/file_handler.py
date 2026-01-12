import os
import uuid
import aiofiles
from fastapi import UploadFile, HTTPException
from typing import Tuple
import logging
from app.config import settings

logger = logging.getLogger(__name__)


class FileHandler:
    """Handle file uploads and storage"""
    
    @staticmethod
    def validate_file_extension(filename: str) -> bool:
        """Check if file extension is allowed"""
        if not filename:
            return False
        
        extension = filename.rsplit('.', 1)[-1].lower()
        return extension in settings.ALLOWED_EXTENSIONS
    
    @staticmethod
    def generate_unique_filename(original_filename: str) -> str:
        """Generate unique filename preserving extension"""
        extension = original_filename.rsplit('.', 1)[-1].lower()
        unique_id = uuid.uuid4().hex
        return f"{unique_id}.{extension}"
    
    @staticmethod
    async def save_upload_file(upload_file: UploadFile) -> Tuple[str, str]:
        """
        Save uploaded file to disk
        
        Args:
            upload_file: FastAPI UploadFile object
            
        Returns:
            Tuple of (file_path, filename)
        """
        try:
            # Validate extension
            if not FileHandler.validate_file_extension(upload_file.filename):
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
                )
            
            # Generate unique filename
            filename = FileHandler.generate_unique_filename(upload_file.filename)
            file_path = os.path.join(settings.UPLOAD_DIR, filename)
            
            # Check file size
            content = await upload_file.read()
            if len(content) > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=400,
                    detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
                )
            
            # Save file
            async with aiofiles.open(file_path, 'wb') as f:
                await f.write(content)
            
            logger.info(f"File saved: {file_path}")
            return file_path, filename
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error saving file: {str(e)}")
            raise HTTPException(status_code=500, detail="Error saving file")
    
    @staticmethod
    def cleanup_file(file_path: str) -> bool:
        """Delete file from disk"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting file: {str(e)}")
            return False
    
    @staticmethod
    def get_file_size(file_path: str) -> int:
        """Get file size in bytes"""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0


file_handler = FileHandler()
