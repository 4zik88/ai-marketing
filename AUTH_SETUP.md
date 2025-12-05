# 🔐 Authentication Setup Guide

This guide explains how to enable HTTP Basic Authentication to protect your AI Marketing application.

## 🎯 Quick Setup on Railway

### Step 1: Enable Authentication

In Railway Dashboard → Your Project → Variables, add:

```env
AUTH_ENABLED=true
AUTH_USERNAME=your_username
AUTH_PASSWORD=your_strong_password_here
```

**Important:** 
- Use a **strong password** (at least 12 characters, mix of letters, numbers, symbols)
- Never commit passwords to Git
- Change default username from "admin"

### Step 2: Redeploy

After adding variables, Railway will automatically redeploy. Your app is now protected! 🔒

## 📋 Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `AUTH_ENABLED` | No | `false` | Set to `true` to enable authentication |
| `AUTH_USERNAME` | Yes* | `admin` | Username for login |
| `AUTH_PASSWORD` | Yes* | (empty) | Password for login |

*Required only if `AUTH_ENABLED=true`

## 🚀 How It Works

When authentication is enabled:
1. **All routes are protected** except `/health` endpoint
2. Browser will show **login popup** when accessing the site
3. User must enter **username** and **password** to access
4. Credentials are checked on every request

## 💡 Examples

### Enable Authentication (Railway)

```env
AUTH_ENABLED=true
AUTH_USERNAME=myuser
AUTH_PASSWORD=MySecurePass123!
```

### Disable Authentication

```env
AUTH_ENABLED=false
# Or simply remove AUTH_ENABLED variable
```

### Local Development

Create `.env` file:

```env
AUTH_ENABLED=true
AUTH_USERNAME=admin
AUTH_PASSWORD=test123
```

## 🔒 Security Best Practices

1. **Use Strong Passwords**
   - Minimum 12 characters
   - Mix of uppercase, lowercase, numbers, symbols
   - Example: `MyApp2024!Secure`

2. **Change Default Username**
   - Don't use "admin" in production
   - Use something unique: `yourname`, `company_name`, etc.

3. **HTTPS Only**
   - Railway provides HTTPS automatically
   - Never use HTTP for authentication

4. **Regular Password Updates**
   - Change password periodically
   - Update in Railway Variables

## 🧪 Testing

### Test Locally

```bash
# Start app
python web_app.py

# Visit http://localhost:8000
# You should see login popup if AUTH_ENABLED=true
```

### Test on Railway

1. Visit your Railway URL
2. Browser should show login dialog
3. Enter username and password
4. Access granted! ✅

## 🆘 Troubleshooting

### "Authentication not working"

- Check `AUTH_ENABLED=true` is set
- Verify `AUTH_PASSWORD` is not empty
- Check Railway logs for errors

### "Can't login"

- Verify username matches `AUTH_USERNAME` exactly
- Check password matches `AUTH_PASSWORD` exactly
- Clear browser cache and try again

### "Want to disable auth temporarily"

Set `AUTH_ENABLED=false` in Railway Variables and redeploy.

## 📝 Notes

- **Health endpoint** (`/health`) is always public (no auth required)
- Authentication uses **HTTP Basic Auth** (standard browser popup)
- Works with all modern browsers
- Credentials are sent with every request (HTTPS recommended)

---

**Your app is now secure! 🔐**

