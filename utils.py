import sys

def expect(given, expected, message):
    if not given == expected:
        print("Error: " + message)
        print("Given: " + str(given))
        print("Expected: " + str(expected))
        sys.exit(1)

def skipBytes(file, numBytes):
    file.read(numBytes)

def getInt(file, numBytes, order='big'):
    return int.from_bytes(file.read(numBytes), byteorder=order)

def getIdentifier(file):
    identifier = file.read(4).decode("ascii")
    #read the null terminator
    skipBytes(file, 1)
    return identifier

def getLength(file):
    return getInt(file, 2)-2

