Employee class will have name, id and manager id
This will only have __repr_

Org chart class will have two dictionaries
employees: id -> Employee object
manager_to_reportees: manager id -> list of employee ids

Behaviors would be

1. addEmployee(name, manager id)
Create employee object
Add object to employees dictionary
Append that employee id to manager_to_reportees dictionary for the appropriate manager


2. getManager(employee id)
Fetch employee object using employee id
If manager id is None, state that
Get the manager object from the employees dictionary using manager id


3. getManagerChain(employee id)
set current as employee id
while current and current manager is not None
get manager object using manager id, if it exists, append to chain else break
return chain


4. reassignManager(employee id, manager id)
save old manager id
if old manager id is manager_to_reportees dictionary, if employee in manager_to_reportees[old manager id], remove the employee id from that list
set employee.manager_id to new manager id
Add the employee id to manager_to_reportees[new manager id] list


5. printOrgChart()
Iterate through manager_to_reportees items() and get manager name, reportee names in an array and display those