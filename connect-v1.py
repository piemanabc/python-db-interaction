import pymongo
import tkinter as tk
from functools import partial


connection = "mongodb://localhost:27017/"
widget_ids = []
results = ''

myclient = pymongo.MongoClient(connection)
mydb = myclient["test-db"]
mycol = mydb["test"]


def check_con(address, timeout):
    # ensure connection is started

    # set a 5-second connection timeout
    client = pymongo.MongoClient(address, serverSelectionTimeoutMS=timeout)
    try:
        print(client.server_info())
        print()
        print("connected")

    except Exception:
        print("Unable to connect to the server.")


def test(bar):
    print(bar.get())


def clean_up(library):
    global widget_ids
    for item in library:
        item.destroy()


def draw_ins(window, library):
    clean_up(library)


def draw_read(window, library):
    global widget_ids
    clean_up(library)
    widget_ids = []

    leftframe = tk.Frame(window)
    leftframe.grid(row=0, column=0, sticky=tk.NSEW)
    widget_ids.append(leftframe)

    label = tk.Label(leftframe, text="")
    label.grid(sticky=tk.EW, row=1, column=0, columnspan=2)
    widget_ids.append(label)

    entry = tk.Entry(leftframe)
    entry.grid(row=0, column=0)
    widget_ids.append(entry)

    qbtnid = tk.Button(leftframe, text='Query', command=partial(query, mycol, entry, label, leftframe))
    qbtnid.grid(row=0, column=1)
    widget_ids.append(qbtnid)


def query(collection,bar, output, window):
    global results, widget_ids
    value = bar.get()
    x = collection.find({"name": "{}".format(value)})
    if int(x.count()) > 0:
        results = x
    else:
        print("no results found for {}".format(value))
        output.config(text="no results found for '{}'".format(value))
        return

    result = results.__getitem__(0)
    keys = list(result)

    output.config(text='Found {} result(s) with {} key(s)'.format(x.count(), len(keys)))

    for i in range(0, len(keys)):
        L = tk.Label(window, text=keys[i])
        L.grid(row=2, column=i, columnspan=1)
        widget_ids.append(L)
    for i in range(0, x.count()):
        result = results.__getitem__(i)
        for e in range(0,len(keys)):
            L = tk.Label(window, text=result[keys[e]])
            L.grid(row=3+i, column=e, columnspan=1)
            widget_ids.append(L)


check_con(connection, 5000)
root = tk.Tk()
root.title("Small Query Program")
root.geometry("400x250")




menubar = tk.Menu(root)

filemenu = tk.Menu(root, tearoff=0)
filemenu.add_command(label="insert data", command=partial(draw_ins, root, widget_ids))
filemenu.add_command(label="read and edit", command=partial(draw_read, root, widget_ids))
filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


root.config(menu=menubar)

root.mainloop()
