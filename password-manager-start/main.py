from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
           'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
           'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def password_gen():
    password_letters = [choice(letters) for n in range(5)]
    password_numbers = [choice(numbers) for n in range(2)]
    password_symbols = [choice(symbols) for n in range(2)]

    password_list = password_letters + password_numbers + password_symbols
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    info_correct = messagebox.askokcancel(message=f"The info is correct: \n 'Website: ' {website}\n 'User: '{email}\n "
                                                  f"'Password: ' {password}")

    if info_correct:
        if len(password) == 0 or len(website) == 0 or len(email) == 0:
            messagebox.showinfo(title="Error", message="Please make sure you haven't left any empty spaces")
        else:
            try:
                with open("data.json", "r") as data_file:
                    # Read old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving update data
                    json.dump(data, data_file, indent=4)

            finally:
                website_entry.delete(0, END)
                email_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- SEARCH ------------------------------- #

def search():
    website = website_entry.get()

    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Not Found", message="Data not found.")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f'User: {email}\nPassword: {password}')
        else:
            messagebox.showinfo(title="Not Found", message=f"{website} not found.")




# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

canvas = Canvas(width=200, height=200, highlightthickness=0)
padlock = PhotoImage(file="logo.png")
canvas.create_image(100, 95, image=padlock)
canvas.grid(column=1, row=0)

website_label = Label(text="Website")
website_label.grid(column=0, row=1)
website_entry = Entry(width=35)
website_entry.grid(column=1, row=1, columnspan=1)
website_entry.focus()
search = Button(text="Search", command=search, width=15)
search.grid(column=2, row=1)

email_label = Label(text="Email/Username")
email_label.grid(column=0, row=2)
email_entry = Entry(width=54)
email_entry.grid(column=1, row=2, columnspan=2)

password_label = Label(text="Password")
password_label.grid(column=0, row=3)
password_entry = Entry(width=35)
password_entry.grid(column=1, row=3)

button_password = Button(text="Generate Password", command=password_gen)
button_password.grid(column=2, row=3)

add_button = Button(width=50, text="Add User", command=save)
add_button.grid(column=0, row=4, columnspan=3)

window.mainloop()
