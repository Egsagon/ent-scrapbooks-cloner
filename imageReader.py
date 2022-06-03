'''
Module that creates a tk widget from an image url.
'''

from tkinter import Label, Tk
from PIL import Image, ImageTk
from urllib2 import urlopen
from io import BytesIO

class ImageWdg(object):
  def __init__(self, *args, url: str) -> None:
    '''
    Represents an image widget.
    '''
    
    # Open URL
    nav = urlopen(url)
    raw = nav.read()
    nav.close()
    
    # Create image
    image = Image.open(BytesIO(raw))
    photo = ImageTk.PhotoImage(image)
    
    # Build the widget
    return Label(*args, image = photo)

if __name__ == '__main__':
  root = Tk()
  url = 'https://ent.iledefrance.fr/workspace/document/861b0a56-35b9-4f4d-bff2-6a449d3f8b97?thumbnail=120x120&t=1654250758706'
  image = ImageWdg(root, url)
  image.pack()
  root.mainloop()
