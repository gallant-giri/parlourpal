import os
import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url
from io import BytesIO
from PIL import Image

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

def upload_image_to_cloudinary(image_bytes, folder="posters", public_id=None):
    """
    Upload image bytes to Cloudinary and return the URL
    
    Args:
        image_bytes: Raw image bytes
        folder: Cloudinary folder name
        public_id: Optional custom public ID
    
    Returns:
        dict: Cloudinary response with URL and other details
    """
    try:
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(
            image_bytes,
            folder=folder,
            public_id=public_id,
            resource_type="image",
            overwrite=True
        )
        
        return {
            'success': True,
            'url': response['secure_url'],
            'public_id': response['public_id'],
            'width': response.get('width'),
            'height': response.get('height'),
            'format': response.get('format')
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def upload_file_to_cloudinary(file, folder="logos", public_id=None):
    """
    Upload a file object to Cloudinary
    
    Args:
        file: Django file object
        folder: Cloudinary folder name
        public_id: Optional custom public ID
    
    Returns:
        dict: Cloudinary response with URL and other details
    """
    try:
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(
            file,
            folder=folder,
            public_id=public_id,
            resource_type="image",
            overwrite=True
        )
        
        return {
            'success': True,
            'url': response['secure_url'],
            'public_id': response['public_id'],
            'width': response.get('width'),
            'height': response.get('height'),
            'format': response.get('format')
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def delete_from_cloudinary(public_id):
    """
    Delete an image from Cloudinary
    
    Args:
        public_id: Cloudinary public ID
    
    Returns:
        dict: Success status and response
    """
    try:
        response = cloudinary.uploader.destroy(public_id)
        return {
            'success': True,
            'response': response
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_cloudinary_url(public_id, transformation=None):
    """
    Get Cloudinary URL with optional transformations
    
    Args:
        public_id: Cloudinary public ID
        transformation: Optional transformation parameters
    
    Returns:
        str: Cloudinary URL
    """
    try:
        url, options = cloudinary_url(public_id, transformation=transformation)
        return url
    except Exception as e:
        return None

def optimize_image_for_cloudinary(image_bytes, max_size=(800, 800), quality=85):
    """
    Optimize image before uploading to Cloudinary
    
    Args:
        image_bytes: Raw image bytes
        max_size: Maximum dimensions (width, height)
        quality: JPEG quality (1-100)
    
    Returns:
        bytes: Optimized image bytes
    """
    try:
        # Open image from bytes
        image = Image.open(BytesIO(image_bytes))
        
        # Convert to RGB if necessary
        if image.mode in ('RGBA', 'LA', 'P'):
            image = image.convert('RGB')
        
        # Resize if larger than max_size
        if image.size[0] > max_size[0] or image.size[1] > max_size[1]:
            image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized image to bytes
        output = BytesIO()
        image.save(output, format='JPEG', quality=quality, optimize=True)
        output.seek(0)
        
        return output.getvalue()
    except Exception as e:
        # Return original bytes if optimization fails
        return image_bytes 