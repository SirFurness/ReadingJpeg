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

def readAPP0(file):
    expect(file.read(1), b'\xff', "APP0 first byte")
    expect(file.read(1), b'\xe0', "APP0 second byte")

    length = getLength(file)

    expect(getIdentifier(file), "JFIF", "JFIF identifier")

    majorVersion = getInt(file, 1)
    minorVersion = getInt(file, 1)

    expect(majorVersion, 1, "JFIF version 1.x")

    #skip the thumbnail info
    skipBytes(file, length-7)

    return True

def readSOI(file):
    expect(file.read(1), b'\xff', "SOI first byte")
    expect(file.read(1), b'\xd8', "SOI second byte")

def getBitsFromInt(number):
    numberToAnd = 128
    bits = []
    for i in range(8):
        bits.append(number & numberToAnd)
        numberToAnd/2
    return bits

def readDQT(file):
    length = getInt(file, 2)

    info = getInt(file, 1)
    bits = getBitsFromInt(info)
    print(bits)
    sys.exit()

def readMarkerSegments(file):
    readSOI(file)
    readAPP0(file)

    while True:
        expect(file.read(1), b'\xff', "First marker byte")
        markerName = getMarker(file.read(1))
        getattr(sys.modules[__name__], "read" + markerName)(file)

def getMarker(byte):
    markers = {
        #already handled: b'\xe0': 'APP0', # JFIF APP0
        b'\xc0': 'SOF0', # Start Of Frame
        b'\xc1': 'SOF1',
        b'\xc4': 'DHT',  # Define Huffman Table
        b'\xdb': 'DQT',  # Define Quantization Table
        b'\xda': 'SOS',  # Start Of Scan
        b'\xdd': 'DRI',  # Define Restart Interval
        b'\xd9': 'EOI'   # End Of Image
    }
    return markers[byte]

if __name__ == "__main__":
    filename = input("Input jpeg/jpg file name: ")

    with open(filename, "rb") as file:
        readMarkerSegments(file)


