from tkinter import *

from search import *

# set up dictionaries
INDEX_FILE_DICT = openIndex()
SEEK_DICT = openSeekDict()  

file = open('docindex', 'r')
DOC_INDEX = json.loads(file.readline())
file.close()

tokinfodict = dict()
loadCache(INDEX_FILE_DICT, SEEK_DICT, tokinfodict)

# Used https://datatofish.com/entry-box-tkinter/ for how to code the GUI

# create the Tk object and canvases
root= Tk()

canvas1 = Canvas(root, width = 1000, height = 900)
canvas1.pack()

# print the results
def printResults():  
    query = entry1.get()
    if query == "":
        label1 = Label(root, text="")
        canvas1.create_window(500, 600, window=label1, width=800, height=500)
        return
    topUrls, time = main(INDEX_FILE_DICT, SEEK_DICT, DOC_INDEX, tokinfodict, query)

    out = "Search Time: {} msec\n\n\n\n".format(time)

    for url in topUrls:
        out += url + '\n\n'

    if topUrls == []:
        out += 'No results'

    label1 = Label(root, text=out, wraplength=600)
    canvas1.create_window(500, 500, window=label1, width=800, height=500)

# create the buttons and search
entry1 = Entry(root, width=50)
button1 = Button(text='Search!', command=printResults)
canvas1.create_window(500, 140, window=entry1)
canvas1.create_window(500, 180, window=button1)


root.mainloop()
