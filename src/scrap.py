import json

def extract(target):
    data = []
    path = 'conf.json'
    with open(path, 'r') as f:
        data = json.load(f)
    if target == 'box':
        box_dims = data['box']
        x_min = box_dims['x_min']
        y_min = box_dims['y_min']
        x_max = box_dims['x_max']
        y_max = box_dims['y_max']
        return (x_min, y_min, x_max, y_max)

