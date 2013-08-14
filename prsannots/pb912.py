# Copyright 2013 Adam Merberg
#
# This file is part of prsannots and is distributed under the terms of
# the LGPL license.  See the file COPYING for full details.

import os
import re
import fnmatch
import sqlite3
import generic

PB_PEN, PB_HIGHLIGHT, PB_HIGHLIGHT_NOTE = "16", "32","64"

class Reader(generic.Reader):
    
    def __init__(self, path):
        generic.Reader.__init__(self, path)
        self.db = sqlite3.connect(os.path.join(path, 'system', 'explorer-2', 'explorer-2.db'))
        self.annotation_path = os.path.join(path, 'system', 'config', 'Active Contents')
        self.path_prefix = '/mnt/ext1'
    
    def _get_books(self):
        #c = self.db.cursor()
        #c.execute('''select books.id, books.title, books.path
        #                from books
        #                where books.ext = "pdf"''')
        books = []
        for annotation_file in os.listdir(self.annotation_path)
          if annotation_file.endswith('.html') && self._get_raw_path(annotation_file).endswith('.pdf')
            books[] = Book(self, reader, annotation_file)
        
        return books
        
    def _get_raw_path(self, annotation_file_name):
      #open the annotation file
      annotation_file = open(os.path.join(self.path, annotation_file_name),'r')
      
      for line in file
        match = re.match("\<!-- filepath=\"(([^\\0\\\"]|\\\\\")+)\".+--!\>", line)
        if match
          return match.group(1)
      #throw an exception
      
    def _convert_path(self, path):
      #convert a path on the device to a readable file path
      return os.path.join(self.path, path[len(self.path_prefix):])
      
class Book(generic.Book):
  
    def __init__(self, reader, annotation_file):
        #open
        self.annotation_file = annotation_file
        self.raw_path = self.reader._get_raw_path(annotation_file)
        self.file_path = self.reader._convert_path(self.raw_path)
        
        c = self.reader.db.cursor()
        c.execute('''select books.id, books.title
                        from books
                        where books.path = "{path}"'''.format(path=self.raw_path))
        row = c.fetchone()  
        
        generic.Book.__init__(self, reader, row[0], row[1], self.file_path, None)
    
    def _get_annotations(self):

        annotation_file_name = self._get_annotation_file()
        annotations = []
        annotation_file = open(os.path.join(annotation_file_path, annotation_file_name))
        
        while line = annotation_file.readline()
          #TODO: optionally include the svg path in the following
          match = re.match("\<!-- type=\"(\\d+)\".+\sposition=\"#pdfloc\([0-9a-f]+,(\d+)[\d,]*\)\"\sendposition=\"#pdfloc\([0-9a-f]+,[\d,]+\)\"(\ssvgpath=\"(([^\\0\\\"]|\\\\\")+))?\"")
          if match && match.group(1) == PB_PEN
            #freehand
            page = match.group(2)
            svg_filename = match.group(4)
            svg_path = os.path.join(annotation_file_path, svg_filename)
            svg_dim = self._get_svg_dim(svg_path)
            annotations[] = generic.Freehand(self, page, svg_path, 0, 0, svg_dim[1], svg_dim[2], 1)
          else if match && match.group(2) == PB_HIGHLIGHT
            #highlight
            page = match.group(2)
            highlight_line = annotation_file.readline()
            match = re.match("\>([^\>\<]*)\</div\>")
            if match
              text = match.group(1)
            else
              text = ""
            annotations[] = generic.Highlight(self, page, text, HIGHLIGHT)
        else if match && match.group(2) == PB_HIGHLIGHT_TEXT
            #highlight with text
            page = match.group(2)
            
            highlight_line = annotation_file.readline()
            highlight_match = re.match("\>([^\>\<]*)\</font\>")
            if highlight_match
              highlighted_text = highlight_match.group(1)
            else
              highlighted_text = ""
            
            note_line = annotation_file.readline()
            note_match = re.match("\>([^\>\<]*)\</div\>")
            if note_match
              note_text = note_match.group(1)
            else
              note_text = ""              
            annotations[] = generic.Highlight(self, page, highlighted_text, HIGHLIGHT_TEXT, note_text)           
        
        return annotations
        
    def _get_svg_dim(self, path):
        svg_file = open(path,'r')
        first = svg_file.readline()
        match = re.match("width=\"(\d+)\"\s+height=\"(\d+)\"")
        if match 
          return match.group(1), match.group(2)
          
        return None
       
      

        