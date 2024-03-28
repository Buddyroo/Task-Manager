import tkinter as tk
from tkinter import ttk
from tkinter import font as tkFont
from tkcalendar import Calendar
from tkinter import Toplevel

a=[]#we create a list of tasks to save all tasks ever created

def choose_date():
    selected_task_index = task_listbox.selection()
    if selected_task_index:
        def on_date_selected():
            selected_date = cal.selection_get()
            task_listbox.set(selected_task_index, column=2, value=selected_date)
            top.destroy()
        top = Toplevel(root)
        top.grab_set()  # Makes the popup window modal
        cal = Calendar(top, selectmode='day', day=4, month=3, year=2024)
        cal.pack(pady=20)
        ok_button = tk.Button(top, text="OK", command=on_date_selected)
        ok_button.pack()

def add_task():
    task = task_entry.get()
    if task:
        task_listbox.insert('', tk.END, values=("", task, ""),  tags=('NoTag',))
        a.append(task)
        task_entry.delete(0,tk.END)

def edit_task_button():
    selected_task_index = task_listbox.selection()
    if selected_task_index:
        selected_task = task_listbox.item(selected_task_index)['values'][1]
        task_entry.insert(0,selected_task)
        text1.config(text="EDIT TASK: ")
        task_entry.config(width=65)
        add_task_button.config(text="Save changes", command=edit_task)

def edit_task():
    edited_task = task_entry.get()
    if edited_task:
        selected_task_index = task_listbox.selection()
        selected_date = task_listbox.item(selected_task_index)['values'][2]
        selected_name = task_listbox.item(selected_task_index)['values'][0]
        task_listbox.item(selected_task_index, values=(selected_name, edited_task, selected_date))
        task_entry.delete(0, tk.END)
        text1.config(text="Enter a task")
        add_task_button.config(text="Add task", command=add_task)

def show_all_tasks():
    # Display all tasks regardless of their status
    update_task_visibility()

def show_tasks_in_progress():
    update_task_visibility(tag_to_show='in_progress')

def show_completed_tasks():
    update_task_visibility(tag_to_show='done')

def show_cancelled_tasks():
    update_task_visibility(tag_to_show='cancelled')

# Initialize a set to keep track of detached items
detached_items = set()
detached_items_search = set()

def update_task_visibility(tag_to_show=None):
    global detached_items  # Refer to the global set of detached items
    # First, reattach all previously detached items to reset the view
    for child in detached_items:
        task_listbox.reattach(child, '', tk.END)
    detached_items.clear()  # Clear the record of detached items since they are now all reattached
    if tag_to_show:
        # After resetting, apply the new filter (if any)
        for child in task_listbox.get_children():
            tags = task_listbox.item(child, "tags")
            if tag_to_show not in tags:
                task_listbox.detach(child)  # This hides the item
                detached_items.add(child)  # Remember it was detached

def delete_task():
    selected_task_index = task_listbox.selection()
    if selected_task_index:
        task_listbox.delete(selected_task_index)

def mark_task_done():
    selected_task_index = task_listbox.selection()
    if selected_task_index:
        task_listbox.item(selected_task_index, tags=('done',))

def mark_in_progress():
    selected_task_index = task_listbox.selection()
    if selected_task_index:
        task_listbox.item(selected_task_index, tags=('in_progress',))

def mark_cancelled():
    selected_task_index = task_listbox.selection()
    if selected_task_index:
        task_listbox.item(selected_task_index, tags=('cancelled',))

def assign_name():
    selected_task_index = task_listbox.selection()
    if selected_task_index:
        text1.config(text="ENTER NAME: ")
        task_entry.config(width=65)
        add_task_button.config(text="Add name", command = add_name)

def add_name():
    entered_name = task_entry.get()
    if entered_name:
        selected_task_index = task_listbox.selection()
        selected_task = task_listbox.item(selected_task_index)['values'][1]# or selected_task = task_listbox.item(selected_task_index, option = 'values')[1]
        selected_date = task_listbox.item(selected_task_index)['values'][2]
        task_listbox.item(selected_task_index,values = (entered_name,selected_task,selected_date))

        task_entry.delete(0, tk.END)
        text1.config(text="Enter a task")
        add_task_button.config(text="Add task", command = add_task)

def search_tasks():
    global detached_items_search  # Refer to the global set of detached items
    # First, reattach all previously detached items to reset the view
    for child in detached_items_search:
        task_listbox.reattach(child, '', tk.END)
    detached_items_search.clear()  # Clear the record of detached items since they are now all reattached
    search_keyword = search_entry.get().lower()
    if search_keyword:
        for child in task_listbox.get_children():
            selected_task = task_listbox.item(child)['values'][1]
            if search_keyword not in selected_task.lower():
               task_listbox.detach(child)  # This hides the item
               detached_items_search.add(child)  # Remember it was detached

root = tk.Tk()
root.title("Task list")
root.configure(background="CadetBlue3")

# Define a bold font
bold_font = tkFont.Font(family="Helvetica", size=10, weight="bold")

# Frame for adding tasks
add_task_frame = tk.Frame(root, bg="CadetBlue3")
add_task_frame.pack(pady=20)

text1 = tk.Label(add_task_frame, text="ENTER A TASK:", bg="CadetBlue3")
text1.pack(side = tk.LEFT, padx = 5)

task_entry = tk.Entry(add_task_frame, width=70, bg="white", fg="black")
task_entry.pack(side = tk.LEFT, padx = 5)

add_task_button = tk.Button(add_task_frame, text="Add Task", command=add_task, bg="grey80")
add_task_button.pack(side = tk.LEFT, padx = 5)

# Frame for searching tasks
search_frame = tk.Frame(root, bg="CadetBlue3")
search_frame.pack(pady=30)

search_label = tk.Label(search_frame, text="Search:", bg="CadetBlue3", fg="grey30")
search_label.pack(side=tk.LEFT)

search_entry = tk.Entry(search_frame, width=20, bg="azure3", fg="grey35")
search_entry.pack(side=tk.LEFT, padx=5)

search_button = tk.Button(search_frame, text="Search", command=search_tasks, fg="grey30", bg="grey80")
search_button.pack(side=tk.LEFT)

# Filter frame with buttons
show_frame = tk.Frame(root, bg="CadetBlue3", bd = 5)
show_frame.pack(pady=5)

label_show = tk.Label(show_frame, text = "FILTER: ", bg ="CadetBlue3", font=bold_font, fg = "grey30")
label_show.pack (side=tk.LEFT, padx = (5,0))

show_all_tasks_button = tk.Button(show_frame, text="Show All", width = 10, height = 1,  command=show_all_tasks, fg="grey30", bg="grey80")
show_all_tasks_button.pack(side=tk.LEFT, padx=(5,15))

dark_goldenrod2_rectangle = tk.Canvas(show_frame, width=10, height=20, bg="LightGoldenrod2")
dark_goldenrod2_rectangle.pack(side=tk.LEFT, padx=(5,0))

show_tasks_in_progress_button = tk.Button(show_frame, text="In Progress", width = 10,  command=show_tasks_in_progress, fg="grey30", bg="grey80")
show_tasks_in_progress_button.pack(side=tk.LEFT, padx=(5,15))

green4_rectangle = tk.Canvas(show_frame, width=10, height=20, bg="DarkSeaGreen3")
green4_rectangle.pack(side=tk.LEFT, padx=(5,0))

show_completed_tasks = tk.Button(show_frame, text="Completed", width = 10,  command=show_completed_tasks, fg="grey30", bg="grey80")
show_completed_tasks.pack(side=tk.LEFT, padx=(5,15))

firebrick_rectangle = tk.Canvas(show_frame, width=10, height=20, bg="DarkSalmon")
firebrick_rectangle.pack(side=tk.LEFT, padx=(5,0))

show_cancelled_tasks = tk.Button(show_frame, text="Cancelled", width = 10,  command=show_cancelled_tasks, fg="grey30", bg="grey80")
show_cancelled_tasks.pack(side=tk.LEFT, padx=(5,15))

# Label for list of tasks
text2 = tk.Label(root, text="LIST OF TASKS", bg="CadetBlue3", fg="grey30")
text2.pack(pady=(30,10))

# Treeview for task list
task_listbox = ttk.Treeview(root, columns=('assigned_to', 'description', 'due_date'), show='headings')
task_listbox.heading('assigned_to', text='Assigned To')
task_listbox.heading('description', text='Description')
task_listbox.heading('due_date', text='Due Date')
task_listbox.pack(pady=(0,10))

#style for headings
style = ttk.Style()
style.theme_use("default")  # Use the default theme
style.configure("Treeview.Heading", background="grey80", foreground="grey30")

#colors for tags
task_listbox.tag_configure('done', background='DarkSeaGreen3')
task_listbox.tag_configure('in_progress', background='LightGoldenrod2')
task_listbox.tag_configure('cancelled', background='DarkSalmon')

# Buttons
button_frame1 = tk.Frame(root, bg="CadetBlue3")
button_frame1.pack(pady=30)

assign_button = tk.Button(button_frame1, text="Assign a Person to Task", width = 20,  command=assign_name, fg="grey30", bg="grey80")
assign_button.pack(side=tk.LEFT, padx=5)

due_date_button = tk.Button(button_frame1, text="Assign Due Date", width = 15, command=choose_date, fg="grey30", bg="grey80")
due_date_button.pack(side=tk.LEFT, padx=5)

delete_button = tk.Button(button_frame1, text="Delete Task", width = 15, command=delete_task, fg="grey30", bg="grey80")
delete_button.pack(side=tk.LEFT, padx=5)

edit_button = tk.Button(button_frame1, text="Edit Task", width = 15, command=edit_task_button, fg="grey30", bg="grey80")
edit_button.pack(side=tk.LEFT, padx=5)

#Mark as Frame
mark_frame = tk.Frame(root, bg="CadetBlue3", bd = 5)
mark_frame.pack(pady=5)

label_mark = tk.Label(mark_frame, text = "MARK TASK AS: ", bg ="CadetBlue3", font=bold_font, fg = "grey30")
label_mark.pack (side=tk.LEFT, padx = (5,0))

dark_goldenrod2_rectangle = tk.Canvas(mark_frame, width=10, height=20, bg="LightGoldenrod2")
dark_goldenrod2_rectangle.pack(side=tk.LEFT, padx=(5,0))

in_progress_button = tk.Button(mark_frame, text="In Progress", width = 10,  command=mark_in_progress, fg="grey30", bg="grey80")
in_progress_button.pack(side=tk.LEFT, padx=(5,15))

green4_rectangle = tk.Canvas(mark_frame, width=10, height=20, bg="DarkSeaGreen3")
green4_rectangle.pack(side=tk.LEFT, padx=(5,0))

mark_done_button = tk.Button(mark_frame, text="Completed", width = 10,  command=mark_task_done, fg="grey30", bg="grey80")
mark_done_button.pack(side=tk.LEFT, padx=(5,15))

firebrick_rectangle = tk.Canvas(mark_frame, width=10, height=20, bg="DarkSalmon")
firebrick_rectangle.pack(side=tk.LEFT, padx=(5,0))

cancelled_button = tk.Button(mark_frame, width = 10, text="Cancelled",command=mark_cancelled, fg="grey30", bg="grey80")
cancelled_button.pack(side=tk.LEFT, padx=(5,15))

bottom_frame = tk.Frame(root, bg="CadetBlue3", bd = 5)
bottom_frame.pack(pady=20)

root.mainloop()
