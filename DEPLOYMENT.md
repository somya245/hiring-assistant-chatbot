# Deployment Guide - TalentScout Hiring Assistant

## 🚀 Deployment Options

This guide covers various deployment options for the TalentScout Hiring Assistant chatbot.

---

## Option 1: Streamlit Cloud (Easiest & Free)

### Why Streamlit Cloud?
- ✅ Free hosting for public apps
- ✅ Automatic updates from GitHub
- ✅ Built for Streamlit apps
- ✅ Easy environment variable management
- ✅ HTTPS by default

### Steps:

1. **Push to GitHub**
   ```bash
   git remote add origin https://github.com/yourusername/hiring-assistant-chatbot.git
   git branch -M main
   git push -u origin main
   ```

2. **Sign up on Streamlit Cloud**
   - Visit https://streamlit.io/cloud
   - Sign in with GitHub
   - Click "New App"

3. **Deploy**
   - Repository: Select your repo
   - Branch: main
   - Main file path: app.py
   - Click Deploy

4. **Set Secrets**
   - In Streamlit Cloud dashboard, click project settings
   - Go to "Secrets" tab
   - Add your `OPENAI_API_KEY`
   - Format:
     ```
     OPENAI_API_KEY = "sk-..."
     ```

5. **Access Your App**
   - URL: `https://<username>-hiring-assistant-chatbot.streamlit.app`
   - Share with anyone!

**Estimated Time**: 5 minutes  
**Cost**: Free (with limitations)

---

## Option 2: AWS EC2 (Most Control)

### Why AWS?
- ✅ Full control over infrastructure
- ✅ Scalable solution
- ✅ Custom domain support
- ✅ Better for production use

### Requirements:
- AWS Account
- Basic AWS knowledge

### Steps:

1. **Launch EC2 Instance**
   ```bash
   # AMI: Ubuntu Server 22.04 LTS
   # Instance Type: t3.micro (free tier eligible)
   # Security Group: Allow SSH (22) and HTTP (80, 443)
   ```

2. **SSH into Instance**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip python3-venv git -y
   ```

4. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/hiring-assistant-chatbot.git
   cd hiring-assistant-chatbot
   ```

5. **Setup Virtual Environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

6. **Create Systemd Service**
   ```bash
   sudo nano /etc/systemd/system/streamlit.service
   ```
   
   Content:
   ```ini
   [Unit]
   Description=TalentScout Hiring Assistant
   After=network.target

   [Service]
   Type=simple
   User=ubuntu
   WorkingDirectory=/home/ubuntu/hiring-assistant-chatbot
   Environment="OPENAI_API_KEY=sk-..."
   ExecStart=/home/ubuntu/hiring-assistant-chatbot/venv/bin/streamlit run app.py --server.port=80
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

7. **Start Service**
   ```bash
   sudo systemctl enable streamlit
   sudo systemctl start streamlit
   sudo systemctl status streamlit
   ```

8. **Point Domain (Optional)**
   - Update Route53 or your DNS provider
   - Point to EC2 Elastic IP

**Estimated Time**: 20 minutes  
**Cost**: ~$3-5/month (or free tier if eligible)

---

## Option 3: Google Cloud Run (Balanced)

### Why Google Cloud Run?
- ✅ Serverless (pay per use)
- ✅ Auto-scaling
- ✅ Easy deployment
- ✅ Good free tier

### Steps:

1. **Install Google Cloud SDK**
   ```bash
   # Visit: https://cloud.google.com/sdk/docs/install
   ```

2. **Authenticate**
   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

3. **Create Dockerfile**
   ```dockerfile
   FROM python:3.9-slim

   WORKDIR /app

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   EXPOSE 8080

   CMD ["streamlit", "run", "app.py", "--server.port=8080"]
   ```

4. **Deploy**
   ```bash
   gcloud run deploy hiring-assistant \
     --source . \
     --platform managed \
     --region us-central1 \
     --set-env-vars OPENAI_API_KEY=sk-...
   ```

5. **Access**
   - Your app URL will be provided after deployment
   - Example: `https://hiring-assistant-xxxxx-uc.a.run.app`

**Estimated Time**: 15 minutes  
**Cost**: Free tier (> free tier: ~$0.00002/request)

---

## Option 4: Heroku (Simple)

### Why Heroku?
- ✅ Simple deployment
- ✅ Git-based deployment
- ✅ Easy environment variables
- ✅ Good for demos

### Steps:

1. **Install Heroku CLI**
   ```bash
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Procfile**
   ```
   web: streamlit run app.py --server.port=$PORT
   ```

3. **Create .streamlit/config.toml**
   ```toml
   [server]
   maxUploadSize = 200
   headless = true
   ```

4. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=sk-...
   git push heroku main
   ```

5. **View Logs**
   ```bash
   heroku logs --tail
   ```

**Estimated Time**: 10 minutes  
**Cost**: Free tier ended; now starts at ~$5-7/month

---

## Option 5: Docker + Any Host

### Why Docker?
- ✅ Works everywhere
- ✅ Consistent environments
- ✅ Easy to scale

### Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . .

# Expose port
EXPOSE 8501

# Set environment
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501

# Run app
CMD ["streamlit", "run", "app.py"]
```

### Build and Run Locally

```bash
# Build
docker build -t hiring-assistant:latest .

# Run
docker run -e OPENAI_API_KEY=sk-... -p 8501:8501 hiring-assistant:latest
```

### Push to Docker Hub

```bash
docker tag hiring-assistant:latest yourusername/hiring-assistant:latest
docker push yourusername/hiring-assistant:latest
```

---

## 📊 Deployment Comparison

| Feature | Streamlit Cloud | AWS EC2 | Google Cloud Run | Heroku | Docker |
|---------|---|---|---|---|---|
| **Ease** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Cost** | Free | ~$3-5/mo | Pay per use | $5-7+/mo | Varies |
| **Scalability** | Limited | High | High | Medium | High |
| **Custom Domain** | Limited | Yes | Yes | Yes | Yes |
| **Setup Time** | 5 min | 20 min | 15 min | 10 min | 10 min |

---

## 🔒 Security Best Practices

### For all deployments:

1. **Never commit `.env`**
   ```bash
   # Already in .gitignore ✓
   ```

2. **Use environment variables for secrets**
   ```python
   api_key = os.getenv("OPENAI_API_KEY")
   ```

3. **Enable HTTPS/TLS**
   - Streamlit Cloud: ✓ Automatic
   - AWS: Use AWS Certificate Manager
   - Google Cloud Run: ✓ Automatic
   - Heroku: ✓ Automatic

4. **Set up monitoring**
   - Monitor API usage
   - Set spending limits in OpenAI
   - Enable logging

5. **Rate limiting** (Optional)
   ```python
   # Add to app.py
   from streamlit_throttle import throttle
   @throttle(calls=10, period=60)  # 10 calls per minute
   def process_input(text):
       pass
   ```

---

## 📈 Monitoring & Maintenance

### Track Usage
```bash
# Check API usage via OpenAI dashboard
# https://platform.openai.com/usage/overview
```

### Monitor Costs
- Set spending limit in OpenAI settings
- Monitor deployment logs regularly
- Check for errors and performance

### Update Application
```bash
# Make changes locally
git add .
git commit -m "fix: Update prompts"
git push origin main

# Auto-deploys on Streamlit Cloud
# Manual redeploy for other platforms
```

---

## 🚨 Troubleshooting Deployment

### App crashes after deployment
- Check logs: `streamlit logs` or platform logs
- Verify environment variables are set
- Check API key is valid
- Verify Python version compatibility

### App is slow
- Check internet connection
- Verify OpenAI API status
- Consider caching responses
- Optimize prompt length

### High costs
- Set spending limits in OpenAI
- Monitor API usage
- Consider caching/batching requests
- Use gpt-3.5-turbo (cheaper than gpt-4)

---

## 📝 Recommended for Assignment

For this 48-hour assignment, I recommend:

1. **Best Option: Streamlit Cloud**
   - ✅ Free
   - ✅ Fastest deployment (5 minutes)
   - ✅ Perfect for demo/presentation
   - ✅ Easy to share link

2. **Backup Option: Google Cloud Run**
   - ✅ Good if Streamlit Cloud doesn't work
   - ✅ Still fast and simple
   - ✅ Free tier available

---

## 📚 Additional Resources

- [Streamlit Deployment Guide](https://docs.streamlit.io/streamlit-cloud)
- [AWS Deployment](https://aws.amazon.com/getting-started/)
- [Google Cloud Run](https://cloud.google.com/run/docs)
- [Docker Basics](https://docs.docker.com/)

---

**Version**: 1.0.0 | **Last Updated**: February 2026
