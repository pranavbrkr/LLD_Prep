from abc import ABC, abstractmethod
from typing import List, Optional
from enum import Enum

class FileType(Enum):
  DIRECTORY = 0
  TEXT = 1
  LOG = 2
  BINARY = 3

class File:
  def __init__(self, name, size, file_type, is_directory = False, children: Optional[List["File"]] = None):
    self.name = name
    self.size = size
    self.file_type = file_type
    self.is_directory = is_directory
    self.children = children or []
  
  def __repr__(self):
    return f"<Name: {self.name}, size: {self.size}, file_type: {self.file_type.name}>"
  
class Filter(ABC):
  @abstractmethod
  def apply(self, file: File):
    pass

class MinSizeFilter(Filter):
  def __init__(self, min_size):
    self.min_size = min_size

  def apply(self, file: File):
    return self.min_size <= file.size
  
class FileTypeFilter(Filter):
  def __init__(self, file_type):
    self.file_type = file_type
  
  def apply(self, file: File):
    return file.file_type == self.file_type

class NotADirectory(Exception):
  pass

class FindCommand:
  def findWithFilters(self, directory: File, filters: List[Filter]):
    if not directory.is_directory:
      raise NotADirectory(f"{directory.name} is not a directory")
    output = []
    self.recurse(directory, filters, output)
    return output
  
  def recurse(self, node: File, filters: List[Filter], output: List[File]):
    for child in node.children:
      if child.is_directory:
        self.recurse(child, filters, output)
      else:
        if all(filter.apply(child) for filter in filters):
          output.append(child)

if __name__ == "__main__":
  root = File("root", 0, FileType.DIRECTORY, True, [
    File("a.txt", 1000, FileType.TEXT),
    File("b.log", 800, FileType.LOG),
    File("c.bin", 600, FileType.BINARY),
    File("sub_dir", 0, FileType.DIRECTORY, True, [
      File("d.log", 1100, FileType.LOG),
      File("e.txt", 110, FileType.TEXT),
    ])
  ])

  cmd = FindCommand()
  filters = [MinSizeFilter(400), FileTypeFilter(FileType.LOG)]

  matches = cmd.findWithFilters(root, filters)
  print(matches)