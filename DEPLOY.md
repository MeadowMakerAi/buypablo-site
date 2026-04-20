# buypablo.com — Deployment Playbook

## Current State
- Domain: `buypablo.com` registered on GoDaddy, expires July 2027
- Currently shows: GoDaddy "Coming Soon" page with orders@buypablo.com
- Site: Complete static HTML/CSS/JS, ready to serve — no build step needed

## Option A: Vercel (Recommended)

### Why Vercel
- Free tier handles this easily (static site, low traffic)
- Instant deploys from git push
- Global CDN, HTTPS automatic
- Preview URLs for every change

### Steps

**1. Install GitHub CLI + create repo (2 min)**
```bash
brew install gh
gh auth login
cd ~/buypablo.com
git remote add origin https://github.com/YOUR_USERNAME/buypablo.com.git
git push -u origin main
```

**2. Connect Vercel (3 min)**
- Go to vercel.com → sign up with GitHub
- Import the `buypablo.com` repo
- Framework: "Other" (static site, no build)
- Deploy → you'll get a `buypablo-com.vercel.app` preview URL

**3. Point GoDaddy DNS to Vercel (5 min)**
- In Vercel dashboard → Project Settings → Domains → Add `buypablo.com`
- Vercel will tell you the DNS records needed. Typically:
  - A record: `@` → `76.76.21.21`
  - CNAME record: `www` → `cname.vercel-dns.com`
- In GoDaddy → DNS Management:
  - Delete the existing A record pointing to `160.153.0.165` (that's GoDaddy's coming-soon server)
  - Add the Vercel A record
  - Add the CNAME for www
- Propagation: usually 5-30 min, can take up to 48h

**4. Verify**
- Check https://buypablo.com loads the real site
- Check https://www.buypablo.com redirects properly
- HTTPS certificate auto-provisions via Vercel

## Option B: GoDaddy Direct Upload

If you want to keep everything on GoDaddy without Vercel:

**1. GoDaddy Hosting**
- You may already have hosting bundled with the domain
- GoDaddy → My Products → check for Web Hosting
- If not, cPanel hosting starts ~$6/mo

**2. Upload via File Manager or FTP**
- Upload all files from `~/buypablo.com/` (except `references/`, `CLAUDE.md`, `.git/`, `screenshots/`)
- Put them in `public_html/` (GoDaddy's web root)

**3. DNS should already work** since the domain is on GoDaddy

## Email: info@buypablo.com

The site CTA says `info@buypablo.com`. The current "Coming Soon" page shows `orders@buypablo.com`. Options:

1. **GoDaddy Email Forwarding** (free with domain) — forward info@buypablo.com to Alex's personal email
2. **Google Workspace** ($6/user/mo) — full inbox at info@buypablo.com
3. **Zoho Mail** (free for 1 user) — lightweight alternative

Minimum viable: GoDaddy email forwarding. Takes 2 minutes in the GoDaddy dashboard.

## Files to Exclude from Deploy

These files should NOT be uploaded to the live site:
- `CLAUDE.md`
- `DEPLOY.md`
- `references/` (entire directory)
- `screenshots/` (if exists)
- `.git/`
- Any `.md` files in root
- `Module 5 - Content*` (unrelated course file)

## Post-Deploy Checklist
- [ ] https://buypablo.com loads (not "Coming Soon")
- [ ] Age gate works (Yes → site, No → Google)
- [ ] All 7 flavor bands render with correct colors
- [ ] Product images rotate (hero + product cards)
- [ ] Mobile hamburger menu works
- [ ] info@buypablo.com receives mail
- [ ] OG tags work (paste URL in iMessage/Slack to preview)
- [ ] experience.html accessible from nav
