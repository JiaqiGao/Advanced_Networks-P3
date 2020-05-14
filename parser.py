import os
import csv

MAC_ADDR = 'b7:52:73'

def parse_sniffer_data():
    for d in os.listdir('sniffer'):
        with open(d + "-parsed-sniffer.csv", 'w') as writeto:
            w = csv.writer(writeto)
            for f in os.listdir('sniffer/' + d):
                with open('sniffer/' + d + '/' + f) as csvfile:
                    r = csv.reader(csvfile)
                    for row in r:
                        if MAC_ADDR in str.lower(row[2]):
                            direction = 1
                        elif MAC_ADDR in str.lower(row[3]):
                            direction = 0
                        else:
                            continue
                        time = row[1]
                        packet_size = row[5]
                        w.writerow(['2', time, direction, packet_size])

def parse_trace_data():
    for d in os.listdir('trace'):
        with open(d + "-parsed-ondevice.csv", 'w') as writeto:
            w = csv.writer(writeto)
            for f in os.listdir('trace/' + d):
                with open('trace/' + d + '/' + f) as csvfile:
                    r = csv.reader(csvfile)
                    for row in r:
                        if '192.168' in row[2]:
                            direction = 1
                        elif '192.168' in row[3]:
                            direction = 0
                        else:
                            continue
                        time = row[1]
                        packet_size = row[5]
                        w.writerow(['2', time, direction, packet_size])

parse_sniffer_data()
parse_trace_data()
            