from tkinter import *
from peewee import *
import datetime


db = SqliteDatabase('to_do_list.db')

class toDoList_db(Model):
    task = CharField(max_length=255)
    timestamp = DateTimeField(default=datetime.datetime.now)
    done = BooleanField(default=False)
    protected = BooleanField(default=False)

    class Meta:
        database = db

class App:
    def __init__(self,master):
        self.master = master
        self.frame = Frame(master, padx = 5, pady = 5)
        self.frame.grid_columnconfigure(0, weight =1)
        self.frame.grid()

        self.addButton = Button(self.frame, text="Add", command=self.add)
        self.addButton.grid(row=1, column=5)

        self.quitButton = Button(self.frame, text="Quit", command=self.quit)
        self.quitButton.grid(row=0, column=4)
        
        self.doneButton = Button(self.frame, text="Done", command=self.done)
        self.doneButton.grid(row=0, column=2)
        
        self.deleteButton = Button(self.frame, text="Delete", command=self.delete)
        self.deleteButton.grid(row=0, column=3)

        label1 = Label(self.frame, text="Commands ")
        label1.grid(row=0, column=0)

        label = Label(self.frame, text="New Task:")
        label.grid(row=1, column=0)

        self.entry = Entry(self.frame)
        self.entry.grid(row=1, column=1, columnspan=4)

        tasks_frame = LabelFrame(self.frame, text="Tasks")
        tasks_frame.grid(columnspan=7, sticky=W+E)
        tasks_frame.columnconfigure(0, weight=1)
        self.tasks = Listbox(tasks_frame)
        self.tasks.grid_columnconfigure(0, weight = 1)
        self.tasks.grid(sticky=E+W)
        
        completed_frame = LabelFrame(self.frame, text="Completed")
        completed_frame.grid(columnspan=7, sticky=E+W)
        completed_frame.columnconfigure(0, weight=1)
        self.completed = Listbox(completed_frame)
        self.completed.grid(sticky=E+W)
        
        self.pull_all_tasks_from_db()

    def add(self):
        task = self.entry.get()
        self.tasks.insert(END,task)
        toDoList_db.create(task = task)

    def done(self):
        sel_task, selection = self.get_selection()
        
        sel_task_db = toDoList_db.get(toDoList_db.task == sel_task)
        
        if sel_task_db.done == False:
            self.tasks.delete(selection[0])
            self.completed.insert(END,sel_task)
            toDoList_db.update(done=True).where(toDoList_db.task == sel_task).execute()
        else:
            self.completed.delete(selection[0])
            self.tasks.insert(END,sel_task)
            toDoList_db.update(done=False).where(toDoList_db.task == sel_task).execute()

    def quit(self):
        self.frame.quit()
        self.master.destroy()

    def pull_all_tasks_from_db(self):
        all_open_tasks = toDoList_db.select().where(toDoList_db.done == False)
        for task in all_open_tasks:
            self.tasks.insert(END, task.task)
            
        all_closed_tasks = toDoList_db.select().where(toDoList_db.done == True)
        for task in all_closed_tasks:
            self.completed.insert(END, task.task)
        
    def clear_database(self):
        for entry in toDoList_db.select():
            entry.delete_instance()
    
    def delete(self):
        sel_task, selection = self.get_selection()
        sel_task_db = toDoList_db.get(toDoList_db.task == sel_task)
        
        if sel_task_db.done == False:
            self.tasks.delete(selection[0])
        else:
            self.completed.delete(selection[0])
        sel_task_db.delete_instance()
        
        
    def get_selection(self):
        selection = self.tasks.curselection()
        completed_selected = False
        if len(selection) == 0:
            selection = self.completed.curselection()
            completed_selected = True
            if len(selection) == 0:
                return
        
        if completed_selected == False:
            sel_task = self.tasks.get(selection[0])
        else:
            sel_task = self.completed.get(selection[0])
        
        return sel_task, selection
        
   
if __name__ == "__main__":        
    root = Tk()
    root.grid_columnconfigure(0, weight=1)
    app = App(root)
    root.mainloop()

    if False: # was using this section to learn how to use peewee. 
        for task_1 in toDoList_db.select():
            #task_1.done = False
            #task_1.save()
            output = "Task: " + str(task_1.task) + ". \tTime stamp: " + str(task_1.timestamp) + ". \tTask Done?: " + str(task_1.done)
            print(output)


