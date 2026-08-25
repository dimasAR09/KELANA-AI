# 🔒 Fix: GitHub Secret Scanning Block

## ❌ Masalah

GitHub mendeteksi **AWS API Key** dalam commit history lama:
- **Commit:** 241d1abdb59a5be0de667a9ce3cdad52a1a25804
- **File:** backend/.env
- **Issue:** File `.env` pernah di-commit dan masih ada di Git history

**GitHub Push Protection** mencegah push untuk melindungi credentials Anda!

---

## ✅ Solusi (Pilih Salah Satu)

### **Solusi 1: Menggunakan Git Filter-Branch** ⭐ (RECOMMENDED)

#### Step 1: Backup Repository
```bash
cd "c:\Program Files\Kelana-ai"
cd ..
xcopy /E /I Kelana-ai Kelana-ai-backup
```

#### Step 2: Remove .env dari History
```bash
cd "c:\Program Files\Kelana-ai"

git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend/.env" --prune-empty --tag-name-filter cat -- --all
```

#### Step 3: Clean Up
```bash
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive
```

#### Step 4: Force Push (Rewrite GitHub History)
```bash
git push origin main --force
git push origin session-5 --force
```

---

### **Solusi 2: Menggunakan GitHub Allow Secret** (Temporary)

**Jika Anda ingin push dulu (NOT RECOMMENDED for production!):**

1. Klik link yang diberikan GitHub:
   ```
   https://github.com/dimasAR09/KELANA-AI/security/secret-scanning/unblock-secret/3IDnhlb4BCjKs8ZlccNV1Bu2my0
   ```

2. GitHub akan minta konfirmasi untuk allow secret

3. Push lagi:
   ```bash
   git push origin main
   git push origin session-5 --force
   ```

**⚠️ WARNING:** Ini TIDAK aman! Credentials Anda tetap exposed di Git history!

---

### **Solusi 3: Start Fresh (Clean Slate)** 

**Jika ingin mulai dari awal dengan clean history:**

#### Option A: Squash All Commits

```bash
cd "c:\Program Files\Kelana-ai"

# Backup first!
git branch backup-before-squash

# Reset to first commit
git checkout --orphan new-main

# Add all files (except .env karena sudah ada di .gitignore)
git add .

# Commit everything
git commit -m "Integrate Amazon Bedrock - Clean Start"

# Delete old main
git branch -D main

# Rename new-main to main
git branch -m main

# Create tag
git tag session-5

# Force push
git push origin main --force
git push origin session-5 --force
```

#### Option B: Delete Repo & Push Fresh

```bash
# 1. Delete repository di GitHub (https://github.com/dimasAR09/KELANA-AI/settings)
# 2. Create new repository dengan nama sama
# 3. Push fresh:

cd "c:\Program Files\Kelana-ai"
git remote remove origin
git remote add origin https://github.com/dimasAR09/KELANA-AI.git
git push -u origin main
git push origin session-5
```

---

## 🔐 PENTING: Rotate AWS Credentials!

**Karena AWS credentials Anda sudah exposed di Git history, Anda HARUS:**

1. **Login ke AWS Console**
2. **Buat API Key baru**
3. **Hapus API Key lama yang ter-leak**
4. **Update file `.env` dengan credentials baru**

### Cara Rotate AWS Credentials:

1. Go to: AWS Console → IAM → Users → Your User
2. Security credentials tab
3. Access keys section
4. "Deactivate" old key yang ter-leak
5. Create new access key
6. Update `.env` file:
   ```
   AWS_BEARER_TOKEN_BEDROCK=NEW_TOKEN_HERE
   ```

---

## 📋 Step-by-Step (Recommended Path)

### **Path 1: Filter-Branch (Keep History)**

```bash
# 1. Backup
cd "c:\Program Files\Kelana-ai"
cd ..
xcopy /E /I Kelana-ai Kelana-ai-backup

# 2. Back to repo
cd Kelana-ai

# 3. Remove .env from history
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend/.env" --prune-empty --tag-name-filter cat -- --all

# 4. Clean up
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# 5. Force push
git push origin main --force
git push origin session-5 --force

# 6. Rotate AWS credentials!
```

### **Path 2: Fresh Start (Clean History)**

```bash
# 1. Backup
cd "c:\Program Files\Kelana-ai"
git branch backup-all-commits

# 2. Create orphan branch
git checkout --orphan new-main

# 3. Add all (except .env)
git add .

# 4. Commit
git commit -m "Integrate Amazon Bedrock"

# 5. Replace main
git branch -D main
git branch -m main

# 6. Tag
git tag session-5

# 7. Force push
git push origin main --force
git push origin session-5 --force

# 8. Rotate AWS credentials!
```

---

## ✅ Verify Success

After push succeeds:

```bash
# 1. Check history doesn't contain .env
git log --all --full-history -- backend/.env
# Should be empty!

# 2. Check GitHub
# Go to: https://github.com/dimasAR09/KELANA-AI
# Browse files - .env should NOT be there

# 3. Check secrets
# GitHub Security tab - should be clear
```

---

## 🆘 Quick Fix Script

**Double-click:** `FIX_SECRET_LEAK.bat`

Script will automatically:
1. Remove .env from entire Git history
2. Clean up references
3. Force push to GitHub

---

## 📝 Prevention for Future

**Already done! ✅**
- `.gitignore` file created
- `.env` now ignored
- `.env.example` as template

**Going forward:**
- `.env` will NEVER be committed again
- Only `.env.example` (template) will be in Git
- Each developer creates their own `.env` from template

---

## ⚡ Quick Command (Copy-Paste)

```bash
cd "c:\Program Files\Kelana-ai"
git filter-branch --force --index-filter "git rm --cached --ignore-unmatch backend/.env" --prune-empty --tag-name-filter cat -- --all
git for-each-ref --format="delete %(refname)" refs/original | git update-ref --stdin
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin main --force
git push origin session-5 --force
```

**Then immediately rotate AWS credentials!** 🔐

---

## 🎯 Summary

**Problem:** `.env` (dengan AWS credentials) ada di commit lama  
**Solution:** Remove dari Git history dengan filter-branch  
**Action Required:** Rotate AWS credentials setelah fix  
**Prevention:** Already in place dengan .gitignore  

**Pilih salah satu solusi di atas dan jalankan!** 🚀
