# Deploy IMPERIAL HOUSE to Render (5 Minutes)

## Step 1: Push Code to GitHub

### 1.1 Create GitHub Account
- Go to github.com and create a free account
- Verify your email

### 1.2 Create Repository
1. Click "+" > "New repository"
2. Name: `imperial-house`
3. Description: "Rental property listing platform for Kenya"
4. ✅ Add .gitignore (Python)
5. ✅ Add README
6. Click "Create repository"

### 1.3 Upload Files
1. Click "Add file" > "Upload files"
2. Select all files from your local folder EXCEPT:
   - `instance/` folder
   - `__pycache__/` folders
   - `.env` file (never upload secrets!)
3. Message: "Initial commit"
4. Click "Commit changes"

**OR use command line (if git installed):**
```bash
cd c:\tennis_payment_system
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/imperial-house.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy to Render

### 2.1 Create Render Account
1. Go to https://render.com
2. Click "Sign up"
3. Use GitHub or email
4. Verify email

### 2.2 Create Web Service
1. Click "Dashboard"
2. Click "New +" button
3. Select "Web Service"
4. Click "Connect" next to your GitHub account
5. Search for `imperial-house` repository
6. Click "Connect"

### 2.3 Configure Deployment
Fill in these settings:

**Name:** `imperial-house-ke` (or similar)

**Environment:** `Python 3.11`

**Region:** `Frankfurt` (closest to Kenya - fastest)

**Build Command:**
```
pip install -r requirements.txt && python -c "from app import create_app, db; app = create_app('production'); app.app_context().push(); db.create_all()"
```

**Start Command:**
```
gunicorn -w 4 -b 0.0.0.0:$PORT run:app
```

### 2.4 Set Environment Variables
Click "Environment" and add these variables:

| Key | Value | Example |
|-----|-------|---------|
| `FLASK_ENV` | `production` | production |
| `SECRET_KEY` | Long random string | `your-secret-key-here` |
| `DATABASE_URL` | PostgreSQL URL | auto-generated |

**To generate SECRET_KEY:**
In Python shell:
```python
import secrets
print(secrets.token_urlsafe(32))
```

### 2.5 Deploy
- Click "Create Web Service"
- Wait ~2-3 minutes for deployment
- You'll see a live URL like: `https://imperial-house-ke.onrender.com`

---

## Step 3: Test the Deployment

### 3.1 Test on Desktop
1. Visit the URL provided by Render
2. Test registration
3. Test login
4. Test browsing properties

### 3.2 Test on Mobile
1. Get your phone (any Kenya network)
2. Visit the URL in browser
3. Test all features:
   - Browse houses
   - Register as tenant/landlord
   - Upload photos (landlords)
   - Add to favorites (tenants)
   - Message features

### 3.3 Test on Different Networks
If possible, test on:
- Safaricom
- Airtel
- Equity
- Telkom

---

## Step 4: Add Custom Domain (Optional but Recommended)

### 4.1 Buy Domain
- Go to namecheap.com or similar
- Search for domain (e.g., `imperialhouse.co.ke`)
- Cost: ~KES 1,500-3,000 per year

### 4.2 Connect to Render
1. In Render dashboard, go to your service
2. Click "Custom Domains"
3. Enter your domain name
4. Click "Add"
5. Copy the CNAME record shown
6. Go to your domain registrar (Namecheap, etc)
7. Add CNAME record:
   - Host: `www`
   - Value: (paste from Render)
8. Wait 5-30 minutes for DNS to update
9. Visit your custom domain!

---

## Step 5: Monitor & Maintain

### 5.1 View Logs
1. In Render dashboard, click your service
2. Click "Logs" tab
3. See real-time errors and info

### 5.2 Enable Auto-Deploy
1. In Render, go to your service
2. Click "Settings"
3. Enable "Auto-Deploy" for `main` branch
4. Now each GitHub push auto-deploys!

### 5.3 Database Backup
Render provides daily backups automatically. To download:
1. Go to your PostgreSQL database in Render
2. Look for "Backups" section
3. Download when needed

---

## Common Issues & Fixes

### Issue: "Build failed"
**Fix:** Check Build Logs in Render for error message. Usually:
- Missing dependency in requirements.txt
- Typo in build command
- Missing environment variable

### Issue: "Application error"
**Fix:** Check Runtime Logs. Usually:
- `SECRET_KEY` not set
- DATABASE_URL not set
- Database initialization failed

### Issue: "Slow in Kenya"
**Fix:** 
- Already using Frankfurt region (fastest to Kenya)
- Enable Render's caching
- Optimize image sizes
- Use CDN (see below)

### Issue: "Not accessible from Kenya network"
**Fix:** Very rare. Try:
- Restart service in Render dashboard
- Check if ISP is blocking (contact them)
- Use VPN if completely blocked (unlikely)

---

## Speed Optimization for Kenya Networks

After deployment, optimize for speed:

### 1. Enable Compression
Already enabled in Flask

### 2. Optimize Images
Before uploading to platform, resize to:
- Max width: 1200px
- Quality: 80-85%
- Format: JPEG or WebP

### 3. Use CDN (Optional)
Add CloudFlare (free):
1. cloudflare.com > Sign up
2. Add your domain
3. Add nameservers to registrar
4. Gets automatic caching + DDoS protection

---

## Production Checklist

- [ ] Code pushed to GitHub
- [ ] Render account created
- [ ] Web service deployed
- [ ] Environment variables set
- [ ] Database initialized
- [ ] Tested on desktop
- [ ] Tested on mobile
- [ ] Tested on Kenya networks
- [ ] Custom domain added (optional)
- [ ] Auto-deploy enabled
- [ ] Monitoring enabled

---

## Next Steps After Deployment

1. **Share the link** with first beta users
2. **Collect feedback** on mobile experience
3. **Monitor logs** for errors
4. **Add features** based on feedback
5. **Scale** as traffic grows

---

## Support & Resources

- **Render Docs:** https://render.com/docs
- **Flask Docs:** https://flask.palletsprojects.com
- **PostgreSQL Docs:** https://www.postgresql.org/docs
- **GitHub Help:** https://help.github.com

---

**Your app will be live and accessible from any phone in Kenya within 5-10 minutes!** 🎉

