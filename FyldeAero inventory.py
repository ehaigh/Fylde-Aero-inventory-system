import tkinter as tk
from tkinter import *
from tkinter import messagebox
import csv
import os

#made global, as almost all subroutines use
global isLocked
#boolean which determines if the user has passed the login screen.
isLocked = True


#opens given pages
def open_addpage():
    if not isLocked:
        addpage.tkraise()
    else:
        messagebox.showinfo(title="Inventory Locked", message="Please login to unlock the inventory.")

def open_removepage():
    if not isLocked:
        removepage.tkraise()
    else:
        messagebox.showinfo(title="Inventory Locked", message="Please login to unlock the inventory.")

def open_editpage():
    if not isLocked:
        editpage.tkraise()
    else:
        messagebox.showinfo(title="Inventory Locked", message="Please login to unlock the inventory.")

def open_searchpage():
    if not isLocked:
        searchpage.tkraise()
    else:
        messagebox.showinfo(title="Inventory Locked", message="Please login to unlock the inventory.")

def open_menupage():
    if not isLocked:
        loadStock()
        menupage.tkraise()
    else:
        messagebox.showinfo(title="Inventory Locked", message="Please login to unlock the inventory.")

#Program functions
def exportStock():
    if not isLocked:
        exportmessage = ""
        #opens the file to read
        with open('stock.csv', newline='') as readfile:
            #seperates records
            stockinfo = csv.reader(readfile, delimiter=',', quotechar='|')
            for row in stockinfo:
                exportmessage = exportmessage + "\nName: " + row[0]
                exportmessage = exportmessage + "\nSKU: " + row[1]
                exportmessage = exportmessage + "\nStock Count: " + row[2] + "\n"
        print(exportmessage)
    else:
        messagebox.showinfo(title="Inventory Locked", message="Please login to unlock the inventory.")

def checkUsername(givenUsername):
    global isLocked

    #Ensuring entered a username
    if (givenUsername == ""):
        messagebox.showinfo(title="Enter username", message="Please enter a username.")
        return

    #boolean to determine if username exists
    usernameFound = False

    #opens csv file
    with open('usernames.csv', newline='') as csvfile:
        #seperates records
        usernames = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in usernames:
            #each entry determines a username
            for entry in row:
                #if username is found, then usernameFound becomes true
                if entry == givenUsername:
                    usernameFound = True

    if usernameFound == True:
        #if username is found, open the menu.
        isLocked = False
        open_menupage()
    else:
        #else make a messagebox with the text in it.
        messagebox.showinfo(title="No username found", message="No username found, please try again.")

