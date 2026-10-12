import uuid

from fastapi import APIRouter

from app import crud
from app.api.deps import CurrentUser, SessionDep, SuperUser
from app.models import (
    Employee,
    EmployeeCreate,
    EmployeePublic,
    EmployeesPublic,
    EmployeeUpdate,
    Message,
)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=EmployeesPublic)
def read_employees(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> EmployeesPublic:
    """
    Retrieve employees. Доступно всем аутентифицированным пользователям.
    """
    items, count = crud.list_all(session, Employee, skip, limit)
    return EmployeesPublic(
        data=[EmployeePublic.model_validate(x) for x in items],
        count=count,
    )


@router.get("/{id}", response_model=EmployeePublic)
def read_employee(
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
) -> Employee:
    """
    Get employee by ID. Доступно всем аутентифицированным пользователям.
    """
    return crud.get_or_404(session, Employee, id)


@router.post("/", response_model=EmployeePublic)
def create_employee(
    *,
    session: SessionDep,
    current_user: SuperUser,
    employee_in: EmployeeCreate,
) -> Employee:
    """
    Create new employee. Только для суперпользователя.
    """
    return crud.create_employee(
        session=session,
        employee_in=employee_in,
        owner_id=current_user.id,
    )


@router.put("/{id}", response_model=EmployeePublic)
def update_employee(
    *,
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
    employee_in: EmployeeUpdate,
) -> Employee:
    """
    Update an employee. Только для суперпользователя.
    """
    employee = crud.get_or_404(session, Employee, id)
    return crud.update_obj(session, employee, employee_in)


@router.delete("/{id}")
def delete_employee(
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
) -> Message:
    """
    Delete an employee. Только для суперпользователя.
    """
    employee = crud.get_or_404(session, Employee, id)
    session.delete(employee)
    session.commit()
    return Message(message="Employee deleted successfully")
