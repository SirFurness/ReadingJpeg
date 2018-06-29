from utils import *
from Segments.DQT import readDQT
from Segments.SOF0 import readSOF0
from Segments.APP0 import readAPP0

def readSOI(file):
    expect(file.read(1), b'\xff', "SOI first byte")
    expect(file.read(1), b'\xd8', "SOI second byte")

def readUnknown(file):
    skipBytes(file, getLength(file))

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
    try:
        return markers[byte]
    except KeyError:
        print(byte)
        return 'Unknown'

if __name__ == "__main__":
    filename = input("Input jpeg/jpg file name: ")

    with open(filename, "rb") as file:
        readMarkerSegments(file)


