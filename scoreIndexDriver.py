import json
import math

if __name__ == "__main__":

    for char in "abcdefghijklmnopqrstuvwxyz0123456789":
        print("scoring '{}'".format(char))
        indexfilename = "mergeIndex/" + char
        indexFile = open(indexfilename, 'r')
        index = json.loads(indexFile.readline())
        indexFile.close()

        
        for tok in index.keys():
            totalOccurrence = 0
            for doc in index[tok].keys():
                positions = index[tok][doc][0]
                docOccurrence = len(positions)
                totalOccurrence += 1
                formattup = (index[tok][doc][1],index[tok][doc][2], index[tok][doc][3],index[tok][doc][4],index[tok][doc][5])

                index[tok][doc] = list([docOccurrence, positions, formattup])

            docids = sorted(list(index[tok].keys()))

            index[tok]["doclist"] = docids
            # print(sorted(list(index[tok].keys())))
            index[tok]["total"] = totalOccurrence

        for tok in index.keys():
            # print(tok)
            totalOccurrence = float(index[tok]["total"])
            numDocs = len(index[tok].keys())

            for doc in index[tok].keys():
                # print(doc)
                if doc == "total" or doc == "doclist":
                    continue
                # print(type(index[tok][doc]))

                docOccurrence = float(index[tok][doc][0])
                print(docOccurrence)
                #positions = index[tok][doc][1][0]


                print(docOccurrence)

                if docOccurrence == 0:
                    tf = 0
                else:
                    tf = 1 + math.log(docOccurrence)
                print(tf)

                df = math.log(55_393 / numDocs)

                tfidf = tf * df


                title,h1,h2,h3,bold = tuple(index[tok][doc][2])
                t_increase = (title * 0.13 * tfidf)
                h1_increase = (h1 * 0.11* tfidf)
                h2_increase = (h2 * 0.09* tfidf)
                h3_increase = (h3 * 0.07* tfidf)
                b_increase = (bold * 0.05 * tfidf)

                doc_score = tfidf + t_increase + h1_increase + h2_increase + h3_increase + b_increase
                print(doc_score)
                index[tok][doc] = (tfidf, doc_score, positions)

        scoredIndexFileName = "scoredIndex/" + char
        '''
        indexFile = open(scoredIndexFileName, 'w')
        indexFile.write(str(index))
        indexFile.close()
        '''
        json.dump(index, open(scoredIndexFileName, 'w'))
