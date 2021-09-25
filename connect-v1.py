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


def query(collection,key,bar, output):
    global results
    value = bar.get()
    x = collection.find({"name": "{}".format(value)})
    if int(x.count()) > 0:
        results = x
    else:
        print("no results found for {}".format(value))

    result = results.__getitem__(0)
    int_keys = len(list(result))

    print(int_keys)
    output.config(text='Found {} result(s) with {} key(s)'.format(x.count(), int_keys))

    for i in range(0, int_keys):
        L = tk.Label(leftframe, text=results[result[i]])
        L.grid(sticky=tk.EW, row=2, column=i, columnspan=2)



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
qbtnid = tk.Button(leftframe, text='Query', command=partial(query, mycol, "name", entry, label))
qbtnid.grid(row=0, column=1)




'''
mydict = { "name": "John", "address": "Highway 37" }

x = mycol.insert_one(mydict)

print(x.inserted_id)


x = mycol.find({"name": "John"})
keys = list(x.__getitem__(0))
for key in keys:
    print(key)
    print(x.__getitem__(0)["{}".format(key)])

print(list(x.__getitem__(0)))
print(x.count())
'''
root.mainloop()