#!/usr/bin/python

# Decoded output form for HIT packets out of the GBT decoder
# header
# strip data
# slope data 

# Order of operations:
# split data into groups of 16 bits
# subtract offsets, assuming data is ordered
# decode strip into vmm, channel using "remapping" 

# A.Wang, last edited Oct 17, 2016


import sys, getopt,binstr


def main(argv):
    remapflag = 0
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:r", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'decodeHIT_32bit.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'decodeHIT_32bit.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt == '-r':
            remapflag = 1

    datafile = open(inputfile, 'r')
    decodedfile = open(outputfile, 'w')

    eventnum = 0
    n = 5 #starting pt of data
    lines = []
    hits = []
    strips = [] #raw strip number after offsets
    rawvmms = [] #vmm number without remapping
    vmms = [] #vmm number after remapping
    chs = [] #channel number
    geoplanes = [] #after remapping, the supposed board number (with mod 8)
    remapping = [11, 10, 9, 8, 15, 14, 13, 12, 3, 2, 1, 0, 7, 6, 5, 4, 27, 26, 25, 24, 31, 30, 29, 28, 19, 18, 17, 16, 23, 22, 21, 20]
    offsets = ["856","85B","84A","84F","84A","84F","856","85B"]
#    offsets = ["84F","84A","856","85B","85B","856","84F","84A"]
    overall_offset = "C00"
    for line in datafile:
        lines.append(line[:len(line)-1])
        if len(lines) == 9: # groups of 9
            print lines
#            strobe = ''.join(map(str,lines))
            header = lines[0] #contains constants + BCID
            bcid = header[4:]
            for i in range(4):
                hits.append(lines[i+1])
            iplane = 0
            for hit in hits:
                strip = int(hit[0:4],16)-int(overall_offset,16)-int(offsets[iplane],16)
                strips.append(strip)
                if strip is not 0:
                    rawvmms.append(strip/64)
                    if remapflag == 1:
                        ivmm = remapping[strip/64]%8
                        igeoplane = remapping[strip/64]/8
                    else:
                        ivmm = (strip/64)%8
                        igeoplane = (strip/64)/8
                    ich = strip%64+1
                    iplane = iplane + 1
                    vmms.append(ivmm)
                    chs.append(ich)
                    geoplanes.append(igeoplane)
                else:
                    iplane = iplane + 1
                    rawvmms.append(0)
                    vmms.append(0)
                    chs.append(0)
                    geoplanes.append(0)
                strip = int(hit[4:],16)-int(overall_offset,16)-int(offsets[iplane],16)
                strips.append(strip)
                if strip is not 0:
                    rawvmms.append(strip/64)
                    if remapflag == 1:
                        ivmm = remapping[strip/64]%8
                        igeoplane = remapping[strip/64]/8
                    else:
                        ivmm = (strip/64)%8
                        igeoplane = (strip/64)/8
                    ich = strip%64+1
                    iplane = iplane + 1
                    vmms.append(ivmm)
                    chs.append(ich)
                    geoplanes.append(igeoplane)
                else:
                    iplane = iplane + 1
                    rawvmms.append(0)
                    vmms.append(0)
                    chs.append(0)
                    geoplanes.append(0)
            decodedfile.write('\n' + str(header)\
                              + " BCID: " + str(int(bcid,16)))
            for ib in range(8):
                decodedfile.write('\n' + str(vmms[ib]) + ' ' + str(chs[ib]))
            lines = []
            hits = []
            strips = []
            vmms = []
            chs = []
            geoplanes = []
#            break
    decodedfile.close()
    datafile.close()
    print "done decoding, exiting \n"
    

if __name__ == "__main__":
    main(sys.argv[1:])
