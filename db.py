import json

def readDB(filename = "db.json") :
    with open(filename, mode = 'r') as jsonFile :
        data = json.load(jsonFile)
        jsonFile.close()

    return  data


def writeDB(obj, filename = "db.json") :
    with open(filename, mode = "w") as jsonFile: 
        jsonFile.write(json.dumps(obj))
        jsonFile.close()