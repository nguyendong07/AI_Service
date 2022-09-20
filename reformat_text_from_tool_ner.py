import json

data = []
with open('all.txt', encoding='utf-8') as f:
    for line in f:
        a = line
        data.append(json.loads(a))


def extract_text(dic):
    rs = []
    sentence = dic["text"]
    label_tagged = dic["entities"][0]['label']
    start = dic["entities"][0]['start_offset']
    end = dic["entities"][0]['end_offset']
    word_entities = sentence[start:end]
    list_words = sentence.split()
    for word in list_words:
        if word == word_entities:
            label = label_tagged
        else:
            label = 'O'
        s = {"word": word, "label": label}
        rs.append(s)
    return rs


f = open("data_train.conll", "w", encoding='utf-8')

for list_items in data:
    _item = extract_text(list_items)
    for item in _item:
        print(item["word"])
        f.write(item["word"] + " " + item["label"])
        f.write('\n')
    f.write('\n')

f.close()
