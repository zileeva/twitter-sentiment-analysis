# Read from file and extract neutral sentences
with open('../dataset/sets/amazon_cells_labelled.txt') as amazon, open('../dataset/sets/imdb_labelled.txt') as imdb, open('../dataset/sets/yelp_labelled.txt') as yelp:
    neutrals = []
    positives = []
    negatives = []

    for line in amazon:
        if line[-2:-1] == '2':
            neutrals.append(line)
        if line[-2:-1] == '1':
            positives.append(line)
        if line[-2:-1] == '0':
            negatives.append(line)

    for line in imdb:
        if line[-2:-1] == '2':
            neutrals.append(line)
        if line[-2:-1] == '1':
            positives.append(line)
        if line[-2:-1] == '0':
            negatives.append(line)

    for line in yelp:
        if line[-2:-1] == '2':
            neutrals.append(line)
        if line[-2:-1] == '1':
            positives.append(line)
        if line[-2:-1] == '0':
            negatives.append(line)

# Write into neutral file
neutral_file = open("../dataset/neutrals.txt", "w")
positive_file = open("../dataset/positives.txt", "w")
negative_file = open("../dataset/negatives.txt", "w")

# Neutrals
for sentence in neutrals:
    neutral_file.write(sentence)
neutral_file.close()

# Positives
for sentence in positives:
    positive_file.write(sentence)
positive_file.close()

# Negatives
for sentence in negatives:
    negative_file.write(sentence)
negative_file.close()
