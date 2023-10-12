import jsonpath


def findone(data, path):
    return jsonpath.match(path, data).obj
