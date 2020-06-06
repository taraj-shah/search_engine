from indexer import *

if __name__ == "__main__":
    partialIndexPath = "partialIndex/"
    fullIndexPath = "mergeIndex/"
    numPartials = 5

    print("Beginning index merge operation . . .")

    mergeIndex(partialIndexPath, fullIndexPath, numPartials)
