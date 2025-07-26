# HTTPS Deployment Guide

## Requirements
- Valid SSL certificate (from Let's Encrypt or other CA)
- Web server configured for HTTPS (Nginx/Apache)
- Django running behind the web server

## Nginx Configuration Example
```nginx
server {
    listen 443 ssl;
    server_name yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
    }
}

server {
    listen 80;
    server_name yourdomain.com;
    return 301 https://$host$request_uri;
}
