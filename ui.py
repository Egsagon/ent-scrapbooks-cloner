# ================== #
# Required modules: tkinter
# install using: pip install tk
   
# Github: https://github.com/Egsagon/sb_ent_gest5
# ================== #


# == Dependencies == #
import os
import API
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk


# = Settings ======= #
MAX_RETRIES = 3
DODEBUG = True
# ================== #


def debug(title: str, text: str) -> None:
   if DODEBUG: print('[  \033[91m' + title.upper()[:4] + '\033[0m  ] ' + text)


class Main(tk.Tk):
   def __init__(self, start: bool = True) -> None:
      '''Represents the application.'''
      
      # Main window
      tk.Tk.__init__(self)
      self.client: API.Connection = None
      self.geometry('400x400')
      
      debug('main', 'Initialized app')
      
      # Students choices
      self.structure: dict = None
      self.classe: dict = None
      self.students: list = None
      
      # Preferences
      self.rootBook: dict = None
      self.rawTitle: str = None
      self.rawSubTitle: str = None
      self.folderName: str = None
      
      # Progress variables
      self.progress: tk.StringVar = tk.StringVar(self, '...')
      self.overallProg: int = 0
      self.selfProg: int = 0
      
      # Progress bars
      self.mainProgressBar: ttk.Progressbar = None
      self.secondProgressBar: ttk.Progressbar = None
      
      # Start application
      if start: self.login()

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
      
      popup.title('TK-ENT')

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
      abort = tk.Button(popup, text = 'Cancel', command = self.abort)
      confirm = tk.Button(popup, text = 'OK', command = check)
      
      pwd_field.bind('<Return>', check)
      
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

   def getSettings(self) -> None:
      '''
      Asks the user the way it wants the duplication to be.
      '''
      
      self.clear()
      
      def next(*_) -> None:
         # Save the settings
         # TODO - Check if settings are valid
         self.rawTitle = title_en.get()
         self.rawSubTitle = subtt_en.get()
         self.folderName = repo_en.get()
         debug('set', f'Saved settings {self.rawTitle}, {self.rawSubTitle}, {self.folderName}')

         # Confirmation popup
         popup = tk.Toplevel(self)
         tk.Label(popup, text = 'the duplication is ready to begin. Are you sure you want to do this?\n___').pack()
         tk.Button(popup, text = 'No', command = popup.destroy).pack()
         tk.Button(popup, text = 'Yes', command = self.start).pack()
         
         popup.title('TK-ENT')
      
      info = tk.Label(self, text = 'Settings')
      cancel = tk.Button(self, text = 'Cancel', command = self.abort)
      back = tk.Button(self, text = 'Back', command = self.getBook)
      confirm = tk.Button(self, text = 'Start duplication', command = next)
      
      # Create containers
      ct_title = tk.LabelFrame(self, text = 'Titles', labelanchor = 'n')
      ct_subtt = tk.LabelFrame(self, text = 'Subtitles', labelanchor = 'n')
      ct_repo = tk.LabelFrame(self, text = 'Folder', labelanchor = 'n')
      
      # Title
      tk.Label(ct_title, text = "The %name% variable will be replaced by the name of the student. Please don't use too 'fancy' chars.").pack()
      title_en = tk.Entry(ct_title)
      title_en.insert(-1, 'Book of %name%')
      
      # Subtitle
      tk.Label(ct_subtt, text = 'Same than the title input.').pack()
      subtt_en = tk.Entry(ct_subtt)
      subtt_en.insert(-1, str(f"Duplicate of {self.rootBook['name']}"))
      
      # Folder
      tk.Label(ct_subtt, text = 'The name of the folder that will be created to contain the books.\nPlease make sure that you don\'t use an already existing book.').pack()
      repo_en = tk.Entry(ct_repo)
      
      info.pack()
      title_en.pack(expand = True, fill = 'x')
      subtt_en.pack(expand = True, fill = 'x')
      repo_en.pack(expand = True, fill = 'x')
      
      ct_title.pack(expand = True, fill = 'x')
      ct_subtt.pack(expand = True, fill = 'x')
      ct_repo.pack(expand = True, fill = 'x')
      
      cancel.pack()
      back.pack()
      confirm.pack()

   def duplicate(self) -> None:
      '''
      Duplicating process.
      '''
      
      length = len(self.students)
      createdBooksIds = []
      
      for i, student in enumerate(self.students):
         
         # Debug
         text = f'Duplicating book for {student["name"]} ({i + 1}/{length})'
         debug('dupl', text)
         
         # Update app
         self.progress.set(text)
         self.mainProgressBar.step((i / length) * 100)
         self.secondProgressBar.step(33)
         
         # Duplicate
         for retry in range(MAX_RETRIES):
            try:
               currentBookId = self.client.duplicateBook(self.rootBook)
               currentBook = self.client.getBook(currentBookId)
               
               debug('duplication', '[Duplicated]')
               self.secondProgressBar.step(33)
               break
            
            except API.DataErr:
               print('FAIL on DUPLICATE, retrying')
            
            except Exception as e:
               print(f'\nRaised exception: {e} (attempt {retry}/{MAX_RETRIES})')
         
         # Rename
         for retry in range(MAX_RETRIES):
            try:
               cur_title = self.rawTitle
               if '%name%' in cur_title: cur_title = cur_title.replace('%name%', student['name'])
               
               cur_subTitle = self.rawSubTitle
               if '%name%' in cur_subTitle: cur_subTitle = cur_subTitle.replace('%name%', student['name'])
               
               self.client.renameBook(currentBook, cur_title, cur_subTitle)
               
               createdBooksIds.append(currentBook['_id'])
               
               debug('duplication', '[Renamed]')
               self.secondProgressBar.step(33)
               break
            
            except API.DataErr:
               print('FAIL on RENAME, retrying')
            
            except Exception as e:
               print(f'\nRaised exception: {e} (attempt {retry}/{MAX_RETRIES})')
      
      debug('duplication', 'Finished duplication process')
      
      # Add to book
      
      folderIds = self.client.getFolderByName(self.folderName)
      bookId: str = None
      
      if folderIds == []:
         # Create new book
         bookId = self.client.createFolder(self.folderName)
         
      else:
         # Get the first matching id
         bookId = folderIds[0]
      
      # Paste the books into the folder
      self.client.makeFolder2(bookId, createdBooksIds, self.folderName)
      
      debug('duplication', f'Moved books into folder {self.folderName}')
      
      # Finish
      self.finish()

   def start(self) -> None:
      '''
      Duplicates the books.
      '''
      
      self.clear()
      
      debug('dup', 'Duplication process started')
      
      info = tk.Label(self, textvariable = self.progress)
      cancel = tk.Button(self, text = 'Abort', command = self.abort)
      self.mainProgressBar = ttk.Progressbar(self)
      self.secondProgressBar = ttk.Progressbar(self)
      
      info.pack()
      self.secondProgressBar.pack()
      self.mainProgressBar.pack()
      cancel.pack()
      
      # Start duplication
      threading.Thread(target = self.duplicate).start()

   def finish(self) -> None:
      '''
      Shows a popup that informs the end of the process.
      '''
      
      def ent(*_) -> None: webbrowser.open_new('https://ent.iledefrance.fr/scrapbook')
      
      popup = tk.Toplevel(self)
      
      info = tk.Label(popup, text = 'The process has finished.')
      info2 = tk.Label(popup, text = 'You may now open/reload the ENT to see changes.')
      close = tk.Button(popup, text = 'Close', command = self.destroy)
      open = tk.Button(popup, text = 'Open ENT', command = ent)
      
      info.pack()
      info2.pack()
      close.pack()
      open.pack()


# = Main loop ====== #
if __name__ == '__main__':
   os.system('clear')
   debug('info', f'Started app from {__file__}')
   
   app = Main()
   app.title('TK-ENT')
   app.mainloop()

   debug('main', 'Closed app')
