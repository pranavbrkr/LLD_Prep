from typing import Optional, List, Dict

class Employee:
  def __init__(self, id: int, name: str, manager_id: Optional[int]):
    self.id = id
    self.name = name
    self.manager_id = manager_id

  def __repr__(self):
    return f"Employee(id = {self.id}, name = {self.name}, manager_id = {self.manager_id})"
  
class OrgChart:
  def __init__(self):
    self.employees: Dict[int, Employee] = {}
    self.manager_to_reportees: Dict[int, List[int]] = {}
  
  def addEmployee(self, id: int, name: str, manager_id: Optional[int]):
    if id in self.employees:
      print(f"Employee with id {id} already exists")
      return
    
    emp = Employee(id, name, manager_id)
    self.employees[id] = emp
    if manager_id is not None:
      self.manager_to_reportees.setdefault(manager_id, []).append(id)
  
  def getManager(self, employee_id: int):
    emp = self.employees.get(employee_id)

    if not emp:
      print(f"Employee with id {emp.id} not found")
      return None

    if emp.manager_id is None:
      print(f"Employee {emp.name} has no manager")
      return None

    return self.employees.get(emp.manager_id)
  
  def getManagerChain(self, employee_id: id) -> List[Employee]:
    chain = []
    current = self.employees.get(employee_id)

    while current and current.manager_id is not None:
      manager = self.employees.get(current.manager_id)
      if manager:
        chain.append(manager)
        current = manager
      else:
        break
    return chain
  
  def reassignManager(self, employee_id: int, new_manager_id: Optional[int]):
    emp = self.employees.get(employee_id)

    if not emp:
      print(f"Employee with id {employee_id} not found")
      return
    
    old_manager_id = emp.manager_id

    if old_manager_id is not None and old_manager_id in self.manager_to_reportees:
      if employee_id in self.manager_to_reportees[old_manager_id]:
        self.manager_to_reportees[old_manager_id].remove(employee_id)
    
    emp.manager_id = new_manager_id

    if new_manager_id is not None:
      self.manager_to_reportees.setdefault(new_manager_id, []).append(employee_id)
  
  def printOrgChart(self):
    print("Org Chart:")
    for manager_id, reportees in self.manager_to_reportees.items():
      manager_name = self.employees[manager_id].name if manager_id in self.employees else "Unknown"
      reportee_names = [self.employees[emp_id].name for emp_id in reportees]
      print(f"Manager {manager_name} ({manager_id}): {reportee_names}")


if __name__ == "__main__":
  org = OrgChart()
  org.addEmployee(1, "Alice", None)
  org.addEmployee(2, "Bob", 1)
  org.addEmployee(3, "Charlie", 1)
  org.addEmployee(4, "David", 2)
  org.addEmployee(5, "Eve", 2)

  manager = org.getManager(4)

  print(f"David's manager: {manager}")

  chain = org.getManagerChain(4)
  print(f"David's manager chain: {[m.name for m in chain]}")

  org.reassignManager(4, 1)
  manager = org.getManager(4)
  print(f"David's new manager: {manager}")

  
  org.printOrgChart()