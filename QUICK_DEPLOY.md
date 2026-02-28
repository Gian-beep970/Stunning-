# IMPERIAL HOUSE - Quick Deployment Guide (2 Steps)

## ⚠️ IMPORTANT: DO THESE STEPS IN ORDER

---

## STEP 1: Upload Code to GitHub (3 minutes)

### A. Create GitHub Account
1. Go to **github.com**
2. Click "Sign up"
3. Enter email, password, username
4. Verify your email

### B. Create Repository
1. After login, click **"+"** in top right
2. Click **"New repository"**
3. Name it: `imperial-house`
4. Click **"Create repository"**

### C. Upload Your Code
1. Click **"Upload files"** button
2. Drag & drop all files from `c:\tennis_payment_system\` 
3. **SKIP these folders:**
   - `instance/`
   - `__pycache__/`
   - Do NOT upload `.env` file (contains secrets!)
4. Click **"Commit changes"** at bottom

**✅ Done! Your code is now on GitHub**

---

## STEP 2: Deploy to Render (3 minutes)

### A. Create Render Account
1. Go to **https://render.com**
2. Click **"Sign up"**
3. Choose "GitHub" option (easiest)
4. Authorize GitHub
5. Verify email

### B. Create Web Service
1. Click **"Dashboard"** in top right
2. Click **"+ New"** button
3. Select **"Web Service"** 
4. Click **"Connect"** next to your GitHub account
5. Search for `imperial-house` 
6. Click **"Connect"** on the repository

### C. Fill in Deployment Settings

**Copy-paste these exactly:**

| Setting | Value |
|---------|-------|
| **Name** | `imperial-house` |
| **Region** | `Frankfurt` |
| **Build Command** | `pip install -r requirements.txt && python run.py init_db` |
| **Start Command** | `gunicorn -w 4 -b 0.0.0.0:$PORT run:app` |

### D. Set Environment Variables
1. Click **"Environment"** tab
2. Click **"+ Add Environment Variable"**
3. Add these 2 variables:

**Variable 1:**
```
Name: FLASK_ENV
Value: production
```

**Variable 2:**
```
Name: SECRET_KEY
Value: MjNlYWViMTg0ODk0ZjZmMmU3MzVmZmExZWJlNzc2YTI=
```
(This is a pre-generated secure key - use as-is)

### E. Deploy
1. Click **"Create Web Service"** button at bottom
2. **Wait 2-3 minutes** while it deploys
3. You'll see a URL like: 
   ```
   https://imperial-house.onrender.com
   ```

### F. Test the URL
1. Copy your Render URL
2. Visit it in your browser
3. You should see the IMPERIAL HOUSE home page!
4. Try registering and logging in

---

## ✅ DONE! Your App is Live!

### Test on Your Phone:
1. Get your phone (any Kenyan network)
2. Paste the Render URL in browser
3. The website will work perfectly on mobile!
4. Share the link with others

---

## 📱 Share This Link

Once deployed, people can access it from any phone in Kenya with this link:
```
https://imperial-house.onrender.com
```

---

## 🔗 Optional: Get a Custom Domain

Instead of the long Render URL, get a custom domain:

1. Buy domain from **namecheap.com** (~KES 2,000/year)
   - Example: `imperialhouse.co.ke`

2. In Render dashboard:
   - Find your service
   - Click "Custom Domains"
   - Enter domain name
   - Follow instructions to add DNS records

3. Wait 5-30 minutes for connection
4. Access via custom domain!

---

## ❌ Troubleshooting

**"Build failed" error:**
- Check that all files are uploaded
- Make sure requirements.txt is included
- Check GitHub repo has all files

**"Application error" on live URL:**
- Go to Render dashboard
- Click your service name
- Check "Logs" tab for error
- Usually means environment variable wasn't set

**"Very slow on mobile in Kenya:"**
- Already optimized! Frankfurt region is closest to Kenya
- Try refreshing page (2nd load is faster due to caching)

**Need more help?**
- Render docs: https://render.com/docs
- Can reply here with error message

---

## 📊 Monitoring Your Live App

After deployment, keep an eye on:

1. **View Logs:**
   - Render Dashboard → Your Service → "Logs" tab
   - Shows all errors and user activity

2. **Check Status:**
   - Click service name
   - See if "Live" (green) or "failed" (red)

3. **Enable Auto-Deploy:**
   - Settings tab → Turn on auto-deploy
   - Now when you push changes to GitHub, app auto-updates!

---

**Your app is now accessible from ANY phone in Kenya!** 🚀

