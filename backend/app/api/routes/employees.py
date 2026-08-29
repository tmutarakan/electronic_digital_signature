import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Message,
    Employee,
    EmployeeCreate,
    EmployeePublic,
    EmployeesPublic,
    EmployeeUpdate,
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=EmployeesPublic)
def read_employees(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> EmployeesPublic:
    """
    Retrieve employees.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Employee)
        count = session.exec(count_statement).one()
        statement = (
            select(Employee)
            .order_by(col(Employee.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        employees = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Employee)
            .where(Employee.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Employee)
            .where(Employee.owner_id == current_user.id)
            .order_by(col(Employee.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        employees = session.exec(statement).all()

    employees_public = [
        EmployeePublic.model_validate(employee)
        for employee in employees
    ]
    return EmployeesPublic(data=employees_public, count=count)


@router.get("/{id}", response_model=EmployeePublic)
def read_employee(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Employee:
    """
    Get employee by ID.
    """
    employee = session.get(Employee, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if not current_user.is_superuser and (employee.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return employee


@router.post("/", response_model=EmployeePublic)
def create_employee(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    employee_in: EmployeeCreate,
) -> Employee:
    """
    Create new employee.
    """
    employee = Employee.model_validate(
        employee_in, update={"owner_id": current_user.id}
    )
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


@router.put("/{id}", response_model=EmployeePublic)
def update_employee(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    employee_in: EmployeeUpdate,
) -> Employee:
    """
    Update an employee.
    """
    employee = session.get(Employee, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if not current_user.is_superuser and (employee.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = employee_in.model_dump(exclude_unset=True)
    _ = employee.sqlmodel_update(update_dict | {"updated_at": datetime.now(ZoneInfo("Europe/Moscow"))})
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee


@router.delete("/{id}")
def delete_employee(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an employee.
    """
    employee = session.get(Employee, id)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    if not current_user.is_superuser and (employee.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(employee)
    session.commit()
    return Message(message="Employee deleted successfully")
