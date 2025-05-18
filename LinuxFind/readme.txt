There will be a file class
This will have details like name, type, size and others if demanded
A flag which will denote whether it is a directory
And children list, which will contain the list of the files or directories this will contain if the above flag is set true


You'll have a filter interface, with abstract method apply(File)
Then youll have classes which will implement filters
1. Min size filter will have min size attribute and will impletment the apply function
2. Type filter will check for file type


Define a NotADirectoryException(Exception) class


Find command class will have two things

recurse(node, filters, output):
for each child of node
if the child is directory
call recurse on child
else apply filters if all(f.apply(file) for f in filters) and append to child

findWithFilters():
first check if the given folder is directory,
if not raise exception,
otherwise proceed and call recurse, and return output