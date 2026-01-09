# Deploying to Streamlit Community Cloud - Step by Step Guide

## ✅ Prerequisites Completed

- [x] Git repository initialized
- [x] Files committed to Git
- [x] requirements.txt created with minimal dependencies
- [x] .gitignore configured to include data files
- [x] README created for GitHub

## 🚀 Deployment Steps

### Step 1: Create a GitHub Account (if you don't have one)

1. Go to https://github.com
2. Click "Sign up"
3. Follow the registration process
4. Verify your email address

### Step 2: Create a New GitHub Repository

1. Log in to GitHub
2. Click the **"+"** icon in the top right corner
3. Select **"New repository"**
4. Fill in the details:
   - **Repository name**: `steel-price-forecasting` (or any name you prefer)
   - **Description**: "Interactive dashboard for steel price forecasting using ML"
   - **Visibility**: Choose **Public** (required for free Streamlit Cloud tier)
   - **DO NOT** initialize with README, .gitignore, or license (we already have these)
5. Click **"Create repository"**

### Step 3: Push Your Code to GitHub

GitHub will show you commands. Use these in your terminal:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/steel-price-forecasting.git

# Rename branch to main (GitHub's default)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/abdul/steel-price-forecasting.git
git branch -M main
git push -u origin main
```

When prompted, enter your GitHub username and password (or personal access token).

### Step 4: Deploy to Streamlit Community Cloud

1. Go to https://share.streamlit.io
2. Click **"Sign in with GitHub"**
3. Authorize Streamlit to access your GitHub account
4. Click **"New app"** button
5. Fill in the deployment form:

   **Repository:**
   - Select your repository: `YOUR_USERNAME/steel-price-forecasting`

   **Branch:**
   - Select: `main`

   **Main file path:**
   - Enter: `dashboard.py`

   **App URL (optional):**
   - Custom URL: `steel-forecasting-dashboard` (or leave blank for auto-generated)

6. Click **"Deploy!"**

### Step 5: Wait for Deployment (2-5 minutes)

Streamlit Cloud will:
- ✅ Clone your repository
- ✅ Install dependencies from requirements.txt
- ✅ Load your data files
- ✅ Start the dashboard

You'll see a progress screen with logs. Watch for:
```
Installing requirements...
✓ streamlit
✓ plotly
✓ pandas
✓ numpy
✓ scikit-learn
✓ scipy

Starting app...
✓ App is live!
```

### Step 6: Access Your Dashboard

Once deployed, you'll get a URL like:
```
https://steel-forecasting-dashboard.streamlit.app
```

Or:
```
https://YOUR_USERNAME-steel-price-forecasting.streamlit.app
```

**Share this URL with anyone!** It's publicly accessible.

---

## 🔧 Troubleshooting

### Error: "ModuleNotFoundError: No module named 'sklearn'"

**Cause**: requirements.txt not found or incorrect

**Fix**: Ensure `requirements.txt` is in the root directory with:
```
streamlit>=1.28.0
plotly>=5.17.0
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
scipy>=1.11.0
```

### Error: "FileNotFoundError: data/extracted/steel_prices_synthetic_with_external.csv"

**Cause**: Data files not committed to Git

**Fix**: Check .gitignore isn't excluding data files. Run:
```bash
git add data/
git commit -m "Add data files for dashboard"
git push
```

Then in Streamlit Cloud, click **"Reboot app"**

### Error: "This app has exceeded its resource limits"

**Cause**: App using too much memory (free tier: 1GB limit)

**Fix**:
1. Reduce data size (use only last 90 days)
2. Add to dashboard.py:
```python
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    df = pd.read_csv(...)
    return df.tail(90)  # Only last 90 days
```

### Dashboard Loads Slowly

**Fix**: Enable caching (already implemented in your dashboard.py)

Ensure you have:
```python
@st.cache_data
def load_data():
    # Your data loading code
```

---

## 🎨 Customization After Deployment

### Change App Theme

In Streamlit Cloud dashboard:
1. Click **"Settings"** (⚙️ icon)
2. Go to **"Theme"**
3. Choose Light/Dark mode
4. Customize colors

### Update App (Push New Changes)

Whenever you update code locally:

```bash
# Make changes to dashboard.py or other files
git add .
git commit -m "Update dashboard with new feature"
git push
```

Streamlit Cloud will **automatically redeploy** (takes ~1-2 minutes).

### Monitor App Usage

In Streamlit Cloud dashboard:
- View **Analytics** to see:
  - Number of visitors
  - Session duration
  - Page views
  - Error logs

---

## 💰 Streamlit Cloud Pricing (2025)

### Free Tier (Community Cloud)
- ✅ **1 public app** (unlimited visitors)
- ✅ **1 GB RAM** per app
- ✅ **1 CPU core**
- ✅ **Unlimited** deployment updates
- ✅ **GitHub integration**
- ✅ **Community support**

**Perfect for your project!** Your dashboard uses ~200MB RAM.

### Paid Tier (if you need more later)
- **$20/month**: 3 private apps, 2GB RAM each
- **$200/month**: Unlimited apps, 4GB RAM, priority support

---

## 🔐 Security & Privacy

### Your Current Setup (Public)
- ✅ Repository is public
- ✅ Dashboard is publicly accessible
- ✅ Using **synthetic data** (safe to share)

### For Production with Real Data

If you add real proprietary data later:

1. **Make repository private**:
   - GitHub: Settings → Danger Zone → Change visibility
   - Requires Streamlit Cloud paid tier ($20/month)

2. **Use Streamlit Secrets** for API keys:
   - Streamlit Cloud: Settings → Secrets
   - Add:
   ```toml
   [api]
   fastmarkets_key = "your_key_here"
   platts_key = "your_key_here"
   ```

   In code:
   ```python
   import streamlit as st
   api_key = st.secrets["api"]["fastmarkets_key"]
   ```

3. **Add authentication** (optional):
   - Use `streamlit-authenticator` library
   - Add login page before dashboard

---

## 📊 Your Current Repository Size

```
Total Size: ~2.5 MB
├── dashboard.py: 30 KB
├── data/extracted/: ~1.2 MB
├── data/validation/: ~50 KB
├── Documentation: ~200 KB
└── Other files: ~50 KB
```

**Well within free tier limits!** (Limit: 1GB)

---

## 🚀 Advanced: Custom Domain (Optional)

If you want a custom domain like `dashboard.yoursteel.com`:

1. Buy a domain (Namecheap, GoDaddy, etc.)
2. In Streamlit Cloud: Settings → Custom Domain
3. Add CNAME record in DNS:
   ```
   CNAME: dashboard
   Value: YOUR-APP.streamlit.app
   ```
4. Wait for DNS propagation (5-30 minutes)

**Note**: Custom domains available on paid tier only.

---

## ✅ Post-Deployment Checklist

After deployment, verify:

- [ ] Dashboard loads without errors
- [ ] All 5 pages are accessible
- [ ] Charts display correctly
- [ ] Data tables show values
- [ ] ROI calculator works
- [ ] No "FileNotFoundError" in logs
- [ ] Page load time < 5 seconds

### Test Your Deployment:

1. **Overview Page**: Should show current price $607.50
2. **Price History**: Should display 17 symbols
3. **Forecasts**: Should show 1/7/30-day charts
4. **Model Performance**: Should display validation results
5. **Business Value**: Calculator should compute savings

---

## 📧 Support

### Streamlit Cloud Issues:
- Documentation: https://docs.streamlit.io/streamlit-community-cloud
- Forum: https://discuss.streamlit.io
- Email: support@streamlit.io

### App-Specific Issues:
- Check app logs in Streamlit Cloud dashboard
- Review error messages in terminal
- Verify all data files are committed to Git

---

## 🎉 You're Done!

Once deployed, your dashboard will be:
- ✅ **Live** 24/7 on Streamlit Cloud
- ✅ **Accessible** from anywhere via URL
- ✅ **Free** to host and share
- ✅ **Auto-updated** when you push to GitHub

**Share your dashboard URL with:**
- Your team
- Stakeholders
- Procurement department
- Finance team
- Anyone interested in steel price forecasting!

---

**Next Steps:**
1. Push code to GitHub (Step 3 above)
2. Deploy to Streamlit Cloud (Step 4 above)
3. Share your dashboard URL
4. Enjoy! 🎉
