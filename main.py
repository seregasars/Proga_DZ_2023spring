import tkinter as tk
import tkinter.ttk as ttk
import sqlite3
from ttkthemes import ThemedTk
from tkinter import messagebox

class Terminal:
    def __init__(self,root):
        self.root = root
        self.rev = {"#%d"%x:False for x in range(1,7)}

        try:

            # осуществить подключение к БД
            self.connection = sqlite3.connect('transport.db')
            # создать курсор для выполнения запросов
            self.cursor = self.connection.cursor()
            self.createDB()
            self.main_window()

        except sqlite3.Error as error:
            messagebox.showinfo(title="Ошибка БД", message="Ошибка при подключении к sqlite. Данные будет невозможно сохранить в Базу Данных")
            self.main_window()



    def main_window(self):

        self.root.title("Сервис грузовиков")
        self.root.geometry("1600x1000")
        self.bg = tk.PhotoImage(file = "truckbg.png")
        self.label1 = ttk.Label( root, image = self.bg)
        self.label1.place(x = 0, y = 0)
        self.table = ttk.Frame(self.root)
        self.cursor.execute("SELECT * from tTransport")
        self.transport = self.cursor.fetchall()


        self.create_table()
        self.btn_add_venicle = ttk.Button(root,text="      Добавить транспорт     ",command=self.add_venicle)
        self.btn_add_venicle.place(x=282,y=250)
        self.del_btn = ttk.Button(root,text="       Удалить транспорт      ",command=self.delete)
        self.del_btn.place(x=491,y=250)
        self.reserve_btn = ttk.Button(root,text="Забронировать транспорт",command=self.reserve)
        self.reserve_btn.place(x=700,y=250)
        self.letgo_btn = ttk.Button(root,text="   Освободить транспорт   ",command=self.letgo)
        self.letgo_btn.place(x=909,y=250)
        self.choose_btn = ttk.Button(root,text="     Подобрать траспорт     ",command=self.choose_open)
        self.choose_btn.place(x=1120,y=250)

    #очистить фрейм
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    #создание таблицы
    def create_table(self):

        columns = ("#1", "#2", "#3", "#4", "#5", "#6")
        self.tree = ttk.Treeview(self.table, show="headings", height=10, columns=columns)

        self.tree.column("#1",anchor="center")
        self.tree.column("#2",anchor="center")
        self.tree.column("#3",anchor="center")
        self.tree.column("#4",anchor="center")
        self.tree.column("#5",anchor="center")
        self.tree.column("#6",anchor="center")

        self.tree.heading("#1", text="Название", command=lambda:self.treeview_sort_column(self.tree,"#1"))
        self.tree.heading("#2", text="Грузоподьемность", command=lambda:self.treeview_sort_column(self.tree,"#2"))
        self.tree.heading("#3", text="Длинна", command=lambda:self.treeview_sort_column(self.tree,"#3"))
        self.tree.heading("#4", text="Ширина", command=lambda:self.treeview_sort_column(self.tree,"#4"))
        self.tree.heading("#5", text="Высота", command=lambda:self.treeview_sort_column(self.tree,"#5"))
        self.tree.heading("#6", text="Статус бронирования", command=lambda:self.treeview_sort_column(self.tree,"#6"))

        for i in range(len(self.transport)):
            self.tree.insert(parent='',index='end',iid=i,text='', values=self.transport[i])

        self.tree.pack()
        self.table.pack()

    def add_venicle(self):
        self.venicle_window = ThemedTk(theme="kroc")
        self.venicle_window.geometry("200x300")
        self.venicle_window.configure(bg="#f2b862")
        self.venicle_window.title("Характеристики")

        info1 = ttk.Label(self.venicle_window,text="Название")
        self.name_entry1 = ttk.Entry(self.venicle_window)
        info2 = ttk.Label(self.venicle_window,text="Грузоподьемность")
        self.name_entry2 = ttk.Entry(self.venicle_window)
        info3 = ttk.Label(self.venicle_window,text="Длинна")
        self.name_entry3 = ttk.Entry(self.venicle_window)
        info4 = ttk.Label(self.venicle_window,text="Ширина")
        self.name_entry4 = ttk.Entry(self.venicle_window)
        info5 = ttk.Label(self.venicle_window,text="Высота")
        self.name_entry5 = ttk.Entry(self.venicle_window)

        confirm_btn = ttk.Button(self.venicle_window,text="подтвердить ",command=self.confirm_venicle_add)

        info1.pack()
        self.name_entry1.pack()
        info2.pack()
        self.name_entry2.pack()
        info3.pack()
        self.name_entry3.pack()
        info4.pack()
        self.name_entry4.pack()
        info5.pack()
        self.name_entry5.pack()
        confirm_btn.pack()

    def delete(self):
        selected_item = self.tree.selection()[0] ## get selected item
        self.tree.delete(selected_item)
        value = self.transport[int(selected_item)][0]
        self.cursor.execute("DELETE FROM Ttransport WHERE name=?",(value,))
        self.connection.commit()

    def confirm_venicle_add(self):
        if(self.name_entry2.get().isnumeric() and self.name_entry3.get().isnumeric() and self.name_entry4.get().isnumeric() and self.name_entry5.get().isnumeric()):
            value = (self.name_entry1.get(),int(self.name_entry2.get()),int(self.name_entry3.get()),int(self.name_entry4.get()),int(self.name_entry5.get()),"Свободный")
            self.transport.append(value)
            self.tree.insert(parent='',index='end',iid = (len(self.transport) -1),text='', values=value)
            self.venicle_window.destroy()
            self.cursor.execute("INSERT INTO tTransport VALUES(?,?,?,?,?,?)", value)
            self.connection.commit()
        else:
            messagebox.showinfo(title="Ошибка",message="Длинна, Грузоподьемность, Длинна, Ширина - Это числа")

    def treeview_sort_column(self, tv, col):
        if col == "#2":
            l = [(int(tv.set(k, col)), k) for k in tv.get_children('')]
        else:
            l = [(tv.set(k, col), k) for k in tv.get_children('')]

        l.sort(reverse=self.rev[col])
        for k in self.rev.keys():
            tv.heading(k,text=tv.heading(k,"text").replace("↓ ","").replace("↑ ",""))
        tv.heading(col,text=["↑ ","↓ "][self.rev[col]]+tv.heading(col,"text"))
        self.rev[col]=not self.rev[col]
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

    def choose_open(self):
        self.choose_window = ThemedTk(theme="kroc")
        self.choose_window.geometry("250x400")
        self.choose_window.title("Характеристики")
        self.choose_window.configure(bg="#f2b862")
        info1 = ttk.Label(self.choose_window,text="Грузоподьемность")
        self.choose_entry1 = ttk.Entry(self.choose_window)
        info2 = ttk.Label(self.choose_window,text="Длинна")
        self.choose_entry2 = ttk.Entry(self.choose_window)
        info3 = ttk.Label(self.choose_window,text="Ширина")
        self.choose_entry3 = ttk.Entry(self.choose_window)
        info4 = ttk.Label(self.choose_window,text="Высота")
        self.choose_entry4 = ttk.Entry(self.choose_window)

        info1.pack()
        self.choose_entry1.pack()
        info2.pack()
        self.choose_entry2.pack()
        info3.pack()
        self.choose_entry3.pack()
        info4.pack()
        self.choose_entry4.pack()

        self.choosesearch_btn = ttk.Button(self.choose_window,text="Найти транспорт",command=self.find_transport)
        self.choosesearch_btn.pack()

    def find_transport(self):
        if(self.choose_entry1.get().isnumeric() and self.choose_entry2.get().isnumeric() and self.choose_entry3.get().isnumeric() and self.choose_entry4.get().isnumeric()):
            mass = int(self.choose_entry1.get())
            length = int(self.choose_entry2.get())
            width = int(self.choose_entry3.get())
            height = int(self.choose_entry4.get())
            self.tree_window = ttk.Treeview(self.choose_window, show="headings", height=7, columns="#1")
            self.tree_window.column("#1",anchor="center")
            self.tree_window.heading("#1", text="Название")
            marker =0
            for i in range(len(self.transport)):
                if mass <= self.transport[i][1]:
                    if length <= self.transport[i][2]:
                        if width <= self.transport[i][3]:
                            if height <= self.transport[i][4]:
                                if self.transport[i][5] == "Свободный":
                                    self.tree_window.insert(parent='',index='end',iid=i,text='', values=self.transport[i])
                                    marker = 1

            self.tree_window.pack()
            if marker == 1:
                choosebtn = ttk.Button(self.choose_window,text="Забронировать",command=self.reserve)
                choosebtn.pack()
        else:
            messagebox.showinfo(title="Ошибка",message="Длинна, Грузоподьемность, Длинна, Ширина - Это числа")

    def reserve(self):
        try:
            selected_item = self.tree_window.selection()[0]
        except:
            selected_item = self.tree.selection()[0]
        value = self.transport[int(selected_item)]
        value = (value[0],value[1],value[2],value[3],value[4],"Забронирован")
        self.transport[int(selected_item)] = value
        self.tree.item(selected_item,values=value)
        self.cursor.execute("UPDATE tTransport SET status = 'Забронирован' WHERE name = ?",(value[0],))
        self.connection.commit()

    def letgo(self):
        selected_item = self.tree.selection()[0]
        value = self.transport[int(selected_item)]
        value = (value[0],value[1],value[2],value[3],value[4],"Свободный")
        self.transport[int(selected_item)] = value
        self.tree.item(selected_item,values=value)
        self.cursor.execute("UPDATE tTransport SET status = 'Свободный' WHERE name = ?",(value[0],))
        self.connection.commit()

    def createDB(self):
            self.cursor.execute("""CREATE TABLE IF NOT EXISTS tTransport(
               name TEXT PRIMARY KEY,
               maxWeight INT,
               lenght INT,
               width INT,
               height INT,
               status TEXT
               );
            """)

root = ThemedTk(theme="kroc")

app = Terminal(root)
root.mainloop()
