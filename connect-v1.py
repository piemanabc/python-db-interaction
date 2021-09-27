import pymongo
import tkinter as tk
from functools import partial


connection = "mongodb://localhost:27017/"
widget_ids = []
results = ''

myclient = pymongo.MongoClient(connection)
mydb = myclient["test-db"]
mycol = mydb["test"]


# Check the connection is active
def check_con(address, timeout, collection):
    # Create connection query and set timeout
    client = pymongo.MongoClient(address, serverSelectionTimeoutMS=timeout)

    try:
        print(client.server_info())
        print()
        print("connected")
        q = collection.find({})
        result = q.__getitem__(0)
        keys = list(result)
        return keys

    except Exception:
        print("Unable to connect to the server.")

# Cleans up window, removing all widgets that have been added. used to clear and reset window
def clean_up(library):
    print("cleaning up")
    for item in library:
        print("removing {}".format(item))
        item.destroy()

# Popup for editing values in the DB. Triggered by button that is made in draw_read()
def popup_edit(entryv,library):
    print("editing")

# //TODO Make this fucking insert data to the DB

def draw_ins(window, library):
    clean_up(library)
    global widget_ids
    widget_ids = []

# Draws the window for searching the database. Allowing for editing of the values or browsing
def draw_read(window, library):
    clean_up(library)
    global widget_ids
    widget_ids = []


    leftframe = tk.Frame(window)
    leftframe.grid(row=0, column=0, sticky=tk.NSEW)
    library.append(leftframe)

    label = tk.Label(leftframe, text="")
    label.grid(sticky=tk.EW, row=1, column=0, columnspan=2)
    library.append(label)

    entry = tk.Entry(leftframe)
    entry.grid(row=0, column=0)
    library.append(entry)

    qbtnid = tk.Button(leftframe, text='Query', command=partial(query, mycol, entry, label, leftframe))
    qbtnid.grid(row=0, column=1)
    library.append(qbtnid)
    widget_ids = library
    return widget_ids


# The magic function that query's the database. All shall quiver in it's power.
# Required arguments are the collection to read from, the bar to get the search term from, the output label for the result
# count and the window to put it all in
# //TODO make this take a query that has been pre formed as a dict data type
# //TODO This will make the subsequent functions easier to run
# //TODO Also the .count() is defunct, Need to use the collection.count_documents(filter) function.
def query(collection,bar, output, window):
    global results, widget_ids
    value = bar.get()
    # query below
    x = collection.find({"name": "{}".format(value)})
    # if
    if int(x.count()) > 0:
        results = x
    else:
        print("no results found for {}".format(value))
        output.config(text="no results found for '{}'".format(value))
        return

    result = results.__getitem__(0)
    keys = list(result)

    output.config(text='Found {} result(s) with {} key(s)'.format(x.count(), len(keys)))

    for i in range(0, len(keys)+1):
        try:
            L = tk.Label(window, text=keys[i])
            L.grid(row=2, column=i, columnspan=1)
        except IndexError:
            L = tk.Label(window, text='Edit')
            L.grid(row=2, column=i, columnspan=1)
        widget_ids.append(L)

    for i in range(0, x.count()):
        result = results.__getitem__(i)
        for e in range(0,len(keys) + 1):
            try:
                L = tk.Label(window, text=result[keys[e]])
                L.grid(row=3+i, column=e, columnspan=1)
                widget_ids.append(L)
            except IndexError:
                b = tk.Button(window, text='Edit', command=partial(popup_edit, i, results))
                b.grid(row=3+i, column=e, columnspan=1)
                widget_ids.append(b)



keychain = check_con(connection, 5000, mycol)
root = tk.Tk()
root.title("Small Query Program")
root.geometry("400x250")

print(mycol.count_documents({"name": "John"}))




menubar = tk.Menu(root)

filemenu = tk.Menu(root, tearoff=0)
filemenu.add_command(label="insert data", command=partial(draw_ins, root, widget_ids))
filemenu.add_command(label="read and edit", command=partial(draw_read, root, widget_ids))
filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)


root.config(menu=menubar)

root.mainloop()
