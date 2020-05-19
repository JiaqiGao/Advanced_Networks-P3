import os
import csv

MAC_ADDR = 'intelcor_b7:52:73'

website_directory = {
    1: 'youtube.com',
    2: 'yahoo.com',
    3: 'facebook.com',
    4: 'reddit.com',
    5: 'instructure.com',
    6: 'stackoverflow.com',
    7: 'linkedin.com',
    8: 'irs.gov',
    9: 'nytimes.com',
    10: 'cnn.com',
    11: 'salesforce.com',
    12: 'okta.com',
    13: 'wikipedia.org',
    14: 'imgur.com',
    15: 'dropbox.com',
    16: 'etsy.com',
    17: 'hulu.com',
    18: 'quizlet.com',
    19: 'homedepot.com',
    20: 'netflix.com'
}

ip_directory = {
    'day1': '192.168.1.118',
    'day2': '192.168.1.118',
    'day3': '192.168.1.118'
}

def parse_sniffer_data():
    for d in os.listdir('sniffer'):
        with open(d + "-parsed-sniffer.csv", 'w') as writeto:
            w = csv.writer(writeto)
            for i in range(1, 21):
                w.writerow([website_directory[i]])
                for j in range(1, 11):
                    with open('sniffer/%s/run%d/packet%d.csv' % (d, j, i)) as csvfile:
                        r = csv.reader(csvfile)
                        for row in r:
                            if MAC_ADDR in str.lower(row[2]):
                                direction = 1
                            elif MAC_ADDR in str.lower(row[3]):
                                direction = 0
                            else:
                                continue
                            index = row[0]
                            time = row[1]
                            packet_size = row[5]
                            w.writerow([index, time, direction, packet_size])

def parse_trace_data():
    for d in os.listdir('trace'):
        with open(d + "-parsed-ondevice.csv", 'w') as writeto:
            w = csv.writer(writeto)
            for i in range(1, 21):
                w.writerow([website_directory[i]])
                for j in range(1, 11):
                    with open('trace/%s/run%d/packet%d.csv' % (d, j, i)) as csvfile:
                        r = csv.reader(csvfile)
                        for row in r:
                            if ip_directory[d] in row[2]:
                                direction = 1
                            elif ip_directory[d] in row[3]:
                                direction = 0
                            else:
                                continue
                            time = row[1]
                            index = row[0]
                            packet_size = row[5]
                            w.writerow([index, time, direction, packet_size])

parse_sniffer_data()
parse_trace_data()
            