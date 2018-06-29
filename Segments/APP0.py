from utils import *

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
