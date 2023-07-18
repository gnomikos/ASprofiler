
import ujson as json
import csv

def import_csv(filename):
    try:
        asns = []
        with open(filename, 'r') as fp:
            reader = csv.reader(fp)
            for row in reader:
                asns+=row
        return set([int(asn) for asn in asns])
    except Exception:
        print('Import Error with file:', filename)
        exit()

def import_json(filename):
    try:
        with open(filename, 'r') as fp:
            data = json.load(fp)
        return data
    except Exception:
        print('Import Error with file:', filename)
        exit()

def export_json(data, filename):
    try:
        with open(filename, 'w') as fp:
            json.dump(data, fp)
    except Exception:
        print('Export Error with file:', filename)
        exit()
