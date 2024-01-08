from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
from PIL import ImageTk,Image
import sqlite3
import re
import webbrowser
import clipboard

active_pass=""

class Login:
    
    def __init__(self) -> None:
        def resetPass():
            self.login.destroy()
            Reset()
            
        self.login=Tk()
        self.login.title("Login")
        self.login["bg"]="#ff972e"
        self.login.geometry("600x400")

        self.contents=Frame(self.login)
        self.contents["bg"]="white"
        self.contents.pack(fill="both",expand="yes",padx=10,pady=38)

        self.text=Label(self.contents,text="Welcome to Password Manager",font=("Arial",20))
        self.text.place(x=100,y=50)

        self.password=Entry(self.contents,show="*",font=("Ariel",18))
        self.password.insert(0,"password")
        self.password.place(x=300,y=200,anchor=CENTER)

        self.loginBtn=Button(self.contents,text="Login",command=self.checkpass)
        self.loginBtn.place(x=300,y=250,height=30,width=100,anchor=CENTER)
        
        self.resetBtn=Button(self.contents,text="Reset Password",command=resetPass)
        self.resetBtn.place(x=300,y=300,height=30,width=100,anchor=CENTER)
        
        self.login.mainloop()
        
    def checkpass(self):
        global active_pass
        conn=sqlite3.connect("pass.db")
        cur=conn.cursor()
        storedData=cur.execute("select email,password from pass")
        storedEmail=""
        storedPassword=""
        for row in storedData:
            storedEmail=row[0]
            storedPassword=row[1]            
        if storedPassword == Encryption(self.password.get(),storedEmail).getEncryption():
            active_pass=self.password.get()
            self.login.destroy()
            Main()
        else:
            self.text.config(text="Login Failed Try Again")
            
class Main:
    
    def __init__(self) -> None:
        
        def addNew():
            if self.passwordText.get()!="":
                if database.newRecord((self.websiteText.get(),self.usernameText.get(),Encryption(active_pass,self.passwordText.get()).getEncryption())):
                    messagebox.askokcancel("Successfull","New Record Created Successfully")
                clear()
            else:
                 messagebox.askokcancel("Failed","Password can't be empty")
        
        def update(data):
            trv.delete(*trv.get_children())
            for row in data:
                trv.insert("",END,values=row)
                
        def search():
            sT=searchText.get()
            conn=sqlite3.connect("password.db")
            cur=conn.cursor()
            data=cur.execute("SELECT * FROM passtable  WHERE website LIKE '%"+sT+"%' OR username LIKE '%"+sT+"%' ")
            update(data)
            conn.close()
            
        def clear():
            conn=sqlite3.connect("password.db")
            cur=conn.cursor()
            data=cur.execute("SELECT * FROM passtable")
            update(data)
            conn.close()
            
        def getDetails(event):
            rowid=trv.identify_row(event.y)
            item=trv.item(trv.focus())
            self.accountNo.set(str(item['values'][0]))
            self.websiteText.set(str(item['values'][1]))
            self.usernameText.set(str(item['values'][2]))
            password=Descryption(str(active_pass),str(item['values'][3])).getDecryption()  
            self.passwordText.set(password)
            
        def updateDetails():
            if self.passwordText.get()!="":
                if database.update((self.websiteText.get(),self.usernameText.get(),Encryption(active_pass,self.passwordText.get()).getEncryption(),self.accountNo.get())):
                    messagebox.askokcancel("Update Successfull","The account details has been updated")
                    clear()
                else:
                    messagebox.askokcancel("Failed to update account details","Please check all the details and try again")
            else:
                messagebox.askokcancel("Failed","Password can't be empty")
        
        def redirect():
            webbrowser.open(self.websiteText.get(), new=2)
        
        def copyPass():
            clipboard.copy(self.passwordText.get())
            messagebox.askokcancel("Copy Successfull","Password copy to clipboard successfull")
        
        def deleteAccount():
            if self.accountNo.get()!="" and messagebox.askyesno("Confirm Delete?","Are you sure you want to delete this account?"):
                print(self.accountNo.get())
                database.delete(self.accountNo.get())
                clear()
            else:
                messagebox.askokcancel("Account Id Not Available","Double click on record then delete")
            
        self.main=Tk()
        self.main.title("Accounts")
        self.main.geometry("800x600")
        self.main["bg"]="#ff972e"
        searchText=StringVar()
        
        
        self.accountNo=StringVar()
        self.websiteText=StringVar()
        self.usernameText=StringVar()
        self.passwordText=StringVar()
        
        #icons
        Iadd=ImageTk.PhotoImage(Image.open("icons/add.png"))
        Isave=ImageTk.PhotoImage(Image.open("icons/save.png"))
        Iredirect=ImageTk.PhotoImage(Image.open("icons/redirect.png"))
        Icopy=ImageTk.PhotoImage(Image.open("icons/copy.png"))
        Idelete=ImageTk.PhotoImage(Image.open("icons/delete.png"))
        
        wrapper1=LabelFrame(self.main,text="Account List")
        wrapper2=LabelFrame(self.main,text="search")
        wrapper3=LabelFrame(self.main,text="Account Data")
        
        wrapper1.pack(fill="both",expand="yes",padx=20,pady=10)
        wrapper2.pack(fill="both",expand="yes",padx=20,pady=10)
        wrapper3.pack(fill="both",expand="yes",padx=20,pady=10)
        
        trv=Treeview(wrapper1,columns=(1,2,3,4),show="headings",height="6")
        trv.pack()
        
        trv.heading(1,text="No")
        trv.heading(2,text="Website")
        trv.heading(3,text="Username")
        trv.heading(4,text="Password")
        
        trv.bind('<Double 1>',getDetails)
        
        conn=sqlite3.connect("password.db")
        cur=conn.cursor()
        data=cur.execute("SELECT * FROM passtable")
        update(data)
        conn.close()
        
        #search Section
        lbl=Label(wrapper2,text="search")
        lbl.pack(side=LEFT,padx=10)
        searchEntry=Entry(wrapper2,textvariable=searchText)
        searchEntry.pack(side=LEFT,padx=6)
        searchBtn=Button(wrapper2,text="search",command=search)
        searchBtn.pack(side=LEFT,padx=6)
        clearBtn=Button(wrapper2,text="Clear",command=clear)
        clearBtn.pack(side=LEFT,padx=6)
        
        #Edit section
        Lwebsite=Label(wrapper3,text="Website")
        Lwebsite.grid(row=0,column=0,padx=5,pady=3)
        Ewebsite=Entry(wrapper3,textvariable=self.websiteText)
        Ewebsite.grid(row=0,column=1,padx=5,pady=3)
        
        Lwebsite=Label(wrapper3,text="Username")
        Lwebsite.grid(row=1,column=0,padx=5,pady=3)
        Ewebsite=Entry(wrapper3,textvariable=self.usernameText)
        Ewebsite.grid(row=1,column=1,padx=5,pady=3)
        
        Lwebsite=Label(wrapper3,text="Password")
        Lwebsite.grid(row=2,column=0,padx=5,pady=3)
        Ewebsite=Entry(wrapper3,textvariable=self.passwordText)
        Ewebsite.grid(row=2,column=1,padx=5,pady=3)
        
        addBtn=Button(wrapper3,text="+",command=addNew,image=Iadd)
        addBtn.grid(row=3,column=0,padx=5,pady=3)
        
        updateBtn=Button(wrapper3,text="^",command=updateDetails,image=Isave)
        updateBtn.grid(row=3,column=1,padx=5,pady=3)
        
        redirectBtn=Button(wrapper3,text=">",command=redirect,image=Iredirect)
        redirectBtn.grid(row=3,column=2,padx=5,pady=3)
        
        copyBtn=Button(wrapper3,text="C",command=copyPass,image=Icopy)
        copyBtn.grid(row=3,column=3,padx=5,pady=3)
        
        deleteBtn=Button(wrapper3,text="X",command=deleteAccount,image=Idelete)
        deleteBtn.grid(row=3,column=4,padx=5,pady=3)
        
        self.main.mainloop()   
               
class database:
        
    def getall():
        conn=sqlite3.connect("password.db")
        cur=conn.cursor()
        data=cur.execute("SELECT * FROM passtable")
        return data
    
    def newRecord(values):
        conn=sqlite3.connect("password.db")
        cur=conn.cursor()
        try:
            cur.execute("INSERT INTO passtable(website,username,password) values(?,?,?)",values)
            conn.commit()
            return True
        except:
            print("failed to insert Record")
            
            
            
    def delete(id):
        conn=sqlite3.connect("password.db")
        cur=conn.cursor()
        deleteRow=cur.execute("DELETE from passtable where rowid=(?)",(str(id),))
        conn.commit()

        
    def update(values):
        conn=sqlite3.connect("password.db")
        cur=conn.cursor()
        try:
            deleteRow=cur.execute("""UPDATE passtable set 
                                    website=(?),
                                    username=(?),
                                    password=(?)
                                    where rowid=(?)""",
                                    values)
            conn.commit()
            return True
        except Exception as e:
            print(e)
 
class Encryption:
    def __init__(self,key,text) -> None:
        self.key=key.lower()
        self.text=(text+self.key).lower()
        
    def wordToNum(self):
        self.listOfNum=[]
        for ind,c in enumerate(self.text):
            self.listOfNum.append(ord(c)+ord(self.key[ind%len(self.key)]))
    
    def decToBin(self):
        self.listOfBin=[]
        for dec in self.listOfNum:
            self.listOfBin.append(f'{dec:b}')
        return self.listOfBin
    
    
    def getEncryption(self):
        self.wordToNum()
        binary=self.decToBin()
        return  "".join(binary)
    
class Descryption:
    
    def __init__(self,key,text) -> None:
        self.key=key.lower()
        self.text=text.lower()
        self.originalString=""
    
    def stringToBin(self):
        self.listOfBin=[]
        for i in range(0,len(self.text),8):
            self.listOfBin.append(self.text[i:i+8])
            
    def binaryToNum(self):
        self.listOfDec=[]
        for binary in self.listOfBin:
            self.listOfDec.append(int(binary,2))
            
    def numToWord(self):
        self.listOfWord=""
        for ind,c in enumerate(self.listOfDec):
            self.listOfWord+=chr(c-ord(self.key[ind%len(self.key)]))
                           
    def getDecryption(self):
        self.stringToBin()
        self.binaryToNum()
        self.numToWord()
        return self.listOfWord[:-len(self.key)] 
       
class Register:
    
    def __init__(self) -> None:
        self.eye=0
        def toggleEye():
            if self.eye==0:
                self.password.config(show="")
                self.eye=1
            else:
                self.password.config(show="*")
                self.eye=0
        
        self.register=Tk()
        self.register.title("Register")
        self.register["bg"]="#F9A958"
        self.register.geometry("600x400")
        
        questions=["what is your nickname?","what is your first teacher name?","what is your bestfriend's name?","what is the name of first movie you watched?"]

        self.clicked=StringVar()
        self.clicked.set(questions[0])
        self.contents=Frame(self.register)
        self.contents["bg"]="white"
        self.contents["highlightbackground"]="#666262"
        self.contents["highlightthickness"]=7
        self.contents.place(x=100,y=100,height=270,width=380)

        #Icon Refrence
        Ipassword=ImageTk.PhotoImage(Image.open("icons/password.png"))
        Iemail=ImageTk.PhotoImage(Image.open("icons/email.png"))
        Ieye=ImageTk.PhotoImage(Image.open("icons/eye.png"))
        
        #labels
        LIpassword=Label(self.contents,image=Ipassword,bg="white")
        LIemail=Label(self.contents,image=Iemail,bg="white")
        LwelcomeMsg=Label(self.register,
                          text="Welcome to Password Manager",
                          font=("Arial Rounded MT Bold",20),
                          fg="white",
                          bg="#F9A958")
        LsetDetails=Label(self.contents,
                          bg="white",
                          text="Fill the details",
                          font=("Arial Rounded MT Bold",12),
                          fg="#F9A958")

        
        #Input box
        self.password=Entry(self.contents,highlightthickness=1,bd=0)
        self.password.config(highlightbackground="#F9A958", highlightcolor="#F9A958",show="*")
        self.email=Entry(self.contents,highlightthickness=1,bd=0)
        self.email.config(highlightbackground="#F9A958", highlightcolor="#F9A958")
        self.securtyQuestion=OptionMenu(self.contents,self.clicked,*questions)
        self.securtyAnswer=Entry(self.contents,highlightthickness=1,bd=0)
        self.securtyAnswer.config(highlightbackground="#F9A958", highlightcolor="#F9A958")
        
        #Button
        eyeBtn=Button(self.contents,image=Ieye,bd=0,bg="white",command=toggleEye)
        registerBtn=Button(self.contents,
                           text="Register",
                           bg="#4BFA17",
                           fg="white",
                           bd=0,
                           font=("Arial Rounded MT Bold",11),
                           command=self.savePass)
        
        #all Placements
        LwelcomeMsg.place(x=98,y=27,height=32,width=428)
        LsetDetails.place(x=182-126,y=142-133,height=40,width=212)
        LIpassword.place(x=159-126,y=203-133,height=26,width=26)
        self.password.place(x=190-126,y=200-133,height=31,width=217)
        eyeBtn.place(x=420-126,y=200-133,height=31,width=33)
        LIemail.place(x=155-126,y=241-133,height=30,width=30)
        self.email.place(x=190-126,y=238-133,height=31,width=217)
        self.securtyQuestion.place(x=190-126,y=275-133,height=31,width=222)
        self.securtyAnswer.place(x=190-126,y=310-133,height=31,width=217)
        registerBtn.place(x=249-126,y=346-133,height=30,width=79)

        
        self.register.mainloop()
    
    def savePass(self):
        #validation
        
        #password validation
        if len(self.password.get())<1:
            messagebox.askokcancel("Empty Password!","The password cant be empty please enter password")
            return
        elif(len(self.password.get())<5):
            messagebox.askokcancel("Weak Password!","The length of the password should be greater than or equal to 6")
            return
        
        #email validation
        regex='^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
        if not (re.search(regex,self.email.get())):
            messagebox.askokcancel("Invalid Email!","The provided email is invalid please try again")
            return
        
        #security Question validation
        if len(self.securtyAnswer.get())<1:
            messagebox.askokcancel("Empty Answer","The answer cant be empty please enter password")
            return
            
        conn=sqlite3.connect("pass.db")
        cur=conn.cursor()

        try:
            cur.execute("""CREATE TABLE pass(email VARCHAR(255),password VARCHAR(255),SQ VARCHAR(255),SA VARCHAR(255))""")
        except:
            pass
        finally:
            enc1=Encryption(self.password.get(),self.email.get()).getEncryption()
            enc2=Encryption(self.securtyAnswer.get(),self.password.get()).getEncryption()
            val=(self.email.get(),enc1,self.clicked.get(),enc2)
            print(val)
            res=cur.execute("INSERT INTO pass VALUES(?,?,?,?)",val)
            conn.commit()
            conn=sqlite3.connect("password.db")
            cur=conn.cursor()
            try:
                cur.execute("""CREATE TABLE passtable(rID INTEGER PRIMARY KEY,website VARCHAR(255),username VARCHAR(255),password VARCHAR(2000))""")
            except Exception as e:
                print("error creating passtable",e)
            finally:
                conn.commit()
            self.register.destroy()
            Login()

class Reset:
    
    def __init__(self) -> None:
        def loadLogin():
            self.reset.destroy()
            Login()
        self.reset=Tk()
        self.reset.title("Reset")
        self.reset["bg"]="#ff972e"
        self.reset.geometry("600x400")

        self.contents=Frame(self.reset)
        self.contents["bg"]="white"
        self.contents.pack(fill="both",expand="yes",padx=10,pady=38)

        conn=sqlite3.connect("pass.db")
        cur=conn.cursor()
        data=cur.execute("SELECT SQ from pass")
        for row in data:
            SQ=row[0]
        conn.close()

        #label
        LNewPassword=Label(self.contents,text="New Password",justify=LEFT)
        LQuestion=Label(self.contents,text="Question",justify=LEFT)
        Question=Label(self.contents,text=SQ,justify=LEFT)
        LAnswer=Label(self.contents,text="Answer",justify=LEFT)
    
        #Input box
        self.EPassword=Entry(self.contents)
        self.EAnswer=Entry(self.contents)
        
        #Button
        verifyBtn=Button(self.contents,text="Change",command=self.resetPassword)
        loginBtn=Button(self.reset,text="Login",command=loadLogin)
        
        #all Placements
        loginBtn.place(x=5,y=5,width=80,height=25)
        LNewPassword.place(x=48,y=28,width=145,height=23,)
        self.EPassword.place(x=208,y=25,width=222,height=32)
        LQuestion.place(x=48,y=73,width=87,height=23,)
        Question.place(x=208,y=74,width=300,height=27,)
        LAnswer.place(x=48,y=116,width=74,height=23,)
        self.EAnswer.place(x=208,y=113,width=222,height=32)
        verifyBtn.place(x=227,y=153,width=84,height=37)

        self.reset.mainloop()
        
    def resetPassword(self):
        self.newPassword= self.EPassword.get()
        self.answer=self.EAnswer.get()
        self.encryptedText=""
        conn=sqlite3.connect("pass.db")
        cur=conn.cursor()

        try:
            record=cur.execute("""SELECT SA FROM pass""")
        except:
            print("error in database")
        finally:
            for  row in record:
                self.encryptedText=row[0]  
        password=Descryption(self.answer,self.encryptedText).getDecryption()  
        global active_pass
        conn=sqlite3.connect("pass.db")
        cur=conn.cursor()
        storedData=cur.execute("select email,password from pass")
        storedEmail=""
        storedPassword=""
        for row in storedData:
            storedEmail=row[0]
            storedPassword=row[1]          
        if storedPassword == Encryption(password,storedEmail).getEncryption():
            active_pass=password
            
            enc1=Encryption(self.newPassword,storedEmail).getEncryption()
            enc2=Encryption(self.answer,self.newPassword).getEncryption()
            val=(enc1,enc2)
            cur.execute("UPDATE pass set password=?,SA=?",val)
            conn.commit()
            
            #changing encryption key of password stored in db
            conn=sqlite3.connect("password.db")
            cur=conn.cursor()
            data=cur.execute("SELECT rowid,password FROM passtable")
            for row in data:
                currentPass=Descryption(str(active_pass),str(row[1])).getDecryption() 
                encryptedPassWithNewKey=Encryption(self.newPassword,currentPass).getEncryption()
                cur.execute("UPDATE passtable set password='"+str(encryptedPassWithNewKey)+"' where rowid="+str(row[0])+"")
            conn.commit()
            self.reset.destroy()
            
            Login()
        else:
            messagebox("RESET FAILED","Please Check Your Security Answer")
           
        
if __name__=='__main__':
    conn=sqlite3.connect("pass.db")
    cur=conn.cursor()
    tables=cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pass'").fetchall()
    if tables==[]:
        Register()
    else:  
        Login()
    conn.commit()
    