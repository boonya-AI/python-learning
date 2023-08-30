
def create(path,content):
    file = open(path,'w')
    file.write(content)
    file.close()
def read(path):
    file = open(path)
    return file.read()
def readAsString(path):
    return open(path).read()

# def readContentAsBytes(path):
#     return open(path).read(N)
def readAsList(path):
    return open(path).readlines()

def readAsText(path):
    return open(path).readline()