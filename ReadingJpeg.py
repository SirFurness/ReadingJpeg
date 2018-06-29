from utils import *
from DQT import readDQT
from SOF0 import readSOF0

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

    quantizationTables = []

    while True:
        expect(file.read(1), b'\xff', "First marker byte")

        markerName = getMarker(file.read(1))
        print(markerName)

        info = getattr(sys.modules[__name__], "read" + markerName)(file)

        if markerName == "DQT":
            quantizationTables.extend(info)

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


