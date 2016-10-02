# modified from https://github.com/ZhuangLab/storm-analysis/blob/master/storm_analysis/sa_utilities/read_tagged_spot_file.py

import sys
import struct
import google.protobuf.internal.decoder as decoder
import TSFProto_pb2

if (len(sys.argv)<2):
    print("usage: <tsf file>")
    exit()

tsf_file_path = sys.argv[1]
if len(sys.argv)>2:
    export_file_path = sys.argv[2]
else:
    export_file_path = tsf_file_path + '.csv'

def _getV(fp, format, size):
    return struct.unpack(format, fp.read(size))[0]

tsf_file = open(tsf_file_path, "rb")

# Read magic number and offset
mnumber = _getV(tsf_file, "I", 4)
offset = _getV(tsf_file, ">Q", 8)

print("mnumber:", mnumber)
print("offset:", offset)

# Read SpotList message
tsf_file.seek(offset+12)

buffer = tsf_file.read()
(spot_list_size, position) = decoder._DecodeVarint(buffer, 0)

spot_list = TSFProto_pb2.SpotList()
spot_list.ParseFromString(buffer[position:position+spot_list_size])

print("Spot List:", spot_list_size)
print(spot_list)
print("")

ps = spot_list.pixel_size

header = 'frame,x [nm],y [nm],z [nm],intensity [photon]\n'
f = open(export_file_path, 'w')
f.write(header)

# Export to csv file(for thunderSTORM)
cur_pos = 12
print('exporting...')
for i in range(spot_list_size):
    tsf_file.seek(cur_pos)
    buffer = tsf_file.read(200)
    (spot_size, position) = decoder._DecodeVarint(buffer, 0)
    spot = TSFProto_pb2.Spot()
    spot.ParseFromString(buffer[position:position+spot_size])
    cur_pos += position + spot_size
    line = "{frame:d},{x:.2f},{y:.2f},{z:.2f},{intensity:.2f}\n"
    f.write(line.format(frame=spot.frame,x=spot.x,y=spot.y,z=spot.z,intensity=spot.intensity))
    print(i)
print('done')
tsf_file.close()

#
# The MIT License
#
# Copyright (c) 2013 Zhuang Lab, Harvard University
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
