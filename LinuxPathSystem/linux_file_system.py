class FileNode:
  def __init__(self, is_file = False):
    self.is_file = is_file
    self.children = {}
    self.content = ""

class FileSystem:
  def __init__(self):
    self.root = FileNode()

  def _traverse(self, path: str) -> FileNode:
    parts = [p for p in path.split('/') if p]
    curr: FileNode = self.root
    for part in parts:
      if part not in curr.children:
        curr.children[part] = FileNode()
      curr = curr.children[part]
    return curr
  
  def mkdir(self, path: str):
    self._traverse(path)
    return f"Directory {path} created"
  
  def addContentToFile(self, file_path: str, content: str):
    parts =  file_path.split('/')
    *dirs, file_name = [p for p in parts if p]
    dir_path = '/' + '/'.join(dirs)

    parent = self._traverse(dir_path)
    if file_name not in parent.children:
      parent.children[file_name] = FileNode(is_file = True)
      file_node: FileNode = parent.children[file_name]
      file_node.content = content
  
  def readContentFromFile(self, filePath: str):
    parts = [p for p in filePath.split('/') if p]
    curr = self.root
    for part in parts:
      curr = curr.children[part]
    return curr.content

fs = FileSystem()

fs.mkdir("/a/b/c")

fs.addContentToFile("/a/b/c/d.txt", "Hello")
print(fs.readContentFromFile("/a/b/c/d.txt"))

fs.addContentToFile("/a/b/c/d.txt", "World")
print(fs.readContentFromFile("/a/b/c/d.txt"))