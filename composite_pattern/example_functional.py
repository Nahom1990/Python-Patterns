from typing import Callable
from functools import reduce

# A component is just a function that takes nothing and evaluates to a salary.
SalaryEvalutor=Callable[[],float]

# Leaf Component (Closure representing an Employee)
def make_employee(name:str,salary:float)->SalaryEvalutor:
    def get_salary()->float:
        return float(salary)
    return get_salary

#composite commponent==> closure representing a Department

def make_department(name:str,*initial_components:SalaryEvalutor)->tuple[SalaryEvalutor,Callable[[SalaryEvalutor],None]]:
    """
    Creates a department closure.
    Returns a tuple of:
    - evaluator: Callable[[], float] -> calculates total salary
    - add_component: Callable[[SalaryEvaluator], None] -> appends a child evaluator
    """
    children:list[SalaryEvalutor]=list(initial_components)

    def get_salary()->float:
        return reduce(lambda total,child:total+child(),children,0.0)

    def add_component(component:SalaryEvalutor)->None:
        children.append(component)

    return get_salary,add_component

# Create leaf components (employees are simply functions)
employee1 = make_employee("Alice", 5000)
employee2 = make_employee("Bob", 6000)
charlie = make_employee("Charlie", 7000)

# Create the 'Backend' department
backend_salary, add_to_backend = make_department("Backend", employee1, employee2)

# Create the 'Engineering' department (nesting backend directly!)
engineering_salary, add_to_engineering = make_department("Engineering")

# Composite nesting: Add backend closure & charlie closure to engineering
add_to_engineering(backend_salary)
add_to_engineering(charlie)

# --- Verification ---
print(f"Backend Total Salary: ${backend_salary():,.2f}")          # 11,000.00
print(f"Engineering Total Salary: ${engineering_salary():,.2f}")  # 18,000.00





####PURE FUNCTIONAL WAY 

from typing import Union, Dict, Any, Sequence

# Immutable tree nodes as simple dictionaries/tuples
EmployeeData = dict[str, Any]
DepartmentData = dict[str, Any]
Node = Union[EmployeeData, DepartmentData]

# Constructors (Data only)
def create_employee(name: str, salary: float) -> EmployeeData:
    return {"type": "employee", "name": name, "salary": salary}

def create_department(name: str, children: Sequence[Node]) -> DepartmentData:
    return {"type": "department", "name": name, "children": children}

# Structural Recursion (Pattern matching over the tree)
def get_salary(node: Node) -> float:
    match node:
        case {"type": "employee", "salary": salary}:
            return float(salary)
        case {"type": "department", "children": children}:
            return sum(map(get_salary, children))
        case _:
            raise ValueError("Invalid node format")

# --- Usage ---
tree = create_department("Engineering", [
    create_department("Backend", [
        create_employee("Alice", 5000),
        create_employee("Bob", 6000),
    ]),
    create_employee("Charlie", 7000)
])

print(f"Total Tree Salary: ${get_salary(tree):,.2f}")  # 18,000.00