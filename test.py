import json

d = {
    'enemyList': [
        (749, 261, "Attaker"),
        (749, 293, "Attaker"),
        (749, 325, 'Attaker'),
        (780, 232, 'Attaker'),
        (780, 360, 'Attaker')
    ],
    'money': 500
}
text = json.dumps(d)
with open(r'D:\!PycharmProjects\!PrimitiveWar2\data\level1.json', 'w') as f:
    f.write(text)
    f.write('\n')
