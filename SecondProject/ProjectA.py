import tkinter
import tkinter.messagebox
from ProjectMain import *

user_info = account("","","")

class Centralizing: #For positioning app in middle of the screen when appear
    def __init__(self,main_window):
        #Get height/width of screen in pixel - height/width required for the app then devide by 2 to get
        #the central position
        x = (main_window.winfo_screenwidth() - main_window.winfo_reqwidth()) / 2
        y = (main_window.winfo_screenheight() - main_window.winfo_reqheight()) / 2
        #Then use geometry to positioning the app GUI at poisition of x and y
        #Structure for setting position is: +x +y (for dimension is X x Y)
        main_window.geometry("+%d+%d" % (x, y)) #passing value of x and y to the string


class LoggingIn:
    def __init__(self):

        self.main_window = tkinter.Tk()
        Centralizing(self.main_window) #Make the window appear in middle of screen

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)
        self.label1 = tkinter.Label(self.frame1,text="User:",width=10,anchor="e")#anchor e makes text align to east/right
        self.label2 = tkinter.Label(self.frame2,text="Password:",width=10,anchor="e")
        self.txtBoxUser = tkinter.Entry(self.frame1,width=18)
        self.txtBoxPassword = tkinter.Entry(self.frame2,width=18)
        self.btnLogin = tkinter.Button(self.frame3,text="Login",command=self.check)

        OPTIONS = ["Student","Professor","Admin"]
        self.selectedVal = tkinter.StringVar()
        self.selectedVal.set(OPTIONS[0])  # set default value for the dropdown list

        self.userType = tkinter.OptionMenu(self.frame3, self.selectedVal, *OPTIONS)# * sign to let it show one by one option
        self.userType.configure(background="white",activebackground="#c9c9c9")#changing background color and hover effect

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()

        self.label1.pack(side="left")
        self.label2.pack(side="left")

        self.txtBoxUser.pack()
        self.txtBoxPassword.pack()

        self.userType.pack()
        self.btnLogin.pack()

        tkinter.mainloop()

    def check(self):

        print(self.selectedVal.get())
        result = Login.validate(self.selectedVal.get(),self.txtBoxUser.get(), self.txtBoxPassword.get())
        print(result)
        if result == 1:
            checkDetails = user_info.gainDetail(self.selectedVal.get(),self.txtBoxUser.get(), self.txtBoxPassword.get())
            if checkDetails !=1:
                print("Failed to get user details")
            else:
                print(user_info)

            self.main_window.destroy()
            if self.selectedVal.get() == "Student":
                StudentInterface()
            elif self.selectedVal.get() == "Professor":
                ProfessorInterface()
            elif self.selectedVal.get() =="Admin":
                AdminInterface()
        elif result == -3:
            print("Wrong username or password!")
        elif result == -2:
            print("Failed to execute")
        elif result == -1:
            print("Failed to connect server")

class StudentInterface:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)

        self.name = tkinter.StringVar()
        self.name.set(user_info.getFName())
        self.label1 = tkinter.Label(self.frame1,text="Welcome ")
        self.label2 = tkinter.Label(self.frame1,textvariable=self.name)
        self.btnSearch = tkinter.Button(self.frame2,text="Show Grades",command=self.search)
        self.content = tkinter.StringVar()
        self.labelContent = tkinter.Label(self.frame3,textvariable=self.content)

        self.btnQuit = tkinter.Button(self.frame3,text="Quit",command=self.quit_funct)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()

        self.label1.pack(side="left")
        self.label2.pack()
        self.btnSearch.pack()
        self.labelContent.pack()

        self.btnQuit.pack()

        tkinter.mainloop()

    def search(self):
        view = Show.grade(user_info.getId())
        text ="CourseID \t\tCourse Name\t\tGrade\n"
        for x in view:
            for i in x:
                text += str(i) + "\t\t"
            text = text.rstrip("\t\t")
            text += "\n"
        self.content.set(text)

    def quit_funct(self):
        self.main_window.destroy()
        LoggingIn()

class AdminInterface:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)
        self.frame4 = tkinter.Frame(self.main_window)

        self.label1 = tkinter.Label(self.frame1,text="Welcome admin! ")
        self.label2 = tkinter.Label(self.frame1,text="Choose the function you want to work with: ")
        self.btnCreateAccount = tkinter.Button(self.frame2,text="Create Account",command=self.createAccount)
        self.btnUpdateAccount = tkinter.Button(self.frame2,text="Update Account",command=self.updateAccount)
        self.btnDeleteAccount = tkinter.Button(self.frame2,text="Delete Account",command=self.deleteAccount)

        self.btnCreateCourse = tkinter.Button(self.frame3,text="Create Course",command=self.createCourse)
        self.btnUpdateCourse = tkinter.Button(self.frame3, text="Update Course",command=self.updateCourse)
        self.btnDeleteCourse = tkinter.Button(self.frame3, text="Delete Course",command=self.deleteCourse)

        self.btnQuit = tkinter.Button(self.frame4,text="Quit",command=self.quit_funct)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()

        self.label1.pack()
        self.label2.pack()

        self.btnCreateAccount.pack(side="left")
        self.btnDeleteAccount.pack(side ="left")
        self.btnUpdateAccount.pack(side="left")
        self.btnCreateCourse.pack(side="left")
        self.btnUpdateCourse.pack(side="left")
        self.btnDeleteCourse.pack(side="left")
        self.btnQuit.pack()

        tkinter.mainloop()


    def createCourse(self):
        self.main_window.destroy()
        CreateCourse()

    def updateCourse(self):
        self.main_window.destroy()
        UpdateCourse()

    def deleteCourse(self):
        self.main_window.destroy()
        DeleteCourse()

    def createAccount(self):
        self.main_window.destroy()
        CreateAccount()

    def updateAccount(self):
        self.main_window.destroy()
        UpdateAccount()

    def deleteAccount(self):
        self.main_window.destroy()
        DeleteAccount()

    def quit_funct(self):
        self.main_window.destroy()
        LoggingIn()

class CreateCourse:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame4 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)

        self.label1 = tkinter.Label(self.frame1, text="Course ID:", width=12, anchor="e")
        self.label2 = tkinter.Label(self.frame2, text="Professor ID:", width=12, anchor="e")
        self.label3 = tkinter.Label(self.frame4, text="Subject ID:", width=12, anchor="e")

        self.txtBox1 = tkinter.Entry(self.frame1, width=18)
        self.txtBox2 = tkinter.Entry(self.frame2, width=18)
        self.txtBox3 = tkinter.Entry(self.frame4, width=18)

        self.btnCreate = tkinter.Button(self.frame3,text="Create",command = self.create)
        self.btnQuit = tkinter.Button(self.frame3, text="Quit",command=self.quit_funct)

        self.frame1.pack()
        self.frame2.pack()
        self.frame4.pack()
        self.frame3.pack()

        self.label1.pack(side="left")
        self.label2.pack(side="left")
        self.label3.pack(side="left")

        self.txtBox1.pack()
        self.txtBox2.pack()
        self.txtBox3.pack()

        self.btnCreate.pack()
        self.btnQuit.pack()
        tkinter.mainloop()

    def create(self):
        #Data for testing: "CSD2214_6","P0123888","CSD2214"
        result = Admin.createCourse(self.txtBox1.get(),self.txtBox2.get(),self.txtBox3.get())
        if (result == 1):
            tkinter.messagebox.showinfo("Announcement", "Course has been created successfully!!")
        elif (result == -4):
            tkinter.messagebox.showerror("Error", "Failed to create\nor\nThe course already existed")
        else:
            tkinter.messagebox.showerror("Error", "Failed to connect database")

    def quit_funct(self):
        self.main_window.destroy()
        AdminInterface()

class UpdateCourse:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame4 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)

        self.label1 = tkinter.Label(self.frame1, text="Course ID:", width=12, anchor="e")
        self.label2 = tkinter.Label(self.frame2, text="Professor ID:", width=12, anchor="e")
        self.label3 = tkinter.Label(self.frame4, text="Subject ID:", width=12, anchor="e")

        self.txtBox1 = tkinter.Entry(self.frame1, width=18)
        self.txtBox2 = tkinter.Entry(self.frame2, width=18)
        self.txtBox3 = tkinter.Entry(self.frame4, width=18)

        self.btnUpdate = tkinter.Button(self.frame3, text="Update", command =self.update)
        self.btnQuit = tkinter.Button(self.frame3, text="Quit", command=self.quit_funct)

        self.frame1.pack()
        self.frame2.pack()
        self.frame4.pack()
        self.frame3.pack()

        self.label1.pack(side="left")
        self.label2.pack(side="left")
        self.label3.pack(side="left")

        self.txtBox1.pack()
        self.txtBox2.pack()
        self.txtBox3.pack()

        self.btnUpdate.pack()
        self.btnQuit.pack()
        tkinter.mainloop()

    def update(self):
        #Data for testing: "CSD2214_5","P0123888","CSD2214"
        result = Admin.updateCourse(self.txtBox1.get(),self.txtBox2.get(),self.txtBox3.get())
        if (result == 1):
            tkinter.messagebox.showinfo("Announcement", "Course has been updated successfully!!")
        elif (result == -4):
            tkinter.messagebox.showerror("Error", "Failed to update")
        elif (result == -2):
            tkinter.messagebox.showerror("Error", "Problem in query string")
        else:
            tkinter.messagebox.showerror("Error", "Failed to connect database")

    def quit_funct(self):
        self.main_window.destroy()
        AdminInterface()

class DeleteCourse:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)

        self.label1 = tkinter.Label(self.frame1, text="Course ID:", width=12, anchor="e")
        self.label2 = tkinter.Label(self.frame2, text="Course Name:", width=12, anchor="e")

        self.txtBox1 = tkinter.Entry(self.frame1, width=18)
        self.txtBox2 = tkinter.Entry(self.frame2, width=18)

        self.btnDelete = tkinter.Button(self.frame3, text="Delete", command=self.delete)
        self.btnQuit = tkinter.Button(self.frame3, text="Quit", command=self.quit_funct)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()

        self.label1.pack(side="left")
        self.label2.pack(side="left")

        self.txtBox1.pack()
        self.txtBox2.pack()

        self.btnDelete.pack()
        self.btnQuit.pack()
        tkinter.mainloop()

    def delete(self):
        #Data for testing: "CSD2214_7"
        result = Admin.deleteCourse(self.txtBox1.get())
        if (result == 1):
            tkinter.messagebox.showinfo("Announcement", "Course has been deleted successfully!!")
        elif (result == -4):
            tkinter.messagebox.showerror("Error", "Failed to delete the course")
        elif (result == -2):
            tkinter.messagebox.showerror("Error", "Problem in query string")
        else:
            tkinter.messagebox.showerror("Error", "Failed to connect database")

    def quit_funct(self):
        self.main_window.destroy()
        AdminInterface()

class CreateAccount:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)
        self.frame7 = tkinter.Frame(self.main_window)
        self.frame4 = tkinter.Frame(self.main_window)
        self.frame5 = tkinter.Frame(self.main_window)
        self.frame6 = tkinter.Frame(self.main_window)

        self.label1 = tkinter.Label(self.frame1,text="Username:",width=10, anchor="e")
        self.label2 = tkinter.Label(self.frame2, text="Password:",width=10, anchor="e")
        self.label3 = tkinter.Label(self.frame3, text="First Name:",width=10, anchor="e")
        self.label6 = tkinter.Label(self.frame7, text="Last Name:", width=10, anchor="e")
        self.label4 = tkinter.Label(self.frame4, text="User Type:",width=10, anchor="e")
        self.label5 = tkinter.Label(self.frame5, text="ID number:",width=10, anchor="e")

        self.txtBox1 = tkinter.Entry(self.frame1,width=18)
        self.txtBox2 = tkinter.Entry(self.frame2, width=18)
        self.txtBox3 = tkinter.Entry(self.frame3, width=18)
        self.txtBox6 = tkinter.Entry(self.frame7, width=18)
        self.txtBox4 = tkinter.Entry(self.frame4, width=18)
        self.txtBox5 = tkinter.Entry(self.frame5, width=18)

        self.btnCreate = tkinter.Button(self.frame6,text="Create",command =self.create)
        self.btnReset = tkinter.Button(self.frame6, text="Reset",command = self.reset)
        self.btnQuit = tkinter.Button(self.frame6, text="Quit",command=self.quit_funct)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame7.pack()
        self.frame4.pack()
        self.frame5.pack()
        self.frame6.pack()

        self.label1.pack(side="left")
        self.label2.pack(side="left")
        self.label3.pack(side="left")
        self.label6.pack(side="left")
        self.label4.pack(side="left")
        self.label5.pack(side="left")

        self.txtBox1.pack()
        self.txtBox2.pack()
        self.txtBox3.pack()
        self.txtBox6.pack()
        self.txtBox4.pack()
        self.txtBox5.pack()

        self.btnCreate.pack()
        self.btnReset.pack()
        self.btnQuit.pack()

        tkinter.mainloop()

    def create(self):
        #Data for testing: "1239999","abcdef","Phuong","Ly","Student","S01239999"
        result = Admin.createAccount(self.txtBox1.get(),self.txtBox2.get(),self.txtBox3.get(),self.txtBox6.get(),
                                     self.txtBox4.get(),self.txtBox5.get())
        if (result == 1):
            tkinter.messagebox.showinfo("Announcement", "Account has been created successfully!!")
        elif (result == -4):
            tkinter.messagebox.showerror("Error", "Failed to create\nor\nID already existed")
        else:
            tkinter.messagebox.showerror("Error", "Failed to connect database")

    def reset(self):
        self.txtBox1.delete(0, 'end')
        self.txtBox2.delete(0, 'end')
        self.txtBox3.delete(0, 'end')
        self.txtBox4.delete(0, 'end')
        self.txtBox5.delete(0, 'end')
        self.txtBox6.delete(0, 'end')

    def quit_funct(self):
        self.main_window.destroy()
        AdminInterface()

class UpdateAccount:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)
        self.frame7 = tkinter.Frame(self.main_window)
        self.frame4 = tkinter.Frame(self.main_window)
        self.frame5 = tkinter.Frame(self.main_window)
        self.frame6 = tkinter.Frame(self.main_window)

        self.label1 = tkinter.Label(self.frame1, text="Username:", width=10, anchor="e")
        self.label2 = tkinter.Label(self.frame2, text="Password:", width=10, anchor="e")
        self.label3 = tkinter.Label(self.frame3, text="First Name:", width=10, anchor="e")
        self.label6 = tkinter.Label(self.frame7, text="Last Name:", width=10, anchor="e")
        self.label4 = tkinter.Label(self.frame4, text="User Type(*):", width=10, anchor="e")
        self.label5 = tkinter.Label(self.frame5, text="ID number(*):", width=10, anchor="e")

        self.txtBox1 = tkinter.Entry(self.frame1, width=18)
        self.txtBox2 = tkinter.Entry(self.frame2, width=18)
        self.txtBox3 = tkinter.Entry(self.frame3, width=18)
        self.txtBox6 = tkinter.Entry(self.frame7, width=18)
        self.txtBox4 = tkinter.Entry(self.frame4, width=18)
        self.txtBox5 = tkinter.Entry(self.frame5, width=18)

        self.btnUpdate = tkinter.Button(self.frame6, text="Update",command = self.update)
        self.btnQuit = tkinter.Button(self.frame6, text="Quit", command=self.quit_funct)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame7.pack()
        self.frame4.pack()
        self.frame5.pack()
        self.frame6.pack()

        self.label1.pack(side="left")
        self.label2.pack(side="left")
        self.label3.pack(side="left")
        self.label6.pack(side="left")
        self.label4.pack(side="left")
        self.label5.pack(side="left")

        self.txtBox1.pack()
        self.txtBox2.pack()
        self.txtBox3.pack()
        self.txtBox6.pack()
        self.txtBox4.pack()
        self.txtBox5.pack()

        self.btnUpdate.pack()
        self.btnQuit.pack()

        tkinter.mainloop()

    def update(self):
        #Data for testing: "1233838","ABCDEF","Alisa","Lixus","Student","S01233838"
        result = Admin.updateAccount(self.txtBox1.get(),self.txtBox2.get(),self.txtBox3.get(),self.txtBox6.get(),
                                     self.txtBox4.get(),self.txtBox5.get())
        if (result == 1):
            tkinter.messagebox.showinfo("Announcement", "Account has been updated successfully!!")
        elif (result == -4):
            tkinter.messagebox.showerror("Error", "Failed to update")
        elif (result == -2):
            tkinter.messagebox.showerror("Error", "Problem in query string")
        else:
            tkinter.messagebox.showerror("Error", "Failed to connect database")

    def quit_funct(self):
        self.main_window.destroy()
        AdminInterface()

class DeleteAccount:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.frame1 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)
        self.frame4 = tkinter.Frame(self.main_window)

        self.label1 = tkinter.Label(self.frame1, text="Username:", width=10, anchor="e")
        self.label2 = tkinter.Label(self.frame2, text="User Type:", width=10, anchor="e")
        self.label3 = tkinter.Label(self.frame3, text="ID Number:", width=10, anchor="e")

        self.txtBox1 = tkinter.Entry(self.frame1, width=18)
        self.txtBox2 = tkinter.Entry(self.frame2, width=18)
        self.txtBox3 = tkinter.Entry(self.frame3, width=18)

        self.btnDelete = tkinter.Button(self.frame4, text="Delete", command=self.delete)
        self.btnQuit = tkinter.Button(self.frame4, text="Quit", command=self.quit_funct)

        self.frame1.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame4.pack()

        self.label1.pack(side="left")
        self.label2.pack(side="left")
        self.label3.pack(side="left")

        self.txtBox1.pack()
        self.txtBox2.pack()
        self.txtBox3.pack()

        self.btnDelete.pack()
        self.btnQuit.pack()

        tkinter.mainloop()

    def delete(self):
        #Testing data: "1237777","Student","S01237777"
        result = Admin.deleteAccount(self.txtBox1.get(),self.txtBox2.get(),self.txtBox3.get())
        if (result == 1):
            tkinter.messagebox.showinfo("Announcement", "Account has been deleted successfully!!")
        elif (result == -4):
            tkinter.messagebox.showerror("Error", "Failed to delete")
        elif (result == -2):
            tkinter.messagebox.showerror("Error", "Problem in query string")
        else:
            tkinter.messagebox.showerror("Error", "Failed to connect database")

    def quit_funct(self):
        self.main_window.destroy()
        AdminInterface()

class ProfessorInterface:
    def __init__(self):
        self.main_window = tkinter.Tk()
        Centralizing(self.main_window)

        self.name = tkinter.StringVar()
        self.name.set("Welcome professor: "+user_info.getFName())

        self.frame7 = tkinter.Frame(self.main_window)
        self.frame2 = tkinter.Frame(self.main_window)
        self.frame3 = tkinter.Frame(self.main_window)
        self.frame5 = tkinter.Frame(self.main_window)
        self.frame6 = tkinter.Frame(self.main_window)

        self.label6 = tkinter.Label(self.frame7,textvariable=self.name)
        self.label2 = tkinter.Label(self.frame2, text="Student ID:", width=10, anchor="e")
        self.label3 = tkinter.Label(self.frame3, text="Course ID:", width=10, anchor="e")
        self.label5 = tkinter.Label(self.frame5, text="Grade:", width=10, anchor="e")

        self.txtBox2 = tkinter.Entry(self.frame2, width=18)
        self.txtBox3 = tkinter.Entry(self.frame3, width=18)
        self.txtBox5 = tkinter.Entry(self.frame5, width=18)

        self.btnAdd = tkinter.Button(self.frame6,text="Add",command = self.add)
        self.btnReset = tkinter.Button(self.frame6, text="Reset", command=self.reset)
        self.btnQuit = tkinter.Button(self.frame6, text="Quit",command=self.quit_funct)

        self.frame7.pack()
        self.frame2.pack()
        self.frame3.pack()
        self.frame5.pack()
        self.frame6.pack()

        self.label2.pack(side="left")
        self.label3.pack(side="left")
        self.label5.pack(side="left")
        self.label6.pack()

        self.txtBox2.pack()
        self.txtBox3.pack()
        self.txtBox5.pack()

        self.btnAdd.pack()
        self.btnReset.pack()
        self.btnQuit.pack()

        tkinter.mainloop()

    def add(self):
        #Data for testing: "P0123777","S01233838","CSD2214_5",88
        result = Professor.addGrade(user_info.getId(),self.txtBox2.get(),self.txtBox3.get(),self.txtBox5.get())
        if( result == 1):
            tkinter.messagebox.showinfo("Add Grade","Grade has been added successfully!!")
        elif (result == -4):
            tkinter.messagebox.showerror("Error","Grade already existed\nor\nstudenID/CourseID mismatch")
        elif (result == -5):
            tkinter.messagebox.showerror("Error","You have no right to add grade for this course")
        else:
            tkinter.messagebox.showerror("Error", "Failed to connect database")


    def reset(self):
        self.txtBox2.delete(0, 'end')
        self.txtBox3.delete(0, 'end')
        self.txtBox5.delete(0, 'end')

    def quit_funct(self):
        self.main_window.destroy()
        LoggingIn()




# AdminInterface()
# StudentInterface()
# ProfessorInterface()
LoggingIn()
