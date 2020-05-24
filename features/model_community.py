from sklearn.neighbors import KNeighborsClassifier
from typing import List
import csv

test_data = ['day_3_parsed.csv']
train_data = ['day_1_parsed.csv', 'day_2_parsed.csv']


def parse_trace(trace):
    feats = []
    num_packets = len(trace)
    feats.append(num_packets)
    total_time = float(trace[-1]['time']) - float(trace[0]['time'])
    feats.append(total_time)
    for i in range(4):
        if i == 0:
            continue
        feats.append(float(trace[i]['time']) - float(trace[0]['time']))
    incoming_count = 0
    outgoing_count = 0
    for p in trace:
        if p['direction'] == '1':
            outgoing_count += 1
        else:
            incoming_count += 1
    feats.append(outgoing_count)
    feats.append(incoming_count)
    return feats


def extract_features(data_files: List[str]):
    X = []
    Y = []
    for f in data_files:
        with open('../parsed_data/' + f) as data:
            r = csv.DictReader(data)
            current_site = None
            current_trace = []
            for row in r:
                if row['website index'] != current_site:
                    if current_trace:
                        X.append(parse_trace(current_trace))
                        Y.append(current_site)
                        current_trace = []
                    current_site = row['website index']
                current_trace.append(row)  
            X.append(parse_trace(current_trace))
            Y.append(current_site)
    return X, Y

X, Y = extract_features(train_data)
neighbors = KNeighborsClassifier(n_neighbors=20)
neighbors.fit(X, Y)

test_X, test_Y = extract_features(test_data)

pred_Y = neighbors.predict(test_X)

total = len(test_Y)
correct = 0

for i in range(len(test_Y)):
    if pred_Y[i] == test_Y[i]:
        correct += 1

print(correct/total)

