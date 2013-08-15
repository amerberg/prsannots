# Copyright 2013 Adam Merberg
#
# This file is part of prsannots and is distributed under the terms of
# the LGPL license.  See the file COPYING for full details.

import os
import re
import fnmatch
import sqlite3
import generic
from xml.dom import minidom

PB_PEN, PB_HIGHLIGHT, PB_HIGHLIGHT_NOTE = "16", "32","64"

class Reader(generic.Reader):
    
    def __init__(self, path):
        generic.Reader.__init__(self, path)
        self.db = sqlite3.connect(os.path.join(path, 'system', 'explorer-2', 'explorer-2.db'))
        self.annotation_dir = os.path.join('system', 'config', 'Active Contents')
        self.path_prefix = '/mnt/ext1/'
    
    def _get_books(self):
        #c = self.db.cursor()
        #c.execute('''select books.id, books.title, books.path
        #                from books
        #                where books.ext = "pdf"''')
        books = []
        for annotation_file in os.listdir(os.path.join(self.path, self.annotation_dir)):
          try:
            if annotation_file.endswith('.html') and self._get_raw_path(annotation_file).endswith('.pdf'):
              books.append(Book(self, annotation_file))
          except:
            print "Unknown book {book}".format(book=annotation_file)
        
        return books
        
    def _get_raw_path(self, annotation_file_name):
      #open the annotation file
      with open(os.path.join(self.path, self.annotation_dir, annotation_file_name),'r') as annotation_file:     
        for line in annotation_file:
          match = re.match("\<!-- filepath=\"(([^\\0\\\"]|\\\\\")+)\".+--!\>", line)
          if match:
            return match.group(1)
      #TODO: handle errors
      
    def _convert_path(self, path):
      #convert a path on the device to a readable file path
      return path[len(self.path_prefix):]
      
class Book(generic.Book):
  
    def __init__(self, reader, annotation_file):
        self.annotation_file = annotation_file
        self.raw_path = reader._get_raw_path(annotation_file)
        file = reader._convert_path(self.raw_path)
        
        c = reader.db.cursor()
        c.execute('''select books.id, books.title
                        from books
                        where books.path = "{path}"'''.format(path=self.raw_path))
        row = c.fetchone()  
        generic.Book.__init__(self, reader, row[0], row[1], file, '')
    
    def _get_annotations(self):

        annotations = []
        with open(os.path.join(self.reader.path, self.reader.annotation_dir, self.annotation_file)) as annotation_file:    
          pattern = "\<!-- type=\"(\\d+)\".+\sposition=\"#pdfloc\([0-9a-f]+,(\d+)[\d,]*\)\"\sendposition=\"#pdfloc\([0-9a-f]+,[\d,]+\)\"(\ssvgpath=\"(([^\\0\\\"]|\\\\\")+))?\""
          for line in annotation_file:
            match = re.match(pattern, line)

            if match and match.group(1) == PB_PEN:
              #freehand
              page = match.group(2)
              svg_filename = match.group(4)
              svg_path = os.path.join(self.reader.annotation_dir, svg_filename)
              svg_dim = self._get_svg_dim(os.path.join(self.reader.path, svg_path))
              annotations.append(Freehand(self, page, svg_path, 0, 0, svg_dim[0], svg_dim[1], 1))
            
            elif match and match.group(1) == PB_HIGHLIGHT:
              #highlight
              page = match.group(2)
              highlight_line = annotation_file.readline()
              match = re.match("\>([^\>\<]*)\</div\>", highlight_line)
            
              if match:
                text = match.group(1)
              else:
                text = ""
              
              annotations.append(generic.Highlight(self, page, text, HIGHLIGHT))
        
            elif match and match.group(1) == PB_HIGHLIGHT_TEXT:
              #highlight with text
              page = match.group(2)
            
              highlight_line = annotation_file.readline()
              highlight_match = re.match("\>([^\>\<]*)\</font\>", highlight_line)
              if highlight_match:
                highlighted_text = highlight_match.group(1)
              else:
                highlighted_text = ""
            
              note_line = annotation_file.readline()
              note_match = re.match("\>([^\>\<]*)\</div\>", note_line)
            
              if note_match:
                note_text = note_match.group(1)
              else:
                note_text = ""
                           
              annotations.append(generic.Highlight(self, page, highlighted_text, HIGHLIGHT_TEXT, note_text))
        
        return annotations
        
    def _get_svg_dim(self, path):
        with open(path,'r') as svg_file:
          first = svg_file.readline()
          match = re.search("width=\"(\d+)\"\s+height=\"(\d+)\"", first)
          if match: 
            return match.group(1), match.group(2)
          
        return None
       
class Freehand(generic.Freehand):
    @property
    def svg(self):
      """The SVG associated with the annotation, as a minidom object."""
      if not hasattr(self, '_svg'):
          doc = minidom.parse(os.path.join(self.book.reader.path, self.svg_file))
          self._svg = doc.getElementsByTagNameNS('http://www.w3.org/2000/svg','svg')[0]
      return self._svg        

        