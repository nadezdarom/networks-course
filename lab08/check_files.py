import sys

if len(sys.argv) != 3:
    print("Usage: filename1 filename2")
    sys.exit(1)

file_name1 = sys.argv[1]
file_name2 = sys.argv[2]

try:
    f1 = open(file_name1, 'rb')
except:
    print(f"{file_name1} does not exist")
    sys.exit(1)

try:
    f2 = open(file_name2, 'rb')
except:
    print(f"{file_name2} does not exist")
    sys.exit(1)

file_data1 = f1.read()
f1.close()
file_data2 = f2.read()
f2.close()

if file_data1 == file_data2:
    print("Success! Files mathced")
else:
    print("Files did not match")