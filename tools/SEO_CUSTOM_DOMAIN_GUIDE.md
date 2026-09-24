# SEO + Custom Domain Setup for GitHub Pages

## Primary domain

- Production landing page: https://victorkipruto.com/
- GitHub Pages origin: https://victorkipruto.com/

## Canonical strategy

The canonical, preferred production URL is:

- https://victorkipruto.com/

The GitHub Pages origin is kept operational for hosting, but it is not used as the canonical SEO URL.

## DNS records

For the apex/root domain, add these A records at the domain registrar or DNS provider:

```dns
A    @    185.199.108.153
A    @    185.199.109.153
A    @    185.199.110.153
A    @    185.199.111.153
```

If you choose to support the www subdomain, add:

```dns
CNAME    www    victor-kipruto-rop.github.io
```

Do not add conflicting records. DNS propagation can take several minutes to hours.

## Google Search Console setup

### Step 1
Open Google Search Console.

### Step 2
Add a Domain property for:

```text
victorkipruto.com
```

### Step 3
Google will provide a DNS TXT verification record.

### Step 4
Add the TXT record to your DNS provider exactly as Google provides.

Example format:

```text
google-site-verification=XXXXXXXX
```

### Step 5
Verify the domain in Search Console.

### Step 6
Submit the sitemap:

```text
https://victorkipruto.com/sitemap.xml
```

### Step 7
Use URL Inspection to verify the homepage:

```text
https://victorkipruto.com/
```

### Step 8
Request indexing for the homepage and key pages if needed.

> Do not hardcode Google verification information into the website source. The verification token is only added to DNS.

## GitHub Pages configuration

1. In the repository settings, confirm GitHub Pages is enabled.
2. Ensure the custom domain is set to `victorkipruto.com`.
3. Enforce HTTPS for GitHub Pages once the certificate is issued.
4. Keep the repository root containing `CNAME`, `robots.txt`, `sitemap.xml`, and the site assets.

## Production SEO checklist

- Custom domain canonical URL is https://victorkipruto.com/
- robots.txt points to https://victorkipruto.com/sitemap.xml
- sitemap.xml contains only canonical domain URLs
- page metadata uses custom-domain URLs
- Open Graph and Twitter metadata use custom-domain URLs
- structured data uses the custom domain and a real Person profile
- Google Search Console is configured via the domain property and DNS TXT verification

## Search Console indexing note

Google indexing is not immediate. The site is prepared for crawling with canonical signals, a clean sitemap, and a verified custom domain, but crawl/index timing depends on Google’s discovery and indexing process.
