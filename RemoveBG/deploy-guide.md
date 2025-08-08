# Deploy to Fly.io - Free Hosting Guide

## Easy GitHub Deployment (Recommended)

### Step 1: Push to GitHub
1. Create a new repository on GitHub
2. Upload all your project files to the repository
3. Make sure the `main` or `master` branch contains all files

### Step 2: Set up Fly.io
1. Sign up at [fly.io](https://fly.io/apps) (free account)
2. Go to your [dashboard tokens page](https://fly.io/user/personal_access_tokens)
3. Create a new token and copy it

### Step 3: Configure GitHub Secrets
1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `FLY_API_TOKEN`
5. Value: Paste your Fly.io token
6. Click **Add secret**

### Step 4: Deploy
1. In your GitHub repository, edit `fly.toml`
2. Change the app name from `ai-background-remover` to something unique like:
   - `ai-bg-remover-yourname`
   - `background-remover-123`
3. Commit and push to GitHub
4. GitHub Actions will automatically deploy your app!
5. Check the **Actions** tab to see deployment progress

## Manual CLI Deployment (Alternative)

If you prefer command line:

## Important Notes

### Free Tier Limits
- **Apps:** 3 apps max
- **Resources:** 256MB RAM, shared CPU
- **Runtime:** Apps sleep after inactivity, wake on request
- **Storage:** Ephemeral (files uploaded will be lost on restart)

### Configuration Details

- **App sleeps:** After ~5 minutes of inactivity
- **Wake time:** ~10-30 seconds when accessed
- **File storage:** Temporary only (use external storage for production)
- **Scaling:** Auto-start/stop enabled to stay within free limits

### Troubleshooting

If deployment fails:

1. **Check app name availability:**
   ```bash
   flyctl apps create your-unique-app-name
   ```

2. **View deployment logs:**
   ```bash
   flyctl logs
   ```

3. **Check app status:**
   ```bash
   flyctl status
   ```

4. **Restart the app:**
   ```bash
   flyctl apps restart
   ```

### Custom Domain (Optional)

To use a custom domain:
1. Add your domain in Fly.io dashboard
2. Update DNS records as instructed
3. SSL certificates are automatically provisioned

### Environment Variables

If you need to set environment variables:
```bash
flyctl secrets set SESSION_SECRET=your-secret-key
```

## Support

- Fly.io Documentation: https://fly.io/docs/
- Community Forum: https://community.fly.io/
- Status Page: https://status.fly.io/