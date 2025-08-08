import os
import logging
from flask import Flask, render_template, request, send_file, flash, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import uuid
import io

# Check for dependencies
CUSTOM_BG_REMOVER = False
try:
    from rembg import remove
    REMBG_AVAILABLE = True
    logging.info("Using rembg library for background removal")
except ImportError:
    try:
        from background_remover import remove_background_simple
        REMBG_AVAILABLE = True
        CUSTOM_BG_REMOVER = True
        logging.info("Using custom background removal implementation")
    except ImportError:
        REMBG_AVAILABLE = False
        CUSTOM_BG_REMOVER = False
        logging.warning("Background removal feature disabled - no implementation available")

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    logging.warning("PIL library not available - some image features disabled")

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Configuration
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

# Ensure upload and processed directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

def allowed_file(filename):
    """Check if the uploaded file has an allowed extension."""
    if not filename or '.' not in filename:
        return False
    return filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with upload interface."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and background removal."""
    try:
        # Check if the post request has the file part
        if 'file' not in request.files:
            return jsonify({'error': 'No file selected'}), 400
        
        file = request.files['file']
        
        # If user does not select file, browser also submits an empty part without filename
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            # Generate unique filename
            file_id = str(uuid.uuid4())
            original_extension = file.filename.rsplit('.', 1)[1].lower()
            filename = f"{file_id}.{original_extension}"
            
            # Save uploaded file
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Process the image to remove background
            try:
                if not REMBG_AVAILABLE:
                    return jsonify({'error': 'Background removal service is currently unavailable. Please try again later.'}), 503
                
                with open(filepath, 'rb') as input_file:
                    input_data = input_file.read()
                
                # Remove background using rembg or custom implementation
                if CUSTOM_BG_REMOVER:
                    output_data = remove_background_simple(input_data)
                else:
                    output_data = remove(input_data)
                
                # Save processed image as PNG (to preserve transparency)
                processed_filename = f"{file_id}_processed.png"
                processed_filepath = os.path.join(app.config['PROCESSED_FOLDER'], processed_filename)
                
                with open(processed_filepath, 'wb') as output_file:
                    output_file.write(output_data)
                
                # Clean up original file
                os.remove(filepath)
                
                return jsonify({
                    'success': True,
                    'message': 'Background removed successfully!',
                    'download_url': url_for('download_file', filename=processed_filename)
                })
                
            except Exception as e:
                # Clean up files on error
                if os.path.exists(filepath):
                    os.remove(filepath)
                logging.error(f"Background removal failed: {str(e)}")
                return jsonify({'error': 'Failed to process image. Please try again.'}), 500
        
        else:
            return jsonify({'error': 'Invalid file type. Please upload a PNG, JPG, JPEG, or WebP image.'}), 400
            
    except Exception as e:
        logging.error(f"Upload error: {str(e)}")
        return jsonify({'error': 'Upload failed. Please try again.'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    """Download processed file."""
    try:
        filepath = os.path.join(app.config['PROCESSED_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(filepath):
            flash('File not found or expired.', 'error')
            return redirect(url_for('index'))
        
        # Clean up file after download
        def remove_file(response):
            try:
                os.remove(filepath)
            except Exception as e:
                logging.error(f"Failed to cleanup file: {str(e)}")
            return response
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=f"background_removed_{filename}",
            mimetype='image/png'
        )
        
    except Exception as e:
        logging.error(f"Download error: {str(e)}")
        flash('Download failed. Please try again.', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return render_template('index.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Handle 500 errors."""
    logging.error(f"Server error: {str(e)}")
    return jsonify({'error': 'Internal server error. Please try again.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
