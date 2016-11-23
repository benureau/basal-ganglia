import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('configfile', type=str)
args = parser.parse_known_args()[0]

with open(args.configfile, 'r', encoding='utf-8') as fp:
    params = json.load(fp)

name  = params['name']
label = params['label']
