import os
import sys

import tkinter
from tkinter import Tk
from tkinter import Text
from tkinter import Toplevel
from tkinter import Variable
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import Checkbutton
from tkinter import Button
from tkinter import Label
from tkinter import Entry
from tkinter import Frame
from tkinter import Toplevel
from tkinter import Menu
from tkinter import Radiobutton 

from tkinter import BOTH
from tkinter import X
from tkinter import WORD 

from tkinter import TOP
from tkinter import LEFT
from tkinter import BOTTOM
from tkinter import RIGHT 

from tkinter import SUNKEN
from tkinter import RAISED
from tkinter import GROOVE
from tkinter import RIDGE 
from tkinter import FLAT

from tkinter import S
from tkinter import SE
from tkinter import NSEW
from tkinter import E
from tkinter import W
from tkinter import N
from tkinter import NE
from tkinter import NW
from tkinter import SW

from tkinter import IntVar
from tkinter import DoubleVar
from tkinter import IntVar
from tkinter import StringVar 

from PIL import Image, ImageTk
import traceback
from tkinter import messagebox
from tkinter import scrolledtext
import sqlite3
from sqlite3 import *

root = Tk()


class SchoolApp: 
    db_conn = 0
    db_cursor = 0
    calc_button = Button()

    @staticmethod
    def quit_app(event=None):
        root.destroy()

    # DATABASE OPERATIONS #

    # this is the main database connection using sqlite3
    def db_connection(self, event=None):
        # create or open the database
        self.db_conn = sqlite3.connect("school.db")
        self.db_conn.commit()

        # create or open admin table
        self.db_conn.execute(''' CREATE TABLE IF NOT EXISTS ADMIN(ID INTEGER PRIMARY KEY AUTOINCREMENT NULL,
                PASSWORD TEXT NOT NULL); ''')
        self.db_conn.commit()

        self.db_conn.execute(''' CREATE TABLE IF NOT EXISTS STUDENT(
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME TEXT NOT NULL,
                EMAIL TEXT NOT NULL,
                LEVEL INTEGER NOT NULL,
                GENDER TEXT NOT NULL); ''')
        self.db_conn.commit()

        self.db_conn.execute(''' CREATE TABLE IF NOT EXISTS TEACHERS(
                ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                NAME TEXT TEXT NOT NULL,
                EMAIL TEXT NOT NULL,
                LEVEL INTEGER NOT NULL,
                QUALIFICATIONS TEXT NOT NULL,
                GENDER TEXT NOT NULL); ''')
        self.db_conn.commit()


    # method used to retrieve all students information from the database
    def get_all_students_data(self, event=None):
        self.db_connection()
        self.db_cursor = self.db_conn.cursor()
        result = self.db_conn.execute("SELECT ID, NAME, EMAIL, LEVEL, GENDER FROM STUDENT ORDER BY ID")
        self.db_conn.commit()

        with open("student_info.txt", "w") as file:
            for row in result:
                file.write("ID : " + str(row[0]) + "\n")
                file.write("NAME : " + str(row[1]) + "\n")
                file.write("EMAIL : " + str(row[2]) + "\n")
                file.write("LEVEL : " + str(row[3]) + "\n")
                file.write("GENDER : " + str(row[4]) + "\n")
                file.write("------------------------------------------- \n\n")

        self.stud_board.delete("1.0", "end")

        text = open("student_info.txt", "r").read()

        self.stud_board.insert("1.0", text)

    # validating student sign up
    def student_signup(self, event=None):
        self.db_connection()
        self.db_conn = sqlite3.connect("school_database.db")
        if self.name_entry.get() == "" or self.email_entry.get() == "" or self.level_entry.get() == "" or self.gender_var.get() == "":
            messagebox.showerror("Trey Academy", "All entry fields should be filled up")
        else:
            self.db_connection()
            self.db_conn.execute("INSERT INTO STUDENT(NAME, EMAIL, LEVEL, GENDER) "
                                 + "VALUES ('" + self.name_entry.get() + "', '" + self.email_entry.get() + "', '" +
                                 self.level_entry.get() + "', '" + self.gender_var.get() + "'); ")
            self.db_conn.commit()
            self.win.destroy()
            messagebox.showinfo("Trey Academy", "Student Account Created Successfully")
            self.get_all_students_data()

    # validating teachers sign up
    def teachers_signup(self, event=None):
        self.db_connection()
        if self.t_name_entry.get() == "" or self.t_email_entry.get() == "" or self.t_level_entry.get() == "" or self.t_qual_entry.get() == "" or self.t_gender_var.get() == 0:
            messagebox.showerror("Trey Academy", "No entry field should be left empty")
        else:
            self.db_connection()
            self.db_conn.execute("INSERT INTO TEACHERS(NAME, EMAIL, LEVEL, QUALIFICATIONS, GENDER) "
                                 + "VALUES ('" + self.t_name_entry.get() + "', '" + self.t_email_entry.get() + "', '" +
                                 self.t_level_entry.get() + "', '" + self.t_qual_entry.get() + "', '" + self.t_gender_var.get() + "'); ")
            self.db_conn.commit()
            self.teach.destroy()
            messagebox.showinfo("Trey Academy", "Teacher's Account Created Successfully")
            self.get_all_teachers_data()


    # retrieving students information
    def get_my_info(self, event=None):
        if self.id_lab_ent.get() == "":
            messagebox.showerror("Trey Academy", "ID entry field must not be empty")
        elif type(self.id_lab_s.get()) != type(1):
            messagebox.showerror("Trey Academy", "ID must be of type integer")
        else:
            self.db_connection()
            self.db_cursor = self.db_conn.cursor()
            result = self.db_conn.execute("SELECT NAME, EMAIL, LEVEL, GENDER FROM STUDENT WHERE ID= " + self.id_lab_ent.get() )
            self.db_conn.commit()

            self.s_name_entry.delete(0, "end")
            self.s_email_entry.delete(0, "end")
            self.s_level_entry.delete(0, "end")

            for row in result:
                self.s_name_entry.insert(0, row[0])
                self.s_email_entry.insert(0, row[1])
                self.s_level_entry.insert(0, row[2])
                self.gender_var_s.set( row[3] )

            get_gen = self.db_conn.execute("SELECT GENDER FROM STUDENT WHERE ID = " + self.id_lab_ent.get() )
            self.db_conn.commit()
            for row in get_gen:
                if str(row[0]) == "F":
                    self.s_female.select()
                else:
                    self.s_male.select()

    # function used to update a student's record
    def update_stud_info(self, event=None):
        self.db_connection()
        if self.s_name_entry.get() != "" or self.s_email_entry.get() != "" or self.s_level_entry.get() != "":
            self.db_cursor = self.db_conn.cursor()
            self.db_cursor.execute("UPDATE STUDENT SET NAME = ' " + self.s_name_entry.get()
                                   + " ', EMAIL = ' " + self.s_email_entry.get()
                                   + " ', LEVEL = ' " + self.s_level_entry.get()
                                   + " ', GENDER = ' " + self.gender_var_s.get()
                                   + " ' WHERE ID = ' " + self.id_lab_ent.get() + " ' ")
            self.db_conn.commit()
            messagebox.showinfo("Trey Academy", "Record updated successfully")

            self.s_name_entry.delete(0, "end")
            self.s_email_entry.delete(0, "end")
            self.s_level_entry.delete(0, "end")

            self.s_male.deselect()
            self.s_female.deselect()

            self.get_all_students_data()

    # method used to delete a student's record
    def delete_student(self, event=None):
        if self.id_lab_ent.get() != "":
            self.db_connection()
            self.db_cursor = self.db_conn.cursor()
            self.db_cursor.execute("DELETE FROM STUDENT WHERE ID = " + self.id_lab_ent.get() )
            self.db_conn.commit()

            messagebox.showinfo("Trey Academy", "Student's Record deleted successfully")

            self.s_name_entry.delete(0, "end")
            self.s_email_entry.delete(0, "end")
            self.s_level_entry.delete(0, "end")

            self.s_male.deselect()
            self.s_female.deselect()
            
            self.get_all_students_data()


    # method used to retrieve all teachers information from the database
    def get_all_teachers_data(self, event=None):
        self.db_connection()
        self.db_cursor = self.db_conn.cursor()
        result = self.db_cursor.execute("SELECT ID, NAME, EMAIL, LEVEL, QUALIFICATIONS, GENDER FROM TEACHERS ORDER BY ID")
        self.db_conn.commit()

        with open("teachers_info.txt", "w") as file:
            for row in result:
                file.write("ID : " + str(row[0]) + "\n")
                file.write("NAME : " + str(row[1]) + "\n")
                file.write("EMAIL : " + str(row[2]) + "\n")
                file.write("LEVEL : " + str(row[3]) + "\n")
                file.write("QUALIFICATION : " + str(row[4]) + "\n")
                file.write("GENDER : " + str(row[5]) + "\n")
                file.write("------------------------------------------- \n\n")

        self.te_board.delete("1.0", "end")

        text = open("teachers_info.txt", "r").read()

        self.te_board.insert("1.0", text)


    # retrieving teacher's information
    def t_get_my_info(self, event=None):
        if self.id_lab_ent_t.get() == "":
            messagebox.showerror("Trey Academy", "ID entry field must not be empty")
        elif type(self.id_lab_t.get()) != type(1):
            messagebox.showerror("Trey Academy", "ID must be of type integer")
        else:
            self.db_connection()
            self.db_cursor = self.db_conn.cursor()
            result = self.db_cursor.execute("SELECT NAME, EMAIL, LEVEL, QUALIFICATIONS, GENDER FROM TEACHERS WHERE ID= " + self.id_lab_ent_t.get() )
            self.db_conn.commit()

            self.te_name_entry.delete(0, "end")
            self.te_email_entry.delete(0, "end")
            self.te_level_entry.delete(0, "end")
            self.te_q_entry.delete(0, "end")

            for row in result:
                self.te_name_entry.insert(0, row[0])
                self.te_email_entry.insert(0, row[1])
                self.te_level_entry.insert(0, row[2])
                self.te_q_entry.insert(0, row[3])
                self.gender_var_te.set( row[4] )

            get_gen = self.db_conn.execute("SELECT GENDER FROM TEACHERS WHERE ID = " + self.id_lab_ent_t.get() )
            self.db_conn.commit()
            for row in get_gen:
                if str(row[0]) == "F":
                    self.te_female.select()
                else:
                    self.te_male.select()


    # this method is used to delete a teacher
    def delete_teacher(self, event=None):
        if self.id_lab_ent_t.get() != "":
            self.db_connection()
            self.db_cursor = self.db_conn.cursor()
            self.db_cursor.execute("DELETE FROM TEACHERS WHERE ID = " + self.id_lab_ent_t.get() )
            self.db_conn.commit()

            messagebox.showinfo("Trey Academy", "Teacher's Record deleted successfully")

            self.te_name_entry.delete(0, "end")
            self.te_email_entry.delete(0, "end")
            self.te_level_entry.delete(0, "end")
            self.te_q_entry.delete(0, "end")

            self.te_male.deselect()
            self.te_female.deselect()
            
            self.get_all_teachers_data()


    # this function updates teachers record
    def update_teachers_info(self, event=None):
        self.db_connection()
        if self.te_name_entry.get() != "" or self.te_email_entry.get() != "" or self.te_password_entry.get() != "" or self.te_level_entry.get() != "" or self.te_q_entry.get():
            self.db_cursor = self.db_conn.cursor()
            self.db_cursor.execute("UPDATE TEACHERS SET NAME = ' " + self.te_name_entry.get()
                                   + " ', EMAIL = ' " + self.te_email_entry.get()
                                   + " ', LEVEL = ' " + self.te_level_entry.get()
                                   + " ', GENDER = ' " + self.gender_var_te.get()
                                   + " ', QUALIFICATIONS = ' " + self.te_q_entry.get()
                                   + " ' WHERE ID = ' " + self.id_lab_ent_t.get() + " ' ")
            self.db_conn.commit()
            messagebox.showinfo("Trey Academy", "Record updated successfully")

            self.te_name_entry.delete(0, "end")
            self.te_email_entry.delete(0, "end")
            self.te_level_entry.delete(0, "end")
            self.te_q_entry.delete(0, "end")

            self.te_male.deselect()
            self.te_female.deselect()

            self.get_all_teachers_data()

    def student_insert(self, event=None):
        try:
            if self.db_connection():
                self.db_conn.execute(" INSERT INTO STUDENT(NAME, EMAIL, LEVEL, GENDER) VALUES("
                                     + self.email_var.get() + ", " + self.level_var.get() + ", " + self.gender_var.get() + "); ")
                self.db_conn.commit()
                messagebox.showinfo("Trey Academy", "Student Account Created Successfully")
            else:
                print("Could not mount database connection")
                traceback.print_exec()
        except OperationalError:
            print("An error occured")
            traceback.print_exec()
    ## END OF DATABASE OPERATIONS ##


######################################### TEACHER SIGN UP ###################################################
    def teacher_sign_up(self, event=None):
        self.db_connection()
        self.teach = Toplevel()
        self.teach.title("Add Teachers")
        self.teach.resizable(width=False, height=False)
        self.teach.geometry("890x200")
        self.teach.configure(bg='dim gray')

        # the icons
        teach_img = Image.open("images/the_teacher.png")
        save_img = Image.open("images/teacher_save.png")

        teach_icon = ImageTk.PhotoImage(teach_img)
        save_icon = ImageTk.PhotoImage(save_img)
        
        # main frame
        frame = Frame(self.teach)
        frame.pack(side=TOP)

        # the student image frame
        teach_frame = Frame(frame, bd=8, bg='dim gray', relief=SUNKEN, width=500, height=200)
        teach_frame.pack(side=LEFT, padx=1, pady=10)

        # the sign up frame
        sign_up = Frame(frame, bd=8, bg='dim gray', relief=SUNKEN, width=500, height=200)
        sign_up.pack(side=LEFT, padx=1, pady=10)

        # the save frame
        save_frame = Frame(frame, bd=8, bg='dim gray', relief=SUNKEN, width=500, height=200)
        save_frame.pack(side=LEFT, padx=1, pady=10)

        # tkinter variables for the sign up entries
        self.t_name_var = StringVar(sign_up, value="")
        self.t_gender_var = StringVar(sign_up, value="")
        self.t_email_var = StringVar(sign_up, value="")
        self.t_password_var = StringVar(sign_up, value="")
        self.t_qual_var = StringVar(sign_up, value="")
        self.t_level_var = StringVar(sign_up, value="")

        # the sign up labels and entries widgets        
        name_label = Label(sign_up, text='Name',bg='dim gray', font=('Klavika', 12, 'bold'))
        name_label.grid(row=0, column=0)

        self.t_name_entry = Entry(sign_up, width=50, relief=SUNKEN, textvariable=self.t_name_var, bd=4)
        self.t_name_entry.grid(row=0, column=2)
        self.t_name_entry.configure(font=('Klavika', 12, 'bold'))
        
        email_label = Label(sign_up, text='Email',bg='dim gray', font=('Klavika', 12, 'bold'))
        email_label.grid(row=2, column=0)

        self.t_email_entry = Entry(sign_up, width=50, relief=SUNKEN, textvariable=self.t_email_var, bd=4)
        self.t_email_entry.grid(row=2, column=2)
        self.t_email_entry.configure(font=('Klavika', 12, 'bold'))
        
        level_label = Label(sign_up, text='Level',bg='dim gray', font=('Klavika', 12, 'bold'))
        level_label.grid(row=4, column=0)

        self.t_level_entry = Entry(sign_up, width=50, relief=SUNKEN, textvariable=self.t_level_var, bd=4)
        self.t_level_entry.grid(row=4, column=2)
        self.t_level_entry.configure(font=('Klavika', 12, 'bold'))

        qual_label = Label(sign_up, text="Qualification", bg='dim gray', font=('Klavika', 12, 'bold'))
        qual_label.grid(row=5, column=0)

        self.t_qual_entry = Entry(sign_up, width=50, relief=SUNKEN, textvariable=self.t_qual_var, bd=4)
        self.t_qual_entry.grid(row=5, column=2)
        self.t_qual_entry.configure(font=('Klavika', 12, 'bold'))
        
        self.male = Radiobutton(sign_up, text="Male",variable=self.t_gender_var, value="M")
        self.male.grid(row=6, column=0)
        self.male.configure(font=('Klavika', 12, 'bold'), bg='dim gray')
        
        self.female = Radiobutton(sign_up, text="Female",variable=self.t_gender_var, value="F")
        self.female.grid(row=6, column=2)
        self.female.configure(font=('Klavika', 12, 'bold'), bg='dim gray')

        # the save and student icon buttons
        save_but = Button(save_frame, image=save_icon, command=self.teachers_signup)
        save_but.image = save_icon
        save_but.pack()

        img_but = Button(teach_frame, image=teach_icon)
        img_but.image = teach_icon
        img_but.pack()

        
        self.teach.mainloop()


    # the student sign up frame
    def student_sign_up(self, event=None):
        self.win = Toplevel()
        self.win.title("Add Student")
        self.win.resizable(width=False, height=False)
        self.win.geometry("880x190")
        self.win.configure(bg='dimgray')

        # the icons
        stud_img = Image.open("images/stud_sign_up.jpeg")
        save_img = Image.open("images/save.png")

        stud_icon = ImageTk.PhotoImage(stud_img)
        save_icon = ImageTk.PhotoImage(save_img)
        
        # main frame
        frame = Frame(self.win)
        frame.pack(side=TOP)

        # the student image frame
        stud_frame = Frame(frame, bd=8, bg='dimgray', relief=SUNKEN, width=500, height=200)
        stud_frame.pack(side=LEFT, padx=1, pady=10)

        # the sign up frame
        sign_up = Frame(frame, bd=8, bg='white', relief=SUNKEN, width=500, height=200)
        sign_up.pack(side=LEFT, padx=1, pady=10)

        # the save frame
        save_frame = Frame(frame, bd=8, bg='dimgray', relief=RAISED, width=500, height=200)
        save_frame.pack(side=LEFT, padx=1, pady=10)

        # tkinter variables for the sign up entries
        self.name_var = StringVar(sign_up, value="")
        self.gender_var = StringVar(sign_up, value="")
        self.email_var = StringVar(sign_up, value="")
        self.password_var = StringVar(sign_up, value="")
        self.level_var = StringVar(sign_up, value="")

        # the sign up labels and entries widgets        
        name_label = Label(sign_up, text='Name',bg='white', font=('Klavika', 12, 'bold'))
        name_label.grid(row=0, column=0)

        self.name_entry = Entry(sign_up, width=50, relief=SUNKEN, textvariable=self.name_var, bd=4)
        self.name_entry.grid(row=0, column=2)
        self.name_entry.configure(font=('Klavika', 12, 'bold'))
        
        email_label = Label(sign_up, text='Email',bg='white', font=('Klavika', 12, 'bold'))
        email_label.grid(row=2, column=0)

        self.email_entry = Entry(sign_up, width=50, relief=SUNKEN, textvariable=self.email_var, bd=4)
        self.email_entry.grid(row=2, column=2)
        self.email_entry.configure(font=('Klavika', 12, 'bold'))
        
        level_label = Label(sign_up, text='Level',bg='white', font=('Klavika', 12, 'bold'))
        level_label.grid(row=4, column=0)

        self.level_entry = Entry(sign_up, width=50, relief=SUNKEN, textvariable=self.level_var, bd=4)
        self.level_entry.grid(row=4, column=2)
        self.level_entry.configure(font=('Klavika', 12, 'bold'))

        self.male = Radiobutton(sign_up, text="Male",variable=self.gender_var, value="M")
        self.male.grid(row=5, column=0)
        self.male.configure(font=('Klavika', 12, 'bold'), bg='white')
        
        self.female = Radiobutton(sign_up, text="Female",variable=self.gender_var, value="F")
        self.female.grid(row=5, column=2)
        self.female.configure(font=('Klavika', 12, 'bold'), bg='white')

        # the save and student icon buttons
        save_but = Button(save_frame, image=save_icon, command=self.student_signup)
        save_but.image = save_icon
        save_but.pack()

        img_but = Button(stud_frame, image=stud_icon)
        img_but.image = stud_icon
        img_but.pack()

        
        self.win.mainloop()
        # END OF STUDENT SIGN UP FRAME #


    def __init__(self, root):
        self.db_connection()
        
        sframe = Frame(root, bd=8, relief=SUNKEN)
        sframe.pack(side=LEFT)
        sframe.configure(bg='dim gray')

        sframe1 = Frame(sframe, bd=4, relief=SUNKEN)
        sframe1.pack(side=TOP, padx=4, pady=4)
        sframe1.configure(bg='white')

        sframe2 = Frame(sframe, bd=2, relief=SUNKEN, bg='silver')
        sframe2.pack(side=TOP, padx=4, pady=4)

        sframe2a = Frame(sframe2, bd=2, bg='white', relief=SUNKEN)
        sframe2a.pack(side=TOP)

        sframe2b = Frame(sframe2, bd=2)
        sframe2b.pack(side=TOP)

        sub_img = Image.open("images/update.jpg")
        sgb_img = Image.open("images/get.jpeg")
        sdb_img = Image.open("images/del.jpeg")
        s_img = Image.open("images/dbstud.png")
        t_img = Image.open("images/th.png")
        add_stud_img = Image.open("images/dbaddstud.jpeg")
        add_te_img = Image.open("images/aat.jpeg")

        sub_icon = ImageTk.PhotoImage(sub_img)
        sgb_icon = ImageTk.PhotoImage(sgb_img)
        sdb_icon = ImageTk.PhotoImage(sdb_img)
        s_icon = ImageTk.PhotoImage(s_img)
        t_icon = ImageTk.PhotoImage(t_img)
        addstud_icon = ImageTk.PhotoImage(add_stud_img)
        add_te_icon = ImageTk.PhotoImage(add_te_img)

        # tkinter variables for the sign up entries
        self.name_var_s = StringVar(sframe, value="")
        self.gender_var_s = StringVar(sframe, value="")
        self.email_var_s = StringVar(sframe, value="")
        self.password_var_s = StringVar(sframe, value="")
        self.level_var_s = StringVar(sframe, value="")
        self.id_lab_s = IntVar(sframe, value="")

        # the students update labels and entries widgets as well as their configurations        
        name_label = Label(sframe1, text='Name',bg='white', font=('Klavika', 12, 'bold'))
        name_label.grid(row=0, column=0)

        self.s_name_entry = Entry(sframe1, width=50, relief=SUNKEN, textvariable=self.name_var_s, bd=4)
        self.s_name_entry.grid(row=0, column=2)
        self.s_name_entry.configure(font=('Klavika', 12, 'bold'))
        
        email_label = Label(sframe1, text='Email',bg='white', font=('Klavika', 12, 'bold'))
        email_label.grid(row=2, column=0)

        self.s_email_entry = Entry(sframe1, width=50, relief=SUNKEN, textvariable=self.email_var_s, bd=4)
        self.s_email_entry.grid(row=2, column=2)
        self.s_email_entry.configure(font=('Klavika', 12, 'bold'))
        
        level_label = Label(sframe1, text='Level',bg='white', font=('Klavika', 12, 'bold'))
        level_label.grid(row=4, column=0)

        self.s_level_entry = Entry(sframe1, width=50, relief=SUNKEN, textvariable=self.level_var_s, bd=4)
        self.s_level_entry.grid(row=4, column=2)
        self.s_level_entry.configure(font=('Klavika', 12, 'bold'))

        self.s_male = Radiobutton(sframe1, text="Male",variable=self.gender_var_s, value="M")
        self.s_male.grid(row=5, column=0)
        self.s_male.configure(font=('Klavika', 12, 'bold'), bg='white')
        
        self.s_female = Radiobutton(sframe1, text="Female",variable=self.gender_var_s, value="F")
        self.s_female.grid(row=5, column=2)
        self.s_female.configure(font=('Klavika', 12, 'bold'), bg='white')

        id_lab = Label(sframe1, text='ID', bg='white', font=('Klavika', 12, 'bold'))
        id_lab.grid(row=6, column=0)

        self.id_lab_ent = Entry(sframe1, width=50, relief=SUNKEN, textvariable=self.id_lab_s, bd=4)
        self.id_lab_ent.grid(row=6, column=2)
        self.id_lab_ent.configure(font=('Klavika', 12, 'bold'))

        sbu = Button(sframe2a, bd=5, image=s_icon, command=self.get_all_students_data)
        sbu.image = s_icon
        sbu.pack(side=LEFT, padx=4, pady=4)

        supdate_but = Button(sframe2a, bd=5, image=sub_icon, command=self.update_stud_info)
        supdate_but.image = sub_icon
        supdate_but.pack(side=LEFT, padx=4, pady=4)

        sget_but = Button(sframe2a, bd=5, image=sgb_icon, command=self.get_my_info)
        sget_but.image = sgb_icon
        sget_but.pack(side=LEFT, padx=4, pady=4)

        sdelete_but = Button(sframe2a, bd=5, image=sdb_icon, command=self.delete_student)
        sdelete_but.image = sdb_icon
        sdelete_but.pack(side=LEFT, padx=4, pady=4)

        st_add = Button(sframe2a, bd=5, image=addstud_icon, command=self.student_sign_up)
        st_add.image = addstud_icon
        st_add.pack(side=LEFT, padx=4, pady=4)
        
 
        self.stud_board = scrolledtext.ScrolledText(sframe2b, bd=20, wrap=WORD)
        self.stud_board.pack(side=BOTTOM, fill=X)
        self.stud_board.configure(bg='white', relief=RIDGE, width=70, font=('Klavika', 12, 'bold'))

        ## TEACHERS


        tframe = Frame(root, bd=8, bg='dimgray', relief=SUNKEN)
        tframe.pack(side=LEFT)

        frame3 = Frame(tframe, bd=4, relief=SUNKEN, bg='#0099ff')
        frame3.pack(side=TOP, padx=4, pady=4)

        frame4 = Frame(tframe, bd=4, relief=SUNKEN, bg='silver')
        frame4.pack(side=TOP, padx=4, pady=4)

        frame4a = Frame(frame4, bd=4, bg='#0099ff', relief=SUNKEN)
        frame4a.pack(side=TOP, padx=4, pady=4)

        frame4b = Frame(frame4, bd=4)
        frame4b.pack(side=TOP, padx=4, pady=4)


        # tkinter variables for the sign up entries
        self.name_var_te = StringVar(tframe, value="")
        self.gender_var_te = StringVar(tframe, value="")
        self.email_var_te = StringVar(tframe, value="")
        self.password_var_te = StringVar(tframe, value="")
        self.level_var_te = StringVar(tframe, value="")
        self.q_var_te = StringVar(tframe, value="")
        self.id_lab_t = IntVar(tframe, value="")

        # the students update labels and entries widgets as well as their configurations        
        tname_label = Label(frame3, text='Name',bg='#0099ff', font=('Klavika', 12, 'bold'))
        tname_label.grid(row=0, column=0)

        self.te_name_entry = Entry(frame3, width=50, relief=SUNKEN, textvariable=self.name_var_te, bd=4)
        self.te_name_entry.grid(row=0, column=2)
        self.te_name_entry.configure(font=('Klavika', 12, 'bold'))
        
        temail_label = Label(frame3, text='Email',bg='#0099ff', font=('Klavika', 12, 'bold'))
        temail_label.grid(row=2, column=0)

        self.te_email_entry = Entry(frame3, width=50, relief=SUNKEN, textvariable=self.email_var_te, bd=4)
        self.te_email_entry.grid(row=2, column=2)
        self.te_email_entry.configure(font=('Klavika', 12, 'bold'))
        
        tlevel_label = Label(frame3, text='Level',bg='#0099ff', font=('Klavika', 12, 'bold'))
        tlevel_label.grid(row=4, column=0)

        self.te_level_entry = Entry(frame3, width=50, relief=SUNKEN, textvariable=self.level_var_te, bd=4)
        self.te_level_entry.grid(row=4, column=2)
        self.te_level_entry.configure(font=('Klavika', 12, 'bold'))

        q_label = Label(frame3, text='Qualification',bg='#0099ff', font=('Klavika', 12, 'bold'))
        q_label.grid(row=5, column=0)

        self.te_q_entry = Entry(frame3, width=50, relief=SUNKEN, textvariable=self.q_var_te, bd=4)
        self.te_q_entry.grid(row=5, column=2)
        self.te_q_entry.configure(font=('Klavika', 12, 'bold'))

        self.te_male = Radiobutton(frame3, text="Male",variable=self.gender_var_te, value="M")
        self.te_male.grid(row=6, column=0)
        self.te_male.configure(font=('Klavika', 12, 'bold'), bg='#0099ff')
        
        self.te_female = Radiobutton(frame3, text="Female",variable=self.gender_var_te, value="F")
        self.te_female.grid(row=6, column=2)
        self.te_female.configure(font=('Klavika', 12, 'bold'), bg='#0099ff')

        tid_lab = Label(frame3, text='ID', bg='#0099ff', font=('Klavika', 12, 'bold'))
        tid_lab.grid(row=7, column=0)

        self.id_lab_ent_t = Entry(frame3, width=50, relief=SUNKEN, textvariable=self.id_lab_t, bd=4)
        self.id_lab_ent_t.grid(row=7, column=2)
        self.id_lab_ent_t.configure(font=('Klavika', 12, 'bold'))

        tbu = Button(frame4a, bd=5, image=t_icon, command=self.get_all_teachers_data)
        tbu.image = t_icon
        tbu.pack(side=LEFT, padx=4, pady=4)

        tupdate_but = Button(frame4a, bd=5, image=sub_icon, command=self.update_teachers_info)
        tupdate_but.image = sub_icon
        tupdate_but.pack(side=LEFT, padx=4, pady=4)

        tget_but = Button(frame4a, bd=5, image=sgb_icon, command=self.t_get_my_info)
        tget_but.image = sgb_icon
        tget_but.pack(side=LEFT, padx=4, pady=4)

        tdelete_but = Button(frame4a, bd=5, image=sdb_icon, command=self.delete_teacher)
        tdelete_but.image = sdb_icon
        tdelete_but.pack(side=LEFT, padx=4, pady=4)

        tadd_but = Button(frame4a, bd=5, image=add_te_icon, command=self.teacher_sign_up)
        tadd_but.image = add_te_icon
        tadd_but.pack(side=LEFT, padx=4, pady=4)
        
        self.te_board = scrolledtext.ScrolledText(frame4b, bd=20, wrap=WORD)
        self.te_board.pack(side=BOTTOM, fill=X)
        self.te_board.configure(bg='#0099ff', relief=RIDGE, width=70, font=('Klavika', 12, 'bold'))

def main():
    try:
        root.title("School Management")
        root.resizable(width=True, height=True)
        root.geometry("1400x700")
        root.state("zoomed")
        root.configure(bg='white', pady=20)
        sch = SchoolApp(root)
        sch.db_connection()
    except Exception:
        traceback.print_exc()
    finally:
        root.mainloop()

if __name__ == "__main__":
    main()
