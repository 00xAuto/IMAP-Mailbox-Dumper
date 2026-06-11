# IMAP Mailbox Dumper

A Python tool for making life easier when dealing with an IMAP server which will dump the full contents of all mail folders — including headers and body — to stdout. Useful during internal network pentests and CTFs when valid mail credentials are obtained.

## Overview

Once you have credentials for a mail account (via password spray, credential stuffing, OSINT, or prior exploitation), this tool enumerates all IMAP folders and prints every email in a readable format. Particularly effective against internal mail servers running Postfix/Dovecot, Exchange, or similar.

**Demonstrated against:** PG Practice — *Postfish* (192.168.x.x)

## Usage

```bash
python3 imap_dump.py
```

You will be prompted interactively:

```
Target host/IP: <mail server IP or hostname>
Username:       <email username>
Password:       <password>
```

Or call the function directly in a script:

```python
dump_mailbox(host="192.168.1.10", user="user", password="pass")
```

## Example Output

```
[*] Available folders:
    (\HasNoChildren) "/" INBOX

============================================================
[*] Folder: INBOX (1 emails)
============================================================
[1] From   : support@domain.com
     To     : None
     Date   : Wed, 31 Mar 2021 13:11:23 +0000 (UTC)
     Subject: ERP Registration Reminder
     Body   :
Hi team,

We will be .... <email contents>.

Regards,
team.
------------------------------------------------------------
```

## Pentest Notes

### What to look for

| Email Content                        | Next Step                                      |
|--------------------------------------|------------------------------------------------|
| Password reset links                 | Visit link, reset creds, pivot to new service  |
| Internal hostnames / IPs             | Add to scope, enumerate further                |
| Credentials in plaintext             | Credential reuse — try SSH, SMB, web logins    |
| Mentions of IT procedures / software | Research for CVEs, default creds               |
| HR / finance data                    | Document for report, check for PII exposure    |

### In this case

The `support@doamin.com` email hints at upcoming **password reset links** being sent to the sales team. In the context of the box, this is a signal to:

1. Look for a password reset mechanism exposed on the web service.
2. Check if the reset flow can be triggered and intercepted (e.g. via a local mail relay or SSRF).
3. Try credential reuse across other services (SSH, SMB, FTP) with `user:user`.

## Requirements

- Python 3.x
- Standard library only (`imaplib`, `email`)
- Valid IMAP credentials
- Network access to port **993** (IMAP over SSL) on the target

## Operational Notes

- Connects using `IMAP4_SSL` (port 993). To use plaintext IMAP (port 143), swap to `imaplib.IMAP4`.
- Folder names are parsed by splitting on `"/"` delimiter — works for standard Dovecot/Courier layouts. Exotic folder names with spaces or special characters may need quoting.
- Bodies are decoded with `errors='ignore'` — binary attachments are skipped gracefully.
- Errors per-folder are caught and logged without crashing the full dump.

---

⚠️ Disclaimer & Legal Warning

This tool is provided for educational purposes and authorized security testing only.

By using this software, you agree to the following terms:


Authorized Use Only

These tools are intended exclusively for:


Penetration testing on systems you own or have been given explicit written permission to test
Capture The Flag (CTF) challenges and lab environments (e.g. Hack The Box, TryHackMe, PG Practice)
Security research in isolated, controlled environments
Educational study of network protocols and authentication mechanisms



No Responsibility / Liability Waiver

The author(s) of this software accept no responsibility or liability for any damage, data loss, legal consequences, or harm caused by the use or misuse of these tools.

This includes but is not limited to:


Unauthorized access to computer systems or networks
Interception of private communications or data
Violation of local, national, or international law
Any indirect, incidental, or consequential damages arising from use of this software



Legal Notice

Unauthorized use of these tools against systems without explicit permission may violate laws including but not limited to:


Computer Fraud and Abuse Act (CFAA) — United States
Computer Misuse Act 1990 — United Kingdom
Cybercrime laws applicable in your jurisdiction


You are solely responsible for ensuring your use of this software complies with all applicable laws and regulations.
