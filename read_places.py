import json


def get_places() -> {}:
    with open('data/places.json', encoding='utf-8') as f:
        data = json.load(f)
        return data


if __name__ == '__main__':
    data_json = get_places()
    for data in data_json['list']['resources']:
        print(data)
