# AI Background Remover

A Flask web application that automatically removes backgrounds from images using AI technology.

## Features

- **Drag & drop file upload** with visual feedback
- **AI-powered background removal** using ONNX models
- **Multiple image formats** supported (PNG, JPG, JPEG, WebP)
- **Responsive design** with Bootstrap
- **Real-time progress** indicators
- **Automatic file cleanup** after download

## Quick Deploy to Fly.io (Free Hosting)

### Option 1: GitHub Deploy (Easiest)
1. Fork/upload this repository to GitHub
2. Sign up at [fly.io](https://fly.io/apps)
3. Get your API token from [dashboard](https://fly.io/user/personal_access_tokens)
4. Add token as `FLY_API_TOKEN` in GitHub repository secrets
5. Edit `fly.toml` and change app name to something unique
6. Push to GitHub - auto-deploys!

### Option 2: CLI Deploy
```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
flyctl launch
```

## Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

Visit `http://localhost:5000`

## File Structure

```
├── main.py              # Flask app entry point
├── app.py               # Main application logic
├── background_remover.py # Custom AI background removal
├── templates/           # HTML templates
├── static/             # CSS, JS, assets
├── Dockerfile          # Container configuration
├── fly.toml            # Fly.io deployment config
└── .github/workflows/  # Auto-deployment
```

## Tech Stack

- **Backend:** Flask, Python 3.11
- **AI Processing:** ONNX Runtime, PIL
- **Frontend:** Bootstrap 5, Vanilla JavaScript
- **Deployment:** Docker, Fly.io

## Free Hosting Limits

- 3 apps maximum
- 512MB RAM, shared CPU
- Apps sleep after inactivity
- Ephemeral storage (files lost on restart)

## License

MIT License - feel free to use and modify!