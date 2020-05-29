import numpy as np
import argparse
import math
from sklearn.ensemble import RandomForestClassifier
from typing import List
import csv


website_dict = {
    'cnn': 0,
    'dropbox': 1,
    'etsy': 2,
    'facebook': 3,
    'homedepot': 4,
    'hulu': 5,
    'imgur': 6,
    'instructure': 7,
    'irs': 8,
    'linkedin': 9,
    'nytimes': 10,
    'okta': 11,
    'quizlet': 12,
    'reddit': 13,
    'salesforce': 14,
    'stackoverflow': 15,
    'wikipedia': 16,
    'yahoo': 17,
    'youtube': 18,
    'netflix': 19,
    'imdb': 20,
    'ebay': 21,
    'twitch': 22,
    'live': 23
}

website_dict_invert = {
    0 : 'cnn',
    1 : 'dropbox',
    2 : 'etsy',
    3 : 'facebook',
    4 : 'homedepot',
    5 : 'hulu',
    6 : 'imgur',
    7 : 'instructure',
    8 : 'irs',
    9 : 'linkedin',
    10: 'nytimes',
    11: 'okta',
    12: 'quizlet',
    13: 'reddit',
    14: 'salesforce',
    15: 'stackoverflow',
    16: 'wikipedia',
    17: 'yahoo',
    18: 'youtube',
    19: 'netflix',
    20: 'imdb',
    21: 'ebay',
    22: 'twitch',
    23: 'live',
}

# our original data
# test_data = ['day3-parsed-ondevice.csv']

# community data
test_data_community = ['day_3_parsedTLS.csv']

# our new data
test_data_local = ['day_7_parsed_jl.csv', 'day_8_parsed_jl.csv', 'day_9_parsed_jl.csv']

# our original data
# train_data = ['day1-parsed-ondevice.csv', 'day2-parsed-ondevice.csv']

# community data
train_data_community = ['day_1_parsedTLS.csv', 'day_2_parsedTLS.csv']

# our new data
train_data_local = ['day_1_parsed_jl.csv', 'day_2_parsed_jl.csv', 'day_3_parsed_jl.csv', 'day_4_parsed_jl.csv', 'day_5_parsed_jl.csv', 'day_6_parsed_jl.csv']


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
    counts = [0]*1500
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

def parse_trace(trace):
    feats = []
    
    # Number of packets
    num_packets = len(trace)
    feats.append(num_packets)

    # Total time
    total_time = float(trace[-1][1]) - float(trace[0][1])
    feats.append(total_time)

    # Fraction of packets incoming
    incoming_packets = len([x for x in trace if int(float((x[2]))) == 1])/num_packets
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
            next(r)
            current_site = None
            current_trace = []
            for row in r:
                if row[0] != current_site:
                    if current_trace:
                        X.append(parse_trace(current_trace))
                        Y.append(website_dict[current_site])
                        current_trace = []
                    current_site = row[0]
                current_trace.append(row) 
            X.append(parse_trace(current_trace))
            Y.append(website_dict[current_site])
    return X, Y

websites = ["cnn", "dropbox", "etsy", "facebook", "homedepot", "hulu", "imgur", "instructure", 
"irs", "linkedin", "nytimes", "okta", "quizlet", "reddit", "salesforce", "stackoverflow", "wikipedia", "yahoo", "youtube"]

def extract_features_sniffer(directory: str, start=1, stop=3):
    X = []
    Y = []
    for w in websites:
        for i in range(start, stop):
            with open(f'../{directory}/{w}-{i}-processed.csv') as data:
                r = csv.reader(data)
                next(r)
                current_trace = []
                for row in r:
                    current_trace.append(row[1:])
                X.append(parse_trace(current_trace))
                Y.append(website_dict[w])
    return X, Y

def train_model(train_data):
    X, Y = extract_features(train_data)
    model = RandomForestClassifier(n_jobs=2, n_estimators=100, oob_score=True)
    model.fit(X, Y)
    return model

def test_model(model, test_data, sniffer, threshold = .4):
    if sniffer:
        X, Y = extract_features_sniffer(test_data)
    else:
        X, Y = extract_features(test_data)
    score = model.score(X, Y)
    probabilities = model.predict_proba(X)
    predictions = np.argmax(probabilities, axis = 1)

    inconclusive = 0
    correct = 0
    wrong = 0

    total = len(predictions)
    for i in range(total):
        if probabilities[i][predictions[i]] > threshold:
            if model.classes_[predictions[i]] == Y[i]:
                correct += 1
            else:
                wrong += 1
        else:
            inconclusive += 1

    print("Results:")
    print("Raw Prediction Score: ", score)
    print("Prediction Score With Minimum Probability of %f: " % threshold, correct/total)
    print("Portion of Predictions Marked Inconclusive: ", inconclusive/total)
    print("Portion of Predictions Falsely Predicted: ", wrong/total)

    errors = {}
    for i in range(total):
        if model.classes_[predictions[i]] == Y[i]:
            pass
        else:
            code = website_dict_invert[model.classes_[predictions[i]]]+":"+ website_dict_invert[Y[i]]
            if not(code in errors):
                errors[code] = 1
            else:
                errors[code] += 1

    errors_list = sorted(errors.items(), key=lambda x: x[1], reverse=True)

    print("Top three wrong predictions (prediction, actual, count)")
    for i in range(3):
        try:
            print(errors_list[i][0].split(":") + [errors_list[i][1]])
        except:
            pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Arguments for training and testing data")
    parser.add_argument('train', metavar='r', type=int)

    args = parser.parse_args()

    train_str = ""
    if args.train == 0:
        train_data = train_data_local
        train_str = "Local Data"
    else:
        train_data = train_data_community
        train_str = "Community Data"

    print("Beginning Training With %s ...\n" % train_str)

    model = train_model(train_data)

    print('Training Completed')


    print('\nTesting On Device Perfomance with Local Data ...\n')

    test_model(model, test_data_local, False)

    print('\nTesting On Device Performance with Community Data ...\n')

    test_model(model, test_data_community, False)

    print("\nTesting Sniffer Performance ...\n")

    test_model(model, 'Parsed Data (Sniffer)', True)


