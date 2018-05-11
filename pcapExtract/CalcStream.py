#!/c/ProgramData/Anaconda3/envs/tensorflow/python/bin/python

from scapy.all import *
FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80

pcaps = rdpcap("./input2.pcap")

src_dst = {}
syn = 0
fin = 0

for packet in pcaps:
    src = packet.src
    dst = packet.dst
    # print(src, dst)
    if src not in src_dst.keys():
        src_dst[src] = defaultdict(list)
    f = packet['TCP'].flags
    if f & FIN:
        if src == "00:05:5d:21:99:4c" and dst == "00:21:6a:5b:7d:4a":
            fin += 1
        src_dst[src][dst].append(('fin', packet.time))
    if f & SYN:
        if src == "00:05:5d:21:99:4c" and dst == "00:21:6a:5b:7d:4a":
            syn += 1
        src_dst[src][dst].append(('syn', packet.time))
print(syn, fin)
print(src_dst["00:05:5d:21:99:4c"]["00:21:6a:5b:7d:4a"])