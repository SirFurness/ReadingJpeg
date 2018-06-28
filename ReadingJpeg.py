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
    length = getLength(file)

    identifier = getIdentifier(file)
    print(identifier)
    if not identifier == "JFIF":
        skipBytes(file, length-5)
        return

    majorVersion = getInt(file, 1)
    minorVersion = getInt(file, 1)

    expect(majorVersion, 1, "JFIF version 1.x")

    #skip the thumbnail info
    skipBytes(file, length-7)

def readSOI(file):
    expect(file.read(1), b'\xff', "SOI first byte")
    expect(file.read(1), b'\xd8', "SOI second byte")

def getBitsFromInt(number):
    numberToAnd = 128
    bits = []
    for i in range(8):
        bits.append(number & numberToAnd)
        numberToAnd = int(numberToAnd/2)
    return bits

def bitsToInt(bits):
    out = 0
    for bit in bits:
        out = (out << 1) | bit
    return out

def getDQTInfo(file):
    infoInt = getInt(file, 1)
    bits = getBitsFromInt(infoInt)
    return (bitsToInt(bits[:4]), bitsToInt(bits[4:]))

def readDQT(file):
    length = getLength(file)

    numTables = int((length-1)/64)

    tablesAsLists = []
    for currentTable in range(numTables):

        precision, destination = getDQTInfo(file)
        if not precision == 0:
            precision = 1
        if destination == 0:
            destination = "luminance"
        elif destination == 1:
            destination = "chrominance"
        else:
            expect(destination, 1, "Destination is not 1 or 0")

        tablesAsLists.append({"destination": destination, "list": []})
        for currentByte in range(64):
            tablesAsLists[currentTable]["list"].append(getInt(file, precision+1))
        return tablesAsLists

def readSOF0(file):
    pass
def readDHT(file):
    pass
def readSOS(file):
    pass
def readDRI(file):
    pass
def readEOI(file):
    pass
def readSOF1(file):
    pass

def readMarkerSegments(file):
    readSOI(file)

    tableQT = []

    while True:
        expect(file.read(1), b'\xff', "First marker byte")

        markerName = getMarker(file.read(1))
        print(markerName)

        info = getattr(sys.modules[__name__], "read" + markerName)(file)

        if markerName == "DQT":
            tableQT.extend(info)

        input("")

def getMarker(byte):
    markers = {
        b'\xe0': 'APP0', # JFIF APP0
        b'\xe1': 'APP0', # JFIF APP1 (I don't what it's for)
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


