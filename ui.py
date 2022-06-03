import os
import API

try: import tkinter as tk
except: os.popen('pip install tk')

DODEBUG = True
def debug(title: str, text: str) -> None:
   if DODEBUG: print('[\033[91m' + title.upper() + '\033[0m] ' + text)

class Main(tk.Tk):
   def __init__(self) -> None:
      '''Represents the application.'''
      
      tk.Tk.__init__(self)
      self.client: API.Connection = None
      self.geometry('400x400')
      
      debug('main', 'Initialized app')
      
      # User choices
      self.structure: dict = None
      self.classe: dict = None
      self.students: list = None
      
      self.rootBook: dict = None
      self.rawTitle: dict = None
      self.rawSubTitle: dict = None
      self.folder: dict = None
      
      # On creation, call login
      self.login()

   def clear(self) -> None:
      '''
      Erase all the widgets on the window.
      '''
      
      try:
         for widget in self.winfo_children(): widget.destroy()
      except: pass

   def abort(self, *_) -> None:
      '''
      Ask the user if he *really* wants to abort the operation.
      '''
      
      debug('ABRT', 'Summoned aborter')
      
      popup = tk.Toplevel(self)
      info = tk.Label(popup, text = 'Do you really want to abort?')
      cancel = tk.Button(popup, text = 'No', command = popup.destroy)
      abort = tk.Button(popup, text = 'Yes', command = self.destroy)
      
      info.pack()
      cancel.pack()
      abort.pack()

   def login(self) -> None:
      '''Opens a popup'''
      
      debug('login', 'Summoned login popup')
      
      def check(*_) -> None:
         try:
            self.client = API.Connection(usr_field.get(), pwd_field.get())
            debug('client', f'logged in as {usr_field.get()}')
            
            self.getStructure()
            popup.destroy()
         
         except API.CredErr:
            infoText.set('Invalid credentials, please try again')
            debug('client', 'Failed to login')
      
      popup = tk.Toplevel(self)
      infoText = tk.StringVar(popup, 'Please enter your ENT credentials')
      info = tk.Label(popup, textvariable = infoText)
      
      usr_field = tk.Entry(popup)
      pwd_field = tk.Entry(popup, show = '*')
      # togglePWD = tk.IntVar()
      # showPWD = tk.Checkbutton(popup, text = 'Show password', variable = togglePWD,
      #                          command = lambda *_: pwd_field.config(show = (None, '*')[togglePWD.get()]))
      
      abort = tk.Button(popup, text = 'Cancel', command = self.abort)
      confirm = tk.Button(popup, text = 'OK', command = check)
      
      info.pack()
      usr_field.pack()
      pwd_field.pack()
      # showPWD.pack()
      abort.pack()
      confirm.pack()

   def getStructure(self) -> None:
      '''
      get the students.
      '''
      
      self.clear()
      
      debug('struct', 'Summoned structure part')
      
      def next(*_) -> None:
         # Send structure to self.getClasse
         ch = choice.curselection()[0]
         debug('struct', f'Choose structure {ch}')
         self.structure = structures[ch]
         
         self.getClasse()
      
      structures = self.client.getStructures()
      debug('client', f'Got a total of {len(structures)} structures')
      
      info = tk.Label(self, text = 'Please choose a structure')
      choice = tk.Listbox(self)
      cancel = tk.Button(self, text = 'Quit', command = self.abort)
      confirm = tk.Button(self, text = 'OK', command = next)
      
      for i, struct in enumerate(structures): choice.insert(i, struct['name'])
      
      info.pack()
      choice.pack(expand = True, fill = 'x')
      cancel.pack()
      confirm.pack()

   def getClasse(self) -> None:
      '''
      Get the classe.
      '''
      
      self.clear()
      
      debug('class', 'Summoned class part')
      
      classes = self.client.getClasses(self.structure)
      debug('client', f'Got a total of {len(classes)} classes')
      
      def next(*_) -> None:
         ch = choice.curselection()[0]
         debug('struct', f'Chose classe {ch}')
         
         self.classe = classes[ch]
         self.getStudents()
      
      info = tk.Label(self, text = 'Please choose a classe')
      choice = tk.Listbox(self)
      
      cancel = tk.Button(self, text = 'Cancel', command = self.abort)
      back = tk.Button(self, text = 'Go back', command = self.getStructure)
      confirm = tk.Button(self, text = 'Next', command = next)
            
      for i, classe in enumerate(classes): choice.insert(i, classe['label'])
      
      info.pack()
      choice.pack(expand = True, fill = 'x')
      
      cancel.pack()
      back.pack()
      confirm.pack()

   def getStudents(self) -> None:
      '''
      Get the students from a certain classe and
      makes the user confirm its choice.
      '''
      
      self.clear()
      
      def next(*_) -> None:
         debug('stud', 'Accepted students, saving..')
         self.students = students
         
         # Go next
         self.getBook()
      
      debug('stud', 'Summoned students part')
      
      students = self.client.getStudents(self.structure, self.classe)
      debug('client', f'Got a total of {len(students)} students')
      
      info = tk.Label(self, text = f'Found {len(students)} students:')
      showoff = tk.Listbox(self)
      
      cancel = tk.Button(self, text = 'Cancel', command = self.abort)
      back = tk.Button(self, text = 'Go Back', command = self.getClasse)
      confirm = tk.Button(self, text = 'Next', command = next)
      
      for i, stud in enumerate(students): showoff.insert(i, stud['name'])
      
      info.pack()
      showoff.pack(expand = True, fill = 'x')
      
      cancel.pack()
      back.pack()
      confirm.pack()

   def getBook(self) -> dict:
      '''
      Get the book to copy.
      '''
      
      self.clear()
      
      def next(*_) -> None:
         # Send structure to self.getClasse
         ch = choice.curselection()[0]
         debug('book', f'Chose book {ch}')
         self.rootBook = booklist[ch]
         self.getSettings()
      
      debug('book', 'Summoned book part')
      
      booklist = self.client.getBooks()
      debug('book', f'Got a total of {len(booklist)} books')
      
      info = tk.Label(self, text = 'Please choose a book')
      choice = tk.Listbox(self)
      
      cancel = tk.Button(self, text = 'Cancel', command = self.abort)
      back = tk.Button(self, text = 'Go Back', command = lambda *_: self.getStudents())
      confirm = tk.Button(self, text = 'Next', command = next)
      
      for i, book in enumerate(booklist): choice.insert(i, book['name'])
      
      info.pack()
      choice.pack(expand = True, fill = 'x')
      
      cancel.pack()
      back.pack()
      confirm.pack()
   
   def confirmBook(self) -> None:
      '''
      Demands confirmation on the chosen book.
      '''
      
      img = ImageTk.PhotoImage()

   def getSettings(self) -> None:
      '''
      Asks the user the way it wants the duplication to be.
      '''
      
      self.clear()
      
      def next(*_) -> None:
         # Confirmation popup
         popup = tk.Toplevel(self)
         tk.Label(popup, text = 'the duplication is ready to begin. Are you sure you want to do this?\nTextHolder')
         tk.Button(popup, text = 'No', command = popup.destroy).pack()
         tk.Button(popup, text = 'Yes', command = self.start).pack()
      
      info = tk.Label(self, text = 'Settings')
      confirm = tk.Button(self, text = 'Start duplication')
      
      # Create containers
      ct_title = tk.LabelFrame(self, text = 'Titles', labelanchor = 'n')
      ct_subtt = tk.LabelFrame(self, text = 'Subtitles', labelanchor = 'n')
      ct_repo = tk.LabelFrame(self, text = 'Folder', labelanchor = 'n')
      
      # Title
      tk.Label(ct_title, text = "The %name% variable will be replaced by the name of the student.").pack()
      title_en = tk.Entry(ct_title)
      title_en.insert(-1, 'Book of %name%')
      
      # Subtitle
      tk.Label(ct_subtt, text = 'Same than the title input.').pack()
      subtt_en = tk.Entry(ct_subtt)
      subtt_en.insert(-1, f"Duplicate of {self.rootBook['name']}")
      
      # Folder
      tk.Label(ct_subtt, text = 'The name of the folder that will be created to contain the books.').pack()
      repo_en = tk.Entry(ct_repo)
      
      info.pack()
      title_en.pack(expand = True, fill = 'x')
      subtt_en.pack(expand = True, fill = 'x')
      repo_en.pack(expand = True, fill = 'x')
      
      ct_title.pack(expand = True, fill = 'x')
      ct_subtt.pack(expand = True, fill = 'x')
      ct_repo.pack(expand = True, fill = 'x')
      
      confirm.pack()
   
   def start(self) -> None:
      '''
      Duplicates the books.
      '''
      
      


if __name__ == '__main__':
   os.system('clear')

   app = Main()
   app.title('TK-ENT')
   app.mainloop()

   debug('main', 'Closed app')
