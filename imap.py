import imaplib
import email
from email.header import decode_header

def dump_mailbox(host, user, password, folder='INBOX'):
    m = imaplib.IMAP4_SSL(host)
    m.login(user, password)
    
    _, folders = m.list()
    print("[*] Available folders:")
    folder_names = []
    for f in folders:
        decoded = f.decode()
        print(f"    {decoded}")
        # Parse folder name after the last delimiter
        folder_name = decoded.split('"/"')[-1].strip().strip('"')
        folder_names.append(folder_name)
    
    for folder_name in folder_names:
        try:
            status, _ = m.select(folder_name)
            if status != 'OK':
                continue

            _, msgs = m.search(None, 'ALL')
            ids = msgs[0].split()
            if not ids:
                continue

            print(f"\\n{'='*60}")
            print(f"[*] Folder: {folder_name} ({len(ids)} emails)")
            print('='*60)

            for num in ids:
                _, data = m.fetch(num, '(RFC822)')
                msg = email.message_from_bytes(data[0][1])

                subject = decode_header(msg['Subject'])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode(errors='ignore')

                print(f"[{num.decode()}] From   : {msg['From']}")
                print(f"     To     : {msg['To']}")
                print(f"     Date   : {msg['Date']}")
                print(f"     Subject: {subject}")

                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == 'text/plain':
                            body = part.get_payload(decode=True).decode(errors='ignore')
                            print(f"     Body   :\\n{body}")
                else:
                    body = msg.get_payload(decode=True).decode(errors='ignore')
                    print(f"     Body   : {body}")
                print("-"*60)

        except Exception as e:
            print(f"[!] Skipping folder '{folder_name}': {e}")
            continue

    m.logout()

if __name__ == '__main__':
    host = input("Target host/IP: ").strip()
    user = input("Username: ").strip()
    password = input("Password: ").strip()
    
    dump_mailbox(host, user, password)
