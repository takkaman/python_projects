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

# pcaps = rdpcap("./tcpopt1.pcap")
file_list = ["./tcpopt1.pcap"]
pkt = {}
non_tcp = 0
syn = 0
fin = 0
long_stream = 0
short_stream = 0
long_stream_count = 0
short_stream_count = 0
long_pcaps = []
short_pcaps = []
pcaps_len = 0
short_index = 1
long_index = 1

i = -1
with open('pcap_read_result.txt', 'w') as fp:
    for file_name in file_list:
        print("Processing file ", file_name)
        fp.write("Processing file "+file_name+"\n")
        myreader = PcapReader(file_name)
        while True:
            packet = myreader.read_packet()
            if packet is None:
                break
            pcaps_len += 1
            try:
                if packet.haslayer("IP") == 0: continue
                if packet['IP'].proto != 6:
                    non_tcp += 1
                    continue
                src_ip = packet['IP'].src
                dst_ip = packet['IP'].dst
                ip_tuple = (src_ip, dst_ip)
                ip_tuple1 = (dst_ip, src_ip)
                src_port = packet['TCP'].sport
                dst_port = packet['TCP'].dport
                port_tuple = (src_port, dst_port)
                port_tuple1 = (dst_port, src_port)
                # print(ip_tuple, port_tuple)
                if ip_tuple not in pkt.keys():
                    pkt[ip_tuple] = {}
                    pkt[ip_tuple1] = {}

                if port_tuple1 not in pkt[ip_tuple1].keys():
                    pkt[ip_tuple1][port_tuple1] = defaultdict(list)
                if port_tuple not in pkt[ip_tuple].keys():
                    pkt[ip_tuple][port_tuple] = defaultdict(list)

                # print("begin", pkt[ip_tuple][port_tuple])
                f = packet['TCP'].flags
                if f & FIN:

                    # if delta> 1000:
                    #     long_stream_count += 1
                    #     long_stream += delta
                    #     long_pcaps.append(syn_pkt)
                    #     long_pcaps.append(packet)
                    # else:
                    #     long_pcaps.append(syn_pkt)
                    #     long_pcaps.append(packet)
                    #     short_stream_count += 1
                    #     short_stream += delta
                    sync_time = -1
                    for time in pkt[ip_tuple][port_tuple]['SYN']:
                        if sync_time == -1:
                            sync_time = time
                        else:
                            if time > sync_time:
                                sync_time = time
                    for time in pkt[ip_tuple1][port_tuple1]['SYN']:
                        if sync_time == -1:
                            sync_time = time
                        else:
                            if time > sync_time:
                                sync_time = time
                    if sync_time == -1: continue
                    delta = float(packet.time)-sync_time
                    # print(packet.time)
                    # print(sync_time)
                    # print("pkt time: %.6f" % packet.time)
                    # print("sync time: %.6f" % sync_time)

                    print("FIN %s %s %.6f" % (ip_tuple, port_tuple, delta))
                    fp.write("FIN %s %s %.6f\n" % (ip_tuple, port_tuple, delta))
                    # print("a")
                    if delta > 10000:
                        long_stream_count += 1
                        long_stream += delta
                        for pkg in pkt[ip_tuple][port_tuple]['PKG']:
                            long_pcaps.append(pkg)
                        for pkg in pkt[ip_tuple1][port_tuple1]['PKG']:
                            long_pcaps.append(pkg)
                        long_pcaps.append(packet)
                        del(pkt[ip_tuple1])
                        del(pkt[ip_tuple])
                        if len(long_pcaps) >= 10000:
                            wrpcap("long_stream_"+str(long_index)+".pcap", long_pcaps)
                            long_index += 1
                            long_pcaps = []
                        print("Found {0} long stream now.".format(long_stream_count))
                        fp.write("Found {0} long stream now.\n".format(long_stream_count))
                    else:
                        # print("b")
                        short_stream_count += 1
                        short_stream += delta
                        for pkg in pkt[ip_tuple][port_tuple]['PKG']:
                            short_pcaps.append(pkg)
                        for pkg in pkt[ip_tuple1][port_tuple1]['PKG']:
                            short_pcaps.append(pkg)
                        short_pcaps.append(packet)
                        del(pkt[ip_tuple][port_tuple])
                        del(pkt[ip_tuple1][port_tuple1])
                        del(pkt[ip_tuple1])
                        del(pkt[ip_tuple])
                        # print(len(short_pcaps))
                        if len(short_pcaps) >= 10000:
                            wrpcap("short_stream_"+str(short_index)+".pcap", short_pcaps)
                            short_index += 1
                            short_pcaps = []
                        # print("1")
                        print("Found {0} short stream with total length now.".format(short_stream_count))
                        # print("2")
                        fp.write("Found {0} short stream with total length now.\n".format(short_stream_count))
                    # pkt[ip_tuple][port_tuple] = defaultdict(list)
                    # pkt[ip_tuple1][port_tuple1] = defaultdict(list)
                    # print("3")
                    # print(pkt[ip_tuple][port_tuple], pkt[ip_tuple1][port_tuple1])
                    # pkt[ip_tuple][port_tuple].append(("FIN", packet.time))
                else:
                    if f & SYN:
                        # print("SYN {0} {1}".format(ip_tuple, port_tuple))
                        # fp.write("SYN {0} {1}\n".format(ip_tuple, port_tuple))
                        pkt[ip_tuple][port_tuple]['SYN'].append(float(packet.time))
                    # print(ip_tuple, port_tuple)
                    # print("before", pkt[ip_tuple])
                    pkt[ip_tuple][port_tuple]['PKG'].append(packet)
                    # print("after", pkt[ip_tuple])
            except Exception as e:
                # pass
                print(e)
        print("Processing file "+file_name+" finished!")
        fp.write("Processing file "+file_name+" finished!\n")


print("Total packages: {0}".format(pcaps_len))
print("Total short stream packages: {0}".format(len(short_pcaps)))
print("Total {0} long stream sessions".format(long_stream_count))
print("Total {0} long stream length".format(long_stream))
print("Total {0} short stream sessions".format(short_stream_count))
print("Total {0} short stream length".format(short_stream))

if long_stream_count > 0:
    wrpcap("long_stream_last.pcap", long_pcaps)
if short_stream_count > 0:
    wrpcap("short_stream_last.pcap", short_pcaps)
# print(syn, fin)
