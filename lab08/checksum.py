import sys


def calculate_checksum(data):
    if len(data) % 2 == 1:
        data += b'\x00'

    checksum = 0
    for i in range(0, len(data), 2):
        checksum += (data[i] << 8 + data[i + 1])
        checksum = (checksum & 0xFFFF) + (checksum >> 16)

    checksum = ~checksum & 0xFFFF
    return checksum


def check_checksum(data, checksum):
    return calculate_checksum(data) == checksum


def test_checksum():
    try:
        f1 = open("test1.txt", 'rb')
    except:
        print(f"File test1.jpg does not exists")
        sys.exit(1)
    

    try:
        f2 = open("test2.txt", 'rb')
    except:
        print(f"File test2.jpeg does not exists")
        sys.exit(1)

    
    test_data1 = f1.read()
    test_data2 = f2.read()

    f1.close()
    f2.close()

    checksum1 = calculate_checksum(test_data1)

    assert check_checksum(test_data1, checksum1), "Test 1 failed"
    assert not(check_checksum(test_data2, checksum1)), "Test 2 failed"

    print("All tests passed")


test_checksum()