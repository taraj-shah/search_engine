from indexer import *

if __name__ == "__main__":
    scoredIndexPath = "scoredIndex/"
    fullIndexPath = "splitIndex/"

    print("Beginning index splitting operation . . .")

    splitIndex(scoredIndexPath, fullIndexPath)
