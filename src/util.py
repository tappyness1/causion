import yaml

def open_yaml_file(fname):
    file_to_open = open(fname)
    cfg = yaml.load(file_to_open, Loader=yaml.FullLoader)
    return cfg