import uuid
from typing import Any

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import (
    CertificationCenter,
    CertificationCenterCreate,
    ElectronicDigitalSignature,
    ElectronicDigitalSignatureCreate,
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
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    _ = db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


# Dummy hash to use for timing attack prevention when user is not found
# This is an Argon2 hash of a random password, used to ensure constant-time comparison
DUMMY_HASH = "$argon2id$v=19$m=65536,t=3,p=4$MjQyZWE1MzBjYjJlZTI0Yw$YTU4NGM5ZTZmYjE2NzZlZjY0ZWY3ZGRkY2U2OWFjNjk"


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        # Prevent timing attacks by running password verification even when user doesn't exist
        # This ensures the response time is similar whether or not the email exists
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
    organization_id: uuid.UUID,
) -> Employee:
    db_employee = Employee.model_validate(
        employee_in, update={"owner_id": owner_id, "organization_id": organization_id}
    )
    session.add(db_employee)
    session.commit()
    session.refresh(db_employee)
    return db_employee


def create_electronic_digital_signature(
    *,
    session: Session,
    electronic_digital_signature_in: ElectronicDigitalSignatureCreate,
    owner_id: uuid.UUID,
) -> ElectronicDigitalSignature:
    db_electronic_digital_signature = ElectronicDigitalSignature.model_validate(
        electronic_digital_signature_in, update={"owner_id": owner_id}
    )
    session.add(db_electronic_digital_signature)
    session.commit()
    session.refresh(db_electronic_digital_signature)
    return db_electronic_digital_signature
