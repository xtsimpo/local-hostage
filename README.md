# Local Hostage

**A password manager in a single HTML file. For everyone who keeps passwords in Excel.**

Single-file, offline, encrypted. No install, no cloud, no account.

---

## Why

Almost every office has a `passwords.xlsx`.
Because the browser cannot hold everything:

- several accounts on the same platform (admin, personal, reporting)
- several platforms on the same domain (`crm.`, `portal.`, `mail.`)
- things with no URL at all (VPN, Wi‑Fi, desktop apps)
- company laptops where you are not allowed to install anything

Local Hostage is one `.html` file. Double-click it and it works.

## How it works

1. Open `vault.html` in Chrome, Edge or Firefox.
2. Choose a master password.
3. Add entries, or import them from Excel.
4. **Save** (`Ctrl S`): a new `.html` is written that contains the app **and** your encrypted data.

One file, everything inside. Copy it to a USB stick, to your company OneDrive, wherever you like. Without the master password it is useless.

**Chrome / Edge:** on the first save you pick where the file goes. After that it saves automatically on every change.
**Firefox:** every save downloads a new copy. Keep only the latest one.

## Importing from Excel

Three ways in:

- **Paste:** select the cells in Excel, `Ctrl C`, then `Ctrl V` in the import window. The fastest option.
- **`.xlsx` file:** read directly, with a sheet picker.
- **`.csv` file:** detects `,` `;` or tab, and the legacy encodings Excel uses on non-English systems.

Local Hostage guesses what each column is from the headers (English or Greek) or, without headers, from the content (URLs, emails). You confirm or change it, then review before anything is imported.
Rows for the same platform are merged into one entry with a tab per account. Duplicates and rows with no username or password are skipped, and you are told how many.

Old `.xls` files and password-protected workbooks are not supported. Copy and paste works for those.

**After importing, delete the Excel file and empty the recycle bin.**

## Shortcuts

| Key | Action |
|---|---|
| `Ctrl K` or `/` | Search |
| `N` | New entry |
| `Ctrl S` | Save file |
| `Ctrl Enter` | Submit form |
| `Esc` | Close |

## Security

| | |
|---|---|
| Encryption | AES-256-GCM, fresh random IV on every save |
| Key derivation | PBKDF2-SHA256, 600,000 iterations, random 16-byte salt |
| Implementation | The browser's Web Crypto API. No external libraries. |
| Network | Blocked by Content Security Policy (`default-src 'none'`). The page cannot send anything anywhere, even if it wanted to. |
| Scripts | Only its own script runs, pinned by a SHA-256 hash in the CSP. |
| Clipboard | Cleared 20 seconds after copying. |
| Auto-lock | After 5 minutes of inactivity. The key and the decrypted data are dropped from memory. |
| Rendering | Your data is only ever inserted as text, never as HTML. |

### What it does NOT protect against

Let's be honest:

- **Forgotten master password = lost data.** There is no reset, by design.
- **Malware or a keylogger on your computer** sees what you see. No password manager saves you from that.
- **Malicious browser extensions** with access to all pages can read the page while it is unlocked.
- **Old copies** of the file still open with the password they had at the time. If you change your master password, delete the old copies.
- **A tampered file.** Someone with access to your file cannot read your passwords. **They can, however, change the code** so that it captures your master password the next time you type it. So:
  - keep the file in a folder only you control, not on a shared drive others can write to
  - download Local Hostage **only from the official repo**, never from an email, a chat or a colleague's copy
  - if anything on the unlock screen looks different from usual, do not type your password
- **Corrupted data.** If even one character of the encrypted part changes, the file will no longer open (it shows "Wrong master password"). Encryption detects any change, but it cannot repair it. **Always keep a backup.**
- **It is not a team tool.** One file, one person.

If your company already provides a password manager (Bitwarden, 1Password, KeePass), use that. Local Hostage is for when the alternative is Excel.

### Check it yourself

All the code is in one file, around 1,500 lines, with no dependencies. Read it.
Open DevTools, Network tab: you will see zero requests.

## For developers

No build tools, no `npm install`. You edit `vault.html` directly.

After **every** change to the `<script>`:

```bash
python3 build.py
```

It updates the SHA-256 hash in the Content Security Policy. Without it the browser blocks the script and you get a blank page.

**Never commit a file that contains data.** The `vault.html` in the repo must have `null` inside `<script id="vault-data">`. `build.py` warns you if it does not.

### Data format

Inside `<script type="application/json" id="vault-data">`:

```json
{
  "format": "local-hostage", "v": 1,
  "kdf": { "name": "PBKDF2-SHA256", "iter": 600000 },
  "salt": "<base64>", "iv": "<base64>", "ct": "<base64>"
}
```

Vaults saved before the rename carry `"format": "kleidi"` and still open normally.
The ciphertext is bound to the fixed string `kleidi-vault-v1` (AES-GCM additional data). **Never change it**, or every existing vault becomes unreadable.

Decrypted, `ct` is:

```json
{
  "version": 1,
  "entries": [{
    "id": "…", "name": "CRM", "url": "https://crm.example.com/login",
    "tags": ["EU"], "favorite": false,
    "accounts": [{ "id": "…", "label": "Admin", "username": "…", "password": "…", "notes": "…", "changed": 1759140000000 }]
  }]
}
```

## Roadmap

- [x] Encryption, saving into the same file, auto-lock
- [x] Grouping by domain and subdomain
- [x] Multiple accounts per platform
- [x] Password generator, reuse check
- [x] Import from Excel (.xlsx, .csv, paste) with column mapping
- [x] English UI
- [ ] Export to CSV (with an explicit warning)
- [ ] Greek UI as an option
- [ ] Argon2id instead of PBKDF2

## License

MIT
