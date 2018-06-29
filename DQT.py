from utils import *

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

    precision = bitsToInt(bits[:4])
    if not precision == 0:
        precision = 1

    destination = bitsToInt(bits[4:])
    if destination == 0:
        destination = "luminance"
    elif destination == 1:
        destination == "chrominance"
    else:
        expect(destination, 1, "Destination is not 1 or 0")

    return (precision, destination)

def readDQT(file):
    length = getLength(file)

    numTables = int((length-1)/64)

    tablesAsLists = []
    for currentTable in range(numTables):

        precision, destination = getDQTInfo(file)

        tablesAsLists.append({"destination": destination, "list": []})
        for currentByte in range(64):
            tablesAsLists[currentTable]["list"].append(getInt(file, precision+1))

    return tablesAsLists

