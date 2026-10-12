import uuid

from fastapi import HTTPException
from sqlmodel import Session, SQLModel, col, func, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    CertificationCenter,
    CertificationCenterCreate,
    Employee,
    EmployeeCreate,
    Item,
    ItemCreate,
    Organization,
    OrganizationCreate,
    SignatureType,
    SignatureTypeCreate,
    User,
    UserCreate,
    UserUpdate,
)

# ---------- Users ----------


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> User:
    user_data: dict[str, str] = user_in.model_dump(exclude_unset=True)
    extra_data: dict[str, str] = {}
    if "password" in user_data:
        password: str = user_data["password"]
        extra_data["hashed_password"] = get_password_hash(password)
    _ = db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    return session.exec(select(User).where(User.email == email)).first()


DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        _ = verify_password(password, DUMMY_HASH)
        return None
    verified, updated_password_hash = verify_password(password, db_user.hashed_password)
    if not verified:
        return None
    if updated_password_hash:
        db_user.hashed_password = updated_password_hash
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
    return db_user


# ---------- Общие хелперы чтения ----------


def get_or_404[ModelT: SQLModel](
    session: Session, model: type[ModelT], id: uuid.UUID
) -> ModelT:
    """Получить запись по ID или 404. Без проверки прав (для справочников)."""
    obj = session.get(model, id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} not found")
    return obj


def list_all[ModelT: SQLModel](
    session: Session, model: type[ModelT], skip: int = 0, limit: int = 100
) -> tuple[list[ModelT], int]:
    """Список всех записей (для справочников)."""
    count = session.exec(select(func.count()).select_from(model)).one()
    statement = (
        select(model)
        .order_by(col(model.created_at).desc()) # pyright:ignore[reportAttributeAccessIssue]
        .offset(skip)
        .limit(limit)
    )
    return list(session.exec(statement).all()), count


# ---------- Общие хелперы записи ----------


def update_obj[ModelT: SQLModel](
    session: Session, obj: ModelT, update_in: SQLModel
) -> ModelT:
    """Частичное обновление объекта по схеме с exclude_unset."""
    obj.sqlmodel_update(update_in.model_dump(exclude_unset=True))
    session.add(obj)
    session.commit()
    session.refresh(obj)
    return obj


def delete_obj(session: Session, obj: SQLModel) -> None:
    """Удаление объекта."""
    session.delete(obj)
    session.commit()


# ---------- Создание сущностей ----------


def create_item(*, session: Session, item_in: ItemCreate, owner_id: uuid.UUID) -> Item:
    db_item = Item.model_validate(item_in, update={"owner_id": owner_id})
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


def create_organization(
    *, session: Session, organization_in: OrganizationCreate, owner_id: uuid.UUID
) -> Organization:
    db_organization = Organization.model_validate(
        organization_in, update={"owner_id": owner_id}
    )
    session.add(db_organization)
    session.commit()
    session.refresh(db_organization)
    return db_organization


def create_certification_center(
    *,
    session: Session,
    certification_center_in: CertificationCenterCreate,
    owner_id: uuid.UUID,
) -> CertificationCenter:
    db_certification_center = CertificationCenter.model_validate(
        certification_center_in, update={"owner_id": owner_id}
    )
    session.add(db_certification_center)
    session.commit()
    session.refresh(db_certification_center)
    return db_certification_center


def create_signature_type(
    *, session: Session, signature_type_in: SignatureTypeCreate, owner_id: uuid.UUID
) -> SignatureType:
    db_signature_type = SignatureType.model_validate(
        signature_type_in, update={"owner_id": owner_id}
    )
    session.add(db_signature_type)
    session.commit()
    session.refresh(db_signature_type)
    return db_signature_type


def create_employee(
    *,
    session: Session,
    employee_in: EmployeeCreate,
    owner_id: uuid.UUID,
) -> Employee:
    db_employee = Employee.model_validate(employee_in, update={"owner_id": owner_id})
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee
