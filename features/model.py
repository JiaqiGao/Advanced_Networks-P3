import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from typing import List
import csv

# our original data
# test_data = ['day3-parsed-ondevice.csv']

# community data
# test_data = ['day_3_parsedTLS.csv']

# our new data
test_data = ['day-3-parsed-ondevice-jl.csv']

# our original data
# train_data = ['day1-parsed-ondevice.csv', 'day2-parsed-ondevice.csv']

# community data
# train_data = ['day_1_parsedTLS.csv', 'day_2_parsedTLS.csv']

# our new data
train_data = ['day-1-parsed-ondevice-jl.csv', 'day-2-parsed-ondevice-jl.csv']


# Number of consecutive packets with direction '1'
def get_burst(trace):
    results = [0, 1]  # [total number, max]
    record = []
    count = 1
    direction = trace[0][2]
    for t in trace[1:]:
        if t[2] == direction:
            count += 1
            if count > results[1]:
                results[1] = count
        else:
            results[0] += 1
            record.append(count)
            count = 1
    results.append(sum(record)/float(len(record)))
    return results

def getUniquePacketLengths(trace):
    counts = [0]*3000
    for i in trace:
        try:
            counts[int(i[3])] = 1
        except:
            pass
    
    # Overfitting
    # most_common = counts[0]
    # for i in range(0, 10000):
    #     if most_common < counts[i]:
    #         most_common = i+1
    return counts

# def cumul_sums(trace):
#     num_packets = len(trace)
#     packets_per_division = num_packets // 100
#     return

def parse_trace(trace):
    feats = []
    
    # Number of packets
    num_packets = len(trace)
    feats.append(num_packets)

    # Total time
    total_time = float(trace[-1][1]) - float(trace[0][1])
    feats.append(total_time)

    # Fraction of packets incoming
    incoming_packets = len([x for x in trace if x[2]=='1'])/num_packets
    feats.append(incoming_packets)
    
    # Number of burst, Maximum burst, Mean burst
    burst_results = get_burst(trace)
    feats += burst_results
    
    # Unique packet lengths
    feats += getUniquePacketLengths(trace)

    # cumul_sums(trace)

    return feats


def extract_features(data_files: List[str]):
    X = []
    Y = []
    for f in data_files:
        with open('../parsed_data/' + f) as data:
            r = csv.reader(data)
            next(r)
            current_site = None
            current_trace = []
            for row in r:
                if row[0] != current_site:
                    if current_trace:
                        X.append(parse_trace(current_trace))
                        Y.append(current_site)
                        current_trace = []
                    current_site = row[0]
                current_trace.append(row) 
            X.append(parse_trace(current_trace))
            Y.append(current_site)
    return X, Y

websites = ["cnn", "dropbox", "etsy", "facebook", "homedepot", "hulu", "imgur", "instructure", "irs", "linkedin", "nytimes", "okta", "quizlet", "reddit", "salesforce", "stackoverflow", "wikipedia", "yahoo", "youtube"]

def extract_features_sniffer(directory: str):
    X = []
    Y = []
    for w in websites:
        for i in range(1, 3):
            with open(f'../{directory}/{w}-{i}-processed.csv') as data:
                r = csv.reader(data)
                next(r)
                current_trace = []
                for row in r:
                    current_trace.append(row[1:])
                X.append(parse_trace(current_trace))
                Y.append(w)
    return X, Y

X, Y = extract_features(train_data)
model = RandomForestClassifier(n_jobs=2, n_estimators=100, oob_score=True)
model.fit(X, Y)

print('train complete')

# on device test
test_X, test_Y = extract_features(test_data)

# sniffer test
s_test_X, s_test_Y = extract_features_sniffer('Parsed Data (Sniffer)')

on_device_score = model.score(test_X, test_Y)

pred_Y = model.predict(test_X)

print("On Device Prediction Score: ", on_device_score)

sniffer_score = model.score(s_test_X, s_test_Y)

sniffer_pred_Y = model.predict(s_test_X)

print("Sniffer Prediction Score: ", sniffer_score)

total = len(s_test_Y)
correct = 0

errors = {}
for i in range(len(s_test_Y)):
    if sniffer_pred_Y[i] == s_test_Y[i]:
        correct += 1
    else:
        code = sniffer_pred_Y[i]+":"+s_test_Y[i]
        if not(code in errors):
            errors[code] = 1
        else:
            errors[code] += 1

errors_list = sorted(errors.items(), key=lambda x: x[1], reverse=True)

print("Top three wrong predictions (SNIFFER) (prediction, actual, count)")
for i in range(3):
    print(errors_list[i][0].split(":") + [errors_list[i][1]])


