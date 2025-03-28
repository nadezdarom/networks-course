from ftplib import FTP
import sys, os

ftp = FTP()
ftp.connect("ftp.dlptest.com", 21)
ftp.login("dlpuser", "rNrKYTX9g7z3RgJRmxWuGHbeu")
print(ftp.getwelcome())

if len(sys.argv) == 1:
    ftp.quit()
    print("\n".join([
        "Usage:",
        "client.py -ls -- Достать все файлы и директории в данной папке",
        "client.py -get [filename] -- Скачать файл",
        "client.py -put [filename] -- Загрузить файл"
    ]))
    sys.exit(1)

if sys.argv[1][1:] == "ls":
    if len(sys.argv) > 2:
        ftp.quit()
        print("Usage: client.py -ls")
        sys.exit(1)
    
    for obj in ftp.nlst():
        print(obj)

elif sys.argv[1][1:] == "get":
    if len(sys.argv) <= 2:
        ftp.quit()
        print("Usage: client.py -get [filename]")
        sys.exit(1)
    
    filename = sys.argv[2]
    
    with open(filename, 'wb') as f:
        ftp.retrbinary(f'RETR {filename}', f.write)

    print(f"File {filename} was successfully downloaded")

elif sys.argv[1][1:] == "put":
    if len(sys.argv) <= 2:
        ftp.quit()
        print("Usage: client.py -get [filename]")
        sys.exit(1)

    filename = sys.argv[2]

    if not os.path.exists(filename):
        print(f"File {filename} does not exist")
        ftp.quit()
        sys.exit(1)

    with open(filename, 'rb') as f:
        ftp.storbinary(f'STOR {filename}', f)
    print(f"File {filename} was successfully uploaded")

else:
    print(f"Unknown action: {sys.argv[1]}")
    ftp.quit()
    sys.exit(1)

ftp.quit()
