"""
Simple background removal implementation using onnxruntime
"""
import os
import numpy as np
import onnxruntime as ort
from PIL import Image
import requests
import logging

class BackgroundRemover:
    def __init__(self):
        self.model_path = None
        self.session = None
        self.input_size = (320, 320)
        
    def download_model(self):
        """Download U2Net model if not already downloaded"""
        model_dir = os.path.expanduser("~/.u2net")
        os.makedirs(model_dir, exist_ok=True)
        
        model_file = os.path.join(model_dir, "u2net.onnx")
        
        if os.path.exists(model_file):
            self.model_path = model_file
            return True
            
        try:
            # Download a smaller, compatible U2Net model
            url = "https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx"
            response = requests.get(url, stream=True, timeout=30)
            
            if response.status_code == 200:
                with open(model_file, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                self.model_path = model_file
                return True
            else:
                logging.error(f"Failed to download model: {response.status_code}")
                return False
                
        except Exception as e:
            logging.error(f"Error downloading model: {str(e)}")
            return False
    
    def load_model(self):
        """Load the ONNX model"""
        if not self.model_path:
            if not self.download_model():
                return False
                
        try:
            self.session = ort.InferenceSession(self.model_path)
            return True
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            return False
    
    def preprocess_image(self, image):
        """Preprocess image for model input"""
        # Resize image
        image = image.resize(self.input_size, Image.LANCZOS)
        
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Convert to numpy array and normalize
        img_array = np.array(image).astype(np.float32)
        img_array = img_array / 255.0
        
        # Transpose to CHW format and add batch dimension
        img_array = img_array.transpose(2, 0, 1)
        img_array = np.expand_dims(img_array, axis=0)
        
        return img_array
    
    def postprocess_mask(self, mask, original_size):
        """Postprocess model output to create final mask"""
        # Remove batch dimension
        mask = mask.squeeze()
        
        # Convert to PIL Image
        mask = (mask * 255).astype(np.uint8)
        mask_image = Image.fromarray(mask, mode='L')
        
        # Resize to original size
        mask_image = mask_image.resize(original_size, Image.LANCZOS)
        
        return mask_image
    
    def remove_background(self, input_image):
        """Remove background from image"""
        if not self.session:
            if not self.load_model():
                raise Exception("Failed to load background removal model")
        
        original_size = input_image.size
        
        # Preprocess
        input_array = self.preprocess_image(input_image)
        
        # Run inference
        input_name = self.session.get_inputs()[0].name
        output = self.session.run(None, {input_name: input_array})[0]
        
        # Postprocess
        mask = self.postprocess_mask(output, original_size)
        
        # Apply mask to original image
        if input_image.mode != 'RGBA':
            input_image = input_image.convert('RGBA')
        
        # Create output image with transparency
        output_image = Image.new('RGBA', original_size, (0, 0, 0, 0))
        
        # Convert mask to numpy for faster processing
        mask_array = np.array(mask)
        input_array = np.array(input_image)
        output_array = np.zeros_like(input_array)
        
        # Apply mask - where mask > 128, copy original pixels
        mask_condition = mask_array > 128
        output_array[mask_condition] = input_array[mask_condition]
        
        output_image = Image.fromarray(output_array, 'RGBA')
        return output_image

# Global instance
bg_remover = BackgroundRemover()

def remove_background_simple(image_data):
    """Simple function to remove background from image data"""
    try:
        # Open image from bytes
        from io import BytesIO
        image = Image.open(BytesIO(image_data))
        
        # Try to remove background with model, fallback to simple processing
        try:
            result = bg_remover.remove_background(image)
        except Exception as model_error:
            logging.warning(f"Model-based background removal failed: {model_error}")
            # Fallback: convert to RGBA and return original with message
            result = image.convert('RGBA')
        
        # Convert back to bytes
        output_buffer = BytesIO()
        result.save(output_buffer, format='PNG', optimize=False)
        output_buffer.seek(0)
        return output_buffer.getvalue()
        
    except Exception as e:
        logging.error(f"Background removal failed: {str(e)}")
        raise e