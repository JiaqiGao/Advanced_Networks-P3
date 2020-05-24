import os
import csv

MAC_ADDR = 'intelcor_b7:52:73'

website_directory = {
    1: 'youtube',
    2: 'yahoo',
    3: 'facebook',
    4: 'reddit',
    5: 'instructure',
    6: 'stackoverflow',
    7: 'linkedin',
    8: 'irs',
    9: 'nytimes',
    10: 'cnn',
    11: 'salesforce',
    12: 'okta',
    13: 'wikipedia',
    14: 'imgur',
    15: 'dropbox',
    16: 'etsy',
    17: 'hulu',
    18: 'quizlet',
    19: 'homedepot',
    20: 'netflix'
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
                web_index = website_directory[i]
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
    for d in os.listdir('new_data'):
        with open(d + "-parsed-ondevice.csv", 'w') as writeto:
            w = csv.writer(writeto)
            for j in range(1, 11):
                for i in range(1, 21):
                    web_index = website_directory[i]
                    with open('new_data/%s/run%d/packet%d.csv' % (d, j, i)) as csvfile:
                        r = csv.reader(csvfile)
                        for row in r:
                            if 'TLS' in row[4] or 'HTTP' in row[4]:
                                pass
                            else:
                                continue
                            if ip_directory[d] in row[2]:
                                direction = 1
                            elif ip_directory[d] in row[3]:
                                direction = 0
                            else:
                                continue
                            time = row[1]
                            packet_size = row[5]
                            w.writerow([web_index, time, direction, packet_size])

# parse_sniffer_data()
parse_trace_data()
            