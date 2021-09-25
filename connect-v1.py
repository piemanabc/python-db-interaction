import pymongo
import tkinter as tk
from functools import partial


connection = "mongodb://localhost:27017/"
button_ids = []
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


def query(collection,bar, output):
    global results
    value = bar.get()
    x = collection.find({"name": "{}".format(value)})
    if int(x.count()) > 0:
        results = x
    else:
        print("no results found for {}".format(value))

    result = results.__getitem__(0)
    keys = list(result)

    output.config(text='Found {} result(s) with {} key(s)'.format(x.count(), len(keys)))

    for i in range(0, len(keys)):
        L = tk.Label(leftframe, text=keys[i])
        L.grid(row=2, column=i, columnspan=1)
    for i in range(0, x.count()):
        result = results.__getitem__(i)
        for e in range(0,len(keys)):
            L = tk.Label(leftframe, text=result[keys[e]])
            L.grid(row=3+i, column=e, columnspan=1)


check_con(connection, 5000)
root = tk.Tk()
root.title("Small Query Program")
root.geometry("400x250")

leftframe = tk.Frame(root)

leftframe.grid(row=0, column=0, sticky=tk.NSEW)


label = tk.Label(leftframe, text="")
label.grid(sticky=tk.EW, row=1, column=0, columnspan=2)

entry = tk.Entry(leftframe)
entry.grid(row=0, column=0)
qbtnid = tk.Button(leftframe, text='Query', command=partial(query, mycol, entry, label))
qbtnid.grid(row=0, column=1)

x = mycol.find({"name": "John"})
print(x.__getitem__(0))

root.mainloop()