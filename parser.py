import os
import csv

MAC_ADDR = 'b7:52:73'

website_directory = {
    'youtube': 2,
    'yahoo': 5,
    'facebook': 4,
    'reddit': 7,
    'netflix': 10,
    'ebay': 9,
    'instructure': 11,
    'twitch': 14,
    'live': 16,
    'stackoverflow': 47,
    'linkedin': 34,
    'irs': 28,
    'imdb': 44,
    'nytimes': 26,
    'cnn': 18,
    'salesforce': 40,
    'okta': 49,
    'wikipedia': 6,
    'imgur': 23,
    'dropbox': 29,
    'zillow': 31,
    'etsy': 35,
    'hulu': 37,
    'quizlet': 42,
    'home depot': 45
}

def parse_sniffer_data():
    for d in os.listdir('sniffer'):
        with open(d + "-parsed-sniffer.csv", 'w') as writeto:
            w = csv.writer(writeto)
            for f in os.listdir('sniffer/' + d):
                with open('sniffer/' + d + '/' + f) as csvfile:
                    name = f.split('-')[0]
                    if name in website_directory:
                        index = website_directory[name]
                    else:
                        print("Unknown file name: " + f)
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
                        w.writerow([index, time, direction, packet_size])

def parse_trace_data():
    for d in os.listdir('trace'):
        with open(d + "-parsed-ondevice.csv", 'w') as writeto:
            w = csv.writer(writeto)
            for f in os.listdir('trace/' + d):
                with open('trace/' + d + '/' + f) as csvfile:
                    name = f.split('-')[0]
                    if name in website_directory:
                        index = website_directory[name]
                    else:
                        print("Unknown file name: " + f)
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
            