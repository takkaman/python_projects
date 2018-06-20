#!/c/ProgramData/Anaconda3/envs/tensorflow/python/bin/python

from scapy.all import *
import traceback

FIN = 0x01
SYN = 0x02
RST = 0x04
PSH = 0x08
ACK = 0x10
URG = 0x20
ECE = 0x40
CWR = 0x80

# pcaps = rdpcap("./tcpopt1.pcap")
file_list = ["./input2.pcap"]
pkt_size = {}
pkt_time = {}
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
ttl_size = 0
ttl_time = 0
min_rate = 99999999
min_srate = 99999999
min_lrate = 99999999

max_rate = 0
max_srate = 0
max_lrate = 0

i = -1
with open('short_time.txt', 'w') as fp_st, open('long_time.txt', 'w') as fp_lt, open('short_rate.txt', 'w') as fp_sr, open('long_rate.txt', 'w') as fp_lr:
    for file_name in file_list:
        print("Processing file ", file_name)
        # fp.write("Processing file "+file_name+"\n")
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
                if ip_tuple not in pkt_size.keys():
                    pkt_size[ip_tuple] = {}
                    pkt_size[ip_tuple1] = {}
                    pkt_time[ip_tuple] = {}
                    pkt_time[ip_tuple1] = {}

                if port_tuple1 not in pkt_size[ip_tuple1].keys():
                    pkt_size[ip_tuple1][port_tuple1] = 0
                    pkt_time[ip_tuple1][port_tuple1] = 0
                if port_tuple not in pkt_size[ip_tuple].keys():
                    pkt_size[ip_tuple][port_tuple] = 0
                    pkt_time[ip_tuple][port_tuple] = 0

                f = packet['TCP'].flags

                if f & FIN:
                    if pkt_time[ip_tuple][port_tuple] == 0: continue
                    # print(packet.time, pkt_time[ip_tuple][port_tuple])
                    delta_t = float(packet.time) - pkt_time[ip_tuple][port_tuple]
                    ttl_time += delta_t
                    pkt_size[ip_tuple1][port_tuple1] += float(packet['IP'].ttl)
                    pkt_size[ip_tuple][port_tuple] += float(packet['IP'].ttl)
                    ttl_size += float(packet['IP'].ttl)
                    rate = float(pkt_size[ip_tuple][port_tuple] / delta_t)
                    if rate > max_rate:
                        max_rate = rate
                    if rate < min_rate:
                        min_rate = rate

                    print("FIN {0}, {1:.3f}, {2:.3f}".format(ip_tuple, delta_t, rate))
                    if delta_t > 1000:
                        fp_lt.write("{0}, {1:.3f}\n".format(ip_tuple, delta_t))
                        fp_lr.write("{0}, {1:.3f}\n".format(ip_tuple, rate))
                        if rate > max_lrate:
                            max_lrate = rate
                        if rate < min_lrate:
                            min_lrate = rate
                    else:
                        fp_st.write("{0}, {1:.3f}\n".format(ip_tuple, delta_t))
                        fp_sr.write("{0}, {1:.3f}\n".format(ip_tuple, rate))
                        if rate > max_srate:
                            max_srate = rate
                        if rate < min_srate:
                            min_srate = rate
                    pkt_size[ip_tuple][port_tuple] = 0
                    pkt_size[ip_tuple1][port_tuple1] = 0
                    pkt_time[ip_tuple][port_tuple] = 0
                    pkt_time[ip_tuple1][port_tuple1] = 0

                if f & SYN:
                    # print("SYN ", float(packet.time))
                    pkt_size[ip_tuple][port_tuple] += float(packet['IP'].ttl)
                    pkt_size[ip_tuple1][port_tuple1] += float(packet['IP'].ttl)
                    ttl_size += float(packet['IP'].ttl)
                    pkt_time[ip_tuple][port_tuple] = float(packet.time)
                    pkt_time[ip_tuple1][port_tuple1] = float(packet.time)

            except Exception as e:
                pass
                # print(traceback.print_exc())
        print("Processing file "+file_name+" finished!")
        # fp.write("Processing file "+file_name+" finished!\n")
    fp_lr.close()
    fp_sr.close()
    fp_lt.close()
    fp_st.close()

avg_rate = float(ttl_size / ttl_time)

with open("avg_rate.txt", "w") as fp_avg, open("max_rate.txt", "w") as fp_max, open("min_rate.txt", "w") as fp_min:
    print("avg: {0:.2f}, max: {1:.2f}, min: {2:.2f}".format(avg_rate, max_rate, min_rate))
    fp_avg.write("{0:.2f}".format(avg_rate))
    fp_max.write("{0:.2f}".format(max_rate))
    fp_min.write("{0:.2f}".format(min_rate))

with open("min_srate.txt", "w") as fp_smin, open("max_srate.txt", "w") as fp_smax, open("min_lrate.txt", "w") as fp_lmin, open("max_lrate.txt", "w") as fp_lmax:
    fp_smin.write("min short rate: {0:.2f}".format(min_srate))
    fp_lmin.write("min long rate: {0:.2f}".format(min_lrate))
    fp_smax.write("max short rate: {0:.2f}".format(max_srate))
    fp_lmax.write("max long rate: {0:.2f}".format(max_lrate))


