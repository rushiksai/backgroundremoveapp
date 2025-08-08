# AI Background Remover

## Overview

This is a Flask-based web application that provides automated background removal from images using AI technology. The application allows users to upload images through a drag-and-drop interface and download the processed images with transparent backgrounds. It uses the `rembg` library for AI-powered background removal and provides a clean, responsive web interface built with Bootstrap.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Single Page Application**: Uses vanilla JavaScript with Bootstrap for styling and responsive design
- **Interactive Upload Interface**: Drag-and-drop file upload with visual feedback and progress indicators
- **Real-time Preview**: Side-by-side comparison of original and processed images
- **Responsive Design**: Mobile-friendly interface using Bootstrap's grid system

### Backend Architecture
- **Flask Web Framework**: Lightweight Python web server handling HTTP requests and file processing
- **RESTful API Design**: Clean separation between upload endpoints and file serving
- **File Management System**: Organized directory structure for uploads and processed files
- **Error Handling**: Comprehensive validation for file types, sizes, and processing errors

### Image Processing Pipeline
- **AI Background Removal**: Uses the `rembg` library for automated background detection and removal
- **Format Support**: Handles PNG, JPG, JPEG, and WebP image formats
- **File Size Validation**: 16MB maximum file size limit to prevent resource exhaustion
- **Unique File Naming**: UUID-based naming system to prevent filename conflicts

### Security and Validation
- **File Type Restrictions**: Whitelist-based file extension validation
- **Secure Filename Handling**: Uses Werkzeug's secure_filename for safe file operations
- **Session Management**: Flask sessions with configurable secret keys
- **Proxy Support**: ProxyFix middleware for proper header handling in production environments

## External Dependencies

### Core Libraries
- **Flask**: Web framework for handling HTTP requests and responses
- **rembg**: AI library for automated background removal from images
- **PIL (Pillow)**: Image processing and manipulation library
- **Werkzeug**: WSGI utilities for secure file handling and middleware

### Frontend Dependencies
- **Bootstrap 5**: CSS framework for responsive design and UI components
- **Font Awesome 6**: Icon library for user interface elements
- **Custom CSS**: Additional styling for drag-and-drop functionality and image previews

### Development Tools
- **Python Logging**: Built-in logging system for debugging and monitoring
- **UUID**: Unique identifier generation for file naming
- **OS Module**: File system operations and environment variable handling

### File Storage
- **Local File System**: Images stored in organized upload and processed directories
- **Temporary File Management**: Automatic cleanup and organization of processed files

## Deployment Configuration

### Fly.io Deployment
- **Docker-based deployment** using Python 3.11 slim image
- **Auto-scaling configuration** with sleep/wake functionality for free tier
- **Health checks** configured for reliable service monitoring
- **Resource limits** optimized for free tier (512MB RAM, 1 shared CPU)

### Production Considerations
- **Ephemeral storage** on Fly.io free tier (uploaded files lost on restart)
- **Custom background removal** implementation to avoid Python version conflicts
- **Graceful fallbacks** for model loading and processing errors