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

def getDestination(bits):
    destination = bitsToInt(bits[4:])
    if destination == 0:
        destination = "luminance"
    elif destination == 1:
        destination = "chrominance"
    else:
        expect(destination, 1, "Destination is not 1 or 0")
    return destination

def getPrecision(bits):
    precision = bitsToInt(bits[:4])
    if not precision == 0:
        precision = 1
    return precision

def getDQTInfo(file):
    infoInt = getInt(file, 1)
    bits = getBitsFromInt(infoInt)

    precision = getPrecision(bits)
    destination = getDestination(bits)

    return (precision, destination)

def getQT(file, precision):
    table = []
    for currentByte in range(64):
        table.append(getInt(file, precision+1))
    return table

def readDQT(file):
    length = getLength(file)

    lengthRemaining = length

    tablesAsLists = []
    while not lengthRemaining == 0:
        precision, destination = getDQTInfo(file)
        lengthRemaining -= 1

        tablesAsLists.append({"destination": destination, "list": getQT(file, precision)})

        lengthRemaining -= 64*(precision+1)

    return tablesAsLists

