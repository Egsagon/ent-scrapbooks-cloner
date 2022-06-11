'''
'''

import os
import API
from tkinter import Label, Tk
from PIL import Image, ImageTk
from urllib.request import urlopen
from io import BytesIO

def saveImage(client: API.Connection, url: str, path: str) -> None:
  '''
  Save an image from an url.
  '''
  
  res = client.session.get(url)
  open(path, 'wb').write(res.content)


client = API.Connection('raphael.kern', input('pwd > '))
url = 'https://ent.iledefrance.fr/workspace/document/26ab40c4-9004-40e2-a116-d9a3669bbd12?thumbnail=120x120&t=1654328718338'

root = Tk()

img = Image(root, client, url)
img.pack()

root.mainloop()