import json

d = {
    'enemyList': [
        (866, 247, 'Attaker'),
        (866, 287, 'Attaker'),
        (866, 327, 'Attaker'),
        (900, 287, 'Defender')

    ],
    'money': 600
}
text = json.dumps(d)
with open(r'D:\!PycharmProjects\!PrimitiveWar2\data\level2.json', 'w') as f:
    f.write(text)
    f.write('\n')
