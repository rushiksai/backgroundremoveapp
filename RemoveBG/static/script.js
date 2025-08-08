// Background Remover App JavaScript

let currentFile = null;
let uploadInProgress = false;

// DOM elements
const uploadArea = document.getElementById('upload-area');
const fileInput = document.getElementById('file-input');
const progressContainer = document.getElementById('progress-container');
const progressBar = document.getElementById('progress-bar');
const progressText = document.getElementById('progress-text');
const previewArea = document.getElementById('preview-area');
const originalPreview = document.getElementById('original-preview');
const processedPreview = document.getElementById('processed-preview');
const processingPlaceholder = document.getElementById('processing-placeholder');
const downloadSection = document.getElementById('download-section');
const downloadBtn = document.getElementById('download-btn');
const alertContainer = document.getElementById('alert-container');

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
});

function setupEventListeners() {
    // File input change
    fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop events
    uploadArea.addEventListener('click', () => {
        if (!uploadInProgress) {
            fileInput.click();
        }
    });
    
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);
    
    // Prevent default drag behaviors on document
    document.addEventListener('dragover', e => e.preventDefault());
    document.addEventListener('drop', e => e.preventDefault());
}

function handleFileSelect(event) {
    const file = event.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(event) {
    event.preventDefault();
    uploadArea.classList.add('dragover');
}

function handleDragLeave(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
}

function handleDrop(event) {
    event.preventDefault();
    uploadArea.classList.remove('dragover');
    
    if (uploadInProgress) return;
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFile(files[0]);
    }
}

function processFile(file) {
    if (uploadInProgress) return;
    
    // Validate file type
    const allowedTypes = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp'];
    if (!allowedTypes.includes(file.type)) {
        showAlert('Invalid file type. Please upload a PNG, JPG, JPEG, or WebP image.', 'danger');
        return;
    }
    
    // Validate file size (16MB)
    const maxSize = 16 * 1024 * 1024;
    if (file.size > maxSize) {
        showAlert('File too large. Maximum size is 16MB.', 'danger');
        return;
    }
    
    currentFile = file;
    uploadInProgress = true;
    
    // Show preview
    showOriginalPreview(file);
    
    // Start upload and processing
    uploadFile(file);
}

function showOriginalPreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        originalPreview.src = e.target.result;
        previewArea.style.display = 'block';
        processedPreview.style.display = 'none';
        processingPlaceholder.style.display = 'flex';
    };
    reader.readAsDataURL(file);
}

function uploadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    // Show progress
    progressContainer.style.display = 'block';
    uploadArea.style.display = 'none';
    
    // Simulate progress for better UX
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 15;
        if (progress > 90) {
            clearInterval(progressInterval);
            progress = 90;
        }
        updateProgress(progress);
    }, 200);
    
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        clearInterval(progressInterval);
        updateProgress(100);
        
        setTimeout(() => {
            if (data.success) {
                handleUploadSuccess(data);
            } else {
                handleUploadError(data.error || 'Upload failed');
            }
        }, 500);
    })
    .catch(error => {
        clearInterval(progressInterval);
        console.error('Upload error:', error);
        handleUploadError('Upload failed. Please check your connection and try again.');
    });
}

function updateProgress(percentage) {
    progressBar.style.width = percentage + '%';
    progressText.textContent = Math.round(percentage) + '%';
}

function handleUploadSuccess(data) {
    // Hide progress
    progressContainer.style.display = 'none';
    
    // Show processed image
    processedPreview.onload = function() {
        processingPlaceholder.style.display = 'none';
        processedPreview.style.display = 'block';
        downloadSection.style.display = 'block';
    };
    
    processedPreview.src = data.download_url;
    downloadBtn.href = data.download_url;
    
    showAlert(data.message, 'success');
    uploadInProgress = false;
}

function handleUploadError(errorMessage) {
    // Hide progress
    progressContainer.style.display = 'none';
    
    // Show upload area again
    uploadArea.style.display = 'block';
    previewArea.style.display = 'none';
    
    showAlert(errorMessage, 'danger');
    uploadInProgress = false;
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show mt-3`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Clear existing alerts
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alertDiv);
    
    // Auto-dismiss success alerts after 5 seconds
    if (type === 'success') {
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

function resetUpload() {
    // Reset all UI elements
    uploadArea.style.display = 'block';
    progressContainer.style.display = 'none';
    previewArea.style.display = 'none';
    downloadSection.style.display = 'none';
    alertContainer.innerHTML = '';
    
    // Reset form
    fileInput.value = '';
    currentFile = null;
    uploadInProgress = false;
    
    // Reset progress
    updateProgress(0);
}

// Utility function to format file size
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Handle page visibility change to reset upload if user navigates away
document.addEventListener('visibilitychange', function() {
    if (document.hidden && uploadInProgress) {
        // User navigated away during upload, reset when they come back
        setTimeout(() => {
            if (!document.hidden) {
                resetUpload();
            }
        }, 1000);
    }
});
