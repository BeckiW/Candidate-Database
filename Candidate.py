
from Tkinter import *
from CandidateBackend import Database

COLUMN_ID = 0
COLUMN_NAME = 1
COLUMN_COUNTRY = 2
COLUMN_PROSPECTIVE_ROLE = 3
COLUMN_EXPERIENCE_YEARS = 4
COLUMN_FIRST_CONTACTED = 5
COLUMN_LINKED_IN = 6
COLUMN_CONTACT_DETAILS = 7
COLUMN_SKILLS = 8
COLUMN_NOTES = 9

database = Database("candidates.db")
listbox_items = []
selected_row = None


def search_text_changed(*args):
    if search_text.get():
        search_command()
    else:
        view_command()


def rebuild_listbox():
    list_candidates.delete(0, END)

    for row in listbox_items:
        text = "%s (%s) - %s" % (row[COLUMN_NAME], row[COLUMN_COUNTRY], row[COLUMN_PROSPECTIVE_ROLE])
        list_candidates.insert(END,text)


def view_command():
    del listbox_items[:]

    for row in database.fetch_all():
        listbox_items.append(row)

    rebuild_listbox()


def search_command():
    del listbox_items[:]

    for row in database.search(search_text.get()):
        listbox_items.append(row)

    rebuild_listbox()


def clear_command():
    selected_row = None

    name_text.set( "" )
    country_text.set( "" )
    prospective_role_text.set( "" )
    experience_years_text.set( "" )
    first_contacted_text.set( "" )
    linked_in_text.set( "" )
    contact_details_text.set( "" )
    skills_text.set( "" )
    notes_text.set( "" )


def add_command():
    database.insert(name_text.get(), country_text.get(), prospective_role_text.get(), experience_years_text.get(), first_contacted_text.get(), linked_in_text.get(), contact_details_text.get(), skills_text.get(), notes_text.get())
    view_command()
    clear_command()


def select_row(event):
    global selected_row
    index=list_candidates.curselection()[0]

    selected_row = listbox_items[index]
    print("Selected Row: " + str(selected_row))

    name_text.set( selected_row[COLUMN_NAME] )
    country_text.set( selected_row[COLUMN_COUNTRY] )
    prospective_role_text.set( selected_row[COLUMN_PROSPECTIVE_ROLE] )
    experience_years_text.set( selected_row[COLUMN_EXPERIENCE_YEARS] )
    first_contacted_text.set( selected_row[COLUMN_FIRST_CONTACTED] )
    linked_in_text.set( selected_row[COLUMN_LINKED_IN] )
    contact_details_text.set( selected_row[COLUMN_CONTACT_DETAILS] )
    skills_text.set( selected_row[COLUMN_SKILLS] )
    notes_text.set( selected_row[COLUMN_NOTES] )


def delete_command():
    if selected_row:
        database.delete(selected_row[COLUMN_ID])
        view_command()
        clear_command()


def update_command():
    if selected_row:
        database.update(selected_row[COLUMN_ID], name_text.get(), country_text.get(), prospective_role_text.get(), experience_years_text.get(), first_contacted_text.get(), linked_in_text.get(), contact_details_text.get(), skills_text.get(), notes_text.get())
        view_command()

#####
# Main Script
#####

window = Tk()

window.wm_title("CandidateList")
window.geometry('{}x{}'.format(800, 600))

# The base grid in the window is just 2x2 - containing the left panel, right panel and bottom panel
# These lines tell Tk which rows/columns should stretch for bigger windows
Grid.rowconfigure( window, 0, weight=1 )
Grid.columnconfigure( window, 1, weight=1 )

# Build the left frame with the search box and list of people

left_frame = Frame(window, width=150)
left_frame.grid(row=0, column=0, sticky=N+S+E+W)

Grid.rowconfigure( left_frame, 1, weight=1 )

search_label = Label(left_frame, text = "Search")
search_label.grid(row=0, column=0, sticky=W)

search_text = StringVar()
search_text.trace("w", search_text_changed)

entry_search = Entry(left_frame, textvariable=search_text)
entry_search.grid(row=0, column=1, columnspan=2, sticky=E+W)

scrollbar = Scrollbar(left_frame)
scrollbar.grid(row=1, column=2, sticky=N+S)

list_candidates = Listbox(left_frame, height=8, width=35)
list_candidates.grid(row=1, column=0, columnspan=2, sticky=N+S+E+W)
list_candidates.bind('<<ListboxSelect>>', select_row)

#scrollbar.config(command=list_candidates.yview)
#list_candidates.config(yscrollcommand=scrollbar.set)

# Current Record Panel

right_frame = Frame(window, width=300)
right_frame.grid(row=0, column=1, sticky=N+S+E+W)

Grid.rowconfigure( right_frame, 8, weight=1 )
Grid.columnconfigure( right_frame, 1, weight=1 )

# Setup StringVars that will link the edit boxes to the data
name_text = StringVar()
country_text = StringVar()
prospective_role_text = StringVar()
experience_years_text = StringVar()
first_contacted_text = StringVar()
linked_in_text = StringVar()
contact_details_text = StringVar()
skills_text = StringVar()
notes_text = StringVar()

# Labels for right hand panel
Label(right_frame, text = "Name:").grid(row=0, column=0, sticky=W)
Label(right_frame, text = "Country:").grid(row=1, column=0, sticky=W)
Label(right_frame, text = "Prospective Role:").grid(row=2, column=0, sticky=W)
Label(right_frame, text = "Experience (Years):").grid(row=3, column=0, sticky=W)
Label(right_frame, text = "First Contacted:").grid(row=4, column=0, sticky=W)
Label(right_frame, text = "Linked In:").grid(row=5, column=0, sticky=W)
Label(right_frame, text = "Contact Details:").grid(row=6, column=0, sticky=W)
Label(right_frame, text = "Skills:").grid(row=7, column=0, sticky=W)
Label(right_frame, text = "Notes:").grid(row=8, column=0, sticky=N+W)

# Edit Boxes for right hand panel
entry_name = Entry(right_frame, textvariable=name_text)
entry_name.grid(row=0, column=1, sticky=E+W)

entry_country = Entry(right_frame, textvariable=country_text)
entry_country.grid(row=1, column=1, sticky=E+W)

entry_prospective_role = Entry(right_frame, textvariable=prospective_role_text)
entry_prospective_role.grid(row=2, column=1, sticky=E+W)

entry_experience_years = Entry(right_frame, textvariable=experience_years_text)
entry_experience_years.grid(row=3, column=1, sticky=E+W)

entry_first_contacted = Entry(right_frame, textvariable=first_contacted_text)
entry_first_contacted.grid(row=4, column=1, sticky=E+W)

entry_linked_in = Entry(right_frame, textvariable=linked_in_text)
entry_linked_in.grid(row=5, column=1, sticky=E+W)

entry_contact_details = Entry(right_frame, textvariable=contact_details_text)
entry_contact_details.grid(row=6, column=1, sticky=E+W)

entry_skills = Entry(right_frame, textvariable=skills_text)
entry_skills.grid(row=7, column=1, sticky=E+W)

entry_notes = Entry(right_frame, textvariable=notes_text)
entry_notes.grid(row=8, column=1, sticky=N+E+W)

# Bottom Panel

bottom_frame = Frame(window, height=100)
bottom_frame.grid(row=1, column=0, columnspan=2, sticky=S)

b1 = Button(bottom_frame, text="Refresh", width = 12, command=view_command)
b1.grid(row = 0, column = 0)

b2 = Button(bottom_frame, text="Clear", width = 12, command=clear_command)
b2.grid(row = 0, column = 1)

b3 = Button(bottom_frame, text="Add entry", width = 12, command=add_command)
b3.grid(row = 0, column = 2)

b4 = Button(bottom_frame, text="Update", width = 12, command = update_command)
b4.grid(row = 0, column = 3)

b5 = Button(bottom_frame, text="Delete", width = 12, command = delete_command)
b5.grid(row = 0, column = 4)

view_command()          # Populate the list view before the app starts
window.mainloop()       # Once we run this code, this script stops and control passes to TK
