import os

file_path = r'e:\University Files\SEM - 5\EE354 Power Engineering\EE-354 Power Engineering\IEEE-9-bus-system-\Report\9bus.jpg'

if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    exit(1)

with open(file_path, 'rb') as f:
    header = f.read(10)
    print(f"Header bytes: {header.hex()}")

    if header.startswith(b'\xff\xd8'):
        print("Format: JPEG")
    elif header.startswith(b'\x89PNG\r\n\x1a\n'):
        print("Format: PNG")
    elif header[:4] == b'RIFF' and header[8:12] == b'WEBP':
        print("Format: WEBP")
    else:
        print("Format: Unknown")