def addItem(itemName, itemSKU, itemCount):

    #error checking
    if (itemName == "") or (itemName.isnumeric()):
        messagebox.showinfo(title="Enter valid item name", message="Please enter a valid item name.")
        return
    if (itemSKU == ""):
        messagebox.showinfo(title="Enter valid SKU", message="Please enter a valid item SKU.")
        return
    if (itemCount == "") or (not (itemCount.isnumeric())):
        messagebox.showinfo(title="Enter valid count", message="Please enter a valid item count.")
        return

    #open csv file to write
    with open('stock.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        #write information to csv file
        writer.writerow([itemName, itemSKU, itemCount])
    messagebox.showinfo(title="Item Added", message="Item successfully added.")

def removeItem(itemSKU):

    if (itemSKU == ""):
        messagebox.showinfo(title="Enter valid SKU", message="Please enter a valid item SKU.")
        return

    #array to keep all lines apart from the one we want to delete
    keeplines = []
    itemFound = False

    #opens the file to read
    with open('stock.csv', newline='') as readfile:
        #seperates records
        stockinfo = csv.reader(readfile, delimiter=',', quotechar='|')
        for row in stockinfo:
            #if its not the item to remove,
            if row[1] != itemSKU:
                #keep the row.
                keeplines.append(row)
            else:
                itemFound = True

    #checks if any item found
    if itemFound == False:
        messagebox.showinfo(title="Item not Removed", message="No item removed, SKU not found.")
    else:
        #opens the file to write
        with open('stock.csv', 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            #write remaining lines.
            writer.writerows(keeplines)
        messagebox.showinfo(title="Item Removed", message="Item successfully removed.")

def editItem(itemSKU, newStock):

    if (itemSKU == ""):
        messagebox.showinfo(title="Enter valid SKU", message="Please enter a valid item SKU.")
        return

    if (newStock == "") or (not (newStock.isnumeric())):
        messagebox.showinfo(title="Enter valid count", message="Please enter a valid item count.")
        return


    #array to keep all lines apart from the one we want to delete
    keeplines = []
    editline = ""

    #opens the file to read
    with open('stock.csv', newline='') as readfile:
        #seperates records
        stockinfo = csv.reader(readfile, delimiter=',', quotechar='|')
        for row in stockinfo:
            #if its not the item to remove,
            if row[1] != itemSKU:
                #keep the row.
                keeplines.append(row)
            else:
                editline = row
                editline[2] = newStock
                keeplines.append(editline)


    if len(editline) == 0:
        messagebox.showinfo(title="Item not edited", message="No item edited, SKU not found.")
    else:
        #opens the file to write
        with open('stock.csv', 'w', newline='') as writefile:
            writer = csv.writer(writefile)
            #write remaining lines.
            writer.writerows(keeplines)
        messagebox.showinfo(title="Item Edited", message="Item successfully edited.")

def searchItem(value):

    if (value == ""):
        messagebox.showinfo(title="Enter valid value", message="Please enter a valid value.")
        return

    keeplines = []    
    
    #opens the file to read
    with open('stock.csv', newline='') as readfile:
        #seperates records
        stockinfo = csv.reader(readfile, delimiter=',', quotechar='|')
        for row in stockinfo:
            #if it matches criteria,
            if (row[0] == value) or (row[1] == value):
                #keep the row.
                keeplines.append(row)
    
    #if nothing found
    if len(keeplines) == 0:
        messagebox.showinfo(title="No items found", message="No items match criteria.")
    #if something found
    else:
        #creates record of items found.
        searchmessage = "Items found:"
        for row in keeplines:
            searchmessage = searchmessage + "\nName: " + row[0]
            searchmessage = searchmessage + "\nSKU: " + row[1]
            searchmessage = searchmessage + "\nStock Count: " + row[2] + "\n"
        messagebox.showinfo(title="Items found", message=searchmessage)
    
def loadStock():

    # clear old widgets first
    for widget in menupage.winfo_children():
        widget.destroy()

    menulabel = Label(menupage,text="Main menu", font=('Arial', 20))
    menulabel.pack()

    #creates a frame for the values
    rowframe = tk.Frame(menupage)

    #inserts values
    namelabel = Label(rowframe, text="Item Name", font=('Arial', 20), padx=25)
    skulabel = Label(rowframe, text="SKU", font=('Arial', 20), padx=25)
    countlabel = Label(rowframe, text="Stock Count", font=('Arial', 20), padx=25)

    #places values
    namelabel.grid(row=0, column=0)
    skulabel.grid(row=0, column=1)
    countlabel.grid(row=0, column=2)

    loadcount = 0

    #opens csv file
    with open('stock.csv', newline='') as csvfile:
        #seperates records
        stockinfo = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in stockinfo:
            loadcount += 1
            #assigns value for each variable
            name = row[0]
            sku = row[1]
            count = row[2]

            #packs the frame
            rowframe.pack()

            #inserts values
            thisnamelabel = Label(rowframe, text=name, font=('Arial', 14), padx=25)
            thisskulabel = Label(rowframe, text=sku, font=('Arial', 14), padx=25)
            thiscountlabel = Label(rowframe, text=count, font=('Arial', 14), padx=25)

            #places values
            thisnamelabel.grid(row=loadcount, column=0)
            thisskulabel.grid(row=loadcount, column=1)
            thiscountlabel.grid(row=loadcount, column=2)

root = tk.Tk()

#creating a menubar
menubar = tk.Menu(root)

#section: main menu
mainmenu = tk.Menu(menubar, tearoff=0)
#opens menu page
mainmenu.add_command(label="Main Menu", command=open_menupage)

#section: item menu
itemmenu = tk.Menu(menubar, tearoff=0)
#opens add, remove, edit, search pages
itemmenu.add_command(label="Add Item", command=open_addpage)
itemmenu.add_command(label="Remove item", command=open_removepage)
itemmenu.add_command(label="Edit item", command=open_editpage)
itemmenu.add_command(label="Search item", command=open_searchpage)

#section: export menu
exportmenu = tk.Menu(menubar, tearoff=0)
#exports all stock data
exportmenu.add_command(label="Export data", command=exportStock)

#add item management and export sections to menu
menubar.add_cascade(menu=mainmenu, label="Main Menu")
menubar.add_cascade(menu=itemmenu, label="Item Management")
menubar.add_cascade(menu=exportmenu, label="Export")

#add menu to screen
root.config(menu=menubar)

#pages for each function
loginpage = Frame(root)
menupage = Frame(root)
addpage = Frame(root)
removepage = Frame(root)
editpage = Frame(root)
searchpage = Frame(root)

#allows page contents to be visible
loginpage.grid(row=0,column=0, sticky="nsew")
menupage.grid(row=0,column=0, sticky="nsew")
addpage.grid(row=0,column=0, sticky="nsew")
removepage.grid(row=0,column=0, sticky="nsew")
editpage.grid(row=0,column=0, sticky="nsew")
searchpage.grid(row=0,column=0, sticky="nsew")

#Company branding
bottom_label = tk.Label(root, text="FYLDE AERO", font=('Arial', 10))
bottom_label.place(relx=0.5, rely=1.0, anchor="s")


#Code for login page

#Text to ask for username
loginlabel = Label(loginpage,text="Please enter your username.", font=('Arial', 20))
loginlabel.pack()

#text box to enter username
textbox = tk.Entry(loginpage, font=('Arial', 16))
textbox.pack()

#button to confirm username
button = tk.Button(loginpage, text="Confirm", font=('Arial', 16), command=lambda: checkUsername(textbox.get()))
button.pack()


#Code for add page

#title
addlabel = Label(addpage,text="Add item", font=('Arial', 20))
addlabel.pack()

#prompts to enter item name
itemnamelabel = Label(addpage,text="Please enter the item name", font=('Arial', 20))
itemnamelabel.pack()

#text box to enter item name
itemnametextbox = tk.Entry(addpage, font=('Arial', 16))
itemnametextbox.pack()

#prompts to enter sku number
skunumlabel = Label(addpage,text="Please enter the SKU number", font=('Arial', 20))
skunumlabel.pack()

#text box to enter sku number
skunumtextbox = tk.Entry(addpage, font=('Arial', 16))
skunumtextbox.pack()

#prompts to enter initial count
initialcountlabel = Label(addpage,text="Please enter the initial count", font=('Arial', 20))
initialcountlabel.pack()

#text box to enter initial count
initialcounttextbox = tk.Entry(addpage, font=('Arial', 16))
initialcounttextbox.pack()

#button to confirm values
addbutton = tk.Button(addpage, text="Confirm", font=('Arial', 16), command=lambda: addItem(itemnametextbox.get(),skunumtextbox.get(),initialcounttextbox.get()))
addbutton.pack()


#Code for remove page

#title
removelabel = Label(removepage,text="Remove item", font=('Arial', 20))
removelabel.pack()

#prompts to enter sku
removeitemlabel = Label(removepage,text="Please enter the SKU number", font=('Arial', 20))
removeitemlabel.pack()

#text box to enter sku
removetextbox = tk.Entry(removepage, font=('Arial', 16))
removetextbox.pack()

#button to confirm values
removebutton = tk.Button(removepage, text="Confirm", font=('Arial', 16), command=lambda: removeItem(removetextbox.get()))
removebutton.pack()


#Code for edit page

#title
editlabel = Label(editpage,text="Edit item stock", font=('Arial', 20))
editlabel.pack()

#prompts to enter sku
edititemlabel = Label(editpage,text="Please enter the SKU number", font=('Arial', 20))
edititemlabel.pack()

#text box to enter sku
edititemtextbox = tk.Entry(editpage, font=('Arial', 16))
edititemtextbox.pack()

#prompts to enter stock
editstocklabel = Label(editpage,text="Please enter the updated stock amount", font=('Arial', 20))
editstocklabel.pack()

#text box to enter stock
editstocktextbox = tk.Entry(editpage, font=('Arial', 16))
editstocktextbox.pack()

#button to confirm values
editbutton = tk.Button(editpage, text="Confirm", font=('Arial', 16), command=lambda: editItem(edititemtextbox.get(),editstocktextbox.get()))
editbutton.pack()


#Code for search page

#title
searchlabel = Label(searchpage,text="Search for items", font=('Arial', 20))
searchlabel.pack()

#prompts to enter sku or name
searchitemlabel = Label(searchpage,text="Enter item SKU number or name", font=('Arial', 20))
searchitemlabel.pack()

#text box to enter sku or name
searchitemtextbox = tk.Entry(searchpage, font=('Arial', 16))
searchitemtextbox.pack()

#button to confirm values
searchbutton = tk.Button(searchpage, text="Confirm", font=('Arial', 16), command=lambda: searchItem(searchitemtextbox.get()))
searchbutton.pack()

#sets initial page to login
loginpage.tkraise()


root.geometry("500x300") #window size
root.title("Inventory Management System")

root.mainloop()

