 import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(to_email, subject, message):
    # Informasi akun email pengirim
    from_email = "khildatulinayah1988@gmail.com"
    from_password = 'ltkc urvx wcai vyrx'

    # Mengatur server SMTP Gmail
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Membuat pesan email
    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject

    # Menambahkan pesan email ke dalam badan email
    msg.attach(MIMEText(message, "plain"))

    try:
        # Koneksi ke server SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Mengamankan koneksi
        server.login(from_email, from_password)  # Login ke akun pengirim

        # Mengirim email
        server.sendmail(from_email, to_email, msg.as_string())
        print("Email berhasil dikirim!")

    except Exception as e:
        print(f"Gagal mengirim email: {e}")
    
    finally:
        server.quit()

# Penggunaan fungsi
recipient = "sadiyah.rpl@gmail.com"
subject = "khildatulinayah/14"
message = "ini adalah pengirim email otomatis menggunakan python"

send_email(recipient, subject, message)