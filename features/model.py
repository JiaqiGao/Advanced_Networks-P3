from sklearn.neighbors import KNeighborsClassifier
from typing import List
import csv

test_data = ['day3-parsed-ondevice.csv']
train_data = ['day1-parsed-ondevice.csv', 'day2-parsed-ondevice.csv']


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
    counts = [0]*80000
    for i in trace:
        counts[int(int(i[3]))] += 1
    
    # Overfitting
    # most_common = counts[0]
    # for i in range(0, 10000):
    #     if most_common < counts[i]:
    #         most_common = i+1
    return counts

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

    return feats


def extract_features(data_files: List[str]):
    X = []
    Y = []
    for f in data_files:
        with open('../parsed_data/' + f) as data:
            r = csv.reader(data)
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
    else:
        print("prediction: " + str(pred_Y[i]) + ", Actual: " + str(test_Y[i]))

print("\nRatio of correct predictions: " + str(correct/total))

