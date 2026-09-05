import uuid
from datetime import datetime

from pydantic import EmailStr, field_validator
from sqlalchemy import DateTime, LargeBinary, Text
from sqlmodel import Column, Field, Relationship, SQLModel

from .common import get_datetime_utc
from .mixins import IDMixin, TimestampsMixin


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
    )
    items: list[Item] = Relationship(back_populates="owner", cascade_delete=True)  # pyright: ignore[reportAny]
    organizations: list[Organization] = Relationship(  # pyright: ignore[reportAny]
        back_populates="owner", cascade_delete=True
    )
    certification_centers: list[CertificationCenter] = Relationship(  # pyright: ignore[reportAny]
        back_populates="owner", cascade_delete=True
    )
    signature_types: list[SignatureType] = Relationship(  # pyright: ignore[reportAny]
        back_populates="owner", cascade_delete=True
    )
    employees: list[Employee] = Relationship(  # pyright: ignore[reportAny]
        back_populates="owner", cascade_delete=True
    )
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="owner", cascade_delete=True
    )


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    pass


# Properties to receive on item update
class ItemUpdate(SQLModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    created_at: datetime | None = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
    )
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User | None = Relationship(back_populates="items")  # pyright: ignore[reportAny]


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# --------------------------------------------------------------------------------
# Организации
# --------------------------------------------------------------------------------
class OrganizationBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class Organization(OrganizationBase, IDMixin, TimestampsMixin, table=True):
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="organizations")  # pyright: ignore[reportAny]
    employees: list[Employee] = Relationship(  # pyright: ignore[reportAny]
        back_populates="organization", cascade_delete=True
    )
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="organization", cascade_delete=True
    )


class OrganizationPublic(OrganizationBase):
    id: uuid.UUID
    owner: UserPublic
    created_at: datetime
    updated_at: datetime


class OrganizationsPublic(SQLModel):
    data: list[OrganizationPublic]
    count: int


# --------------------------------------------------------------------------------
# Удостоверяющий центр
# --------------------------------------------------------------------------------
class CertificationCenterBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class CertificationCenterCreate(CertificationCenterBase):
    pass


class CertificationCenterUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class CertificationCenter(
    CertificationCenterBase, IDMixin, TimestampsMixin, table=True
):
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="certification_centers")  # pyright: ignore[reportAny]
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="certification_center", cascade_delete=True
    )


class CertificationCenterPublic(CertificationCenterBase):
    id: uuid.UUID
    owner: UserPublic
    created_at: datetime
    updated_at: datetime


class CertificationCentersPublic(SQLModel):
    data: list[CertificationCenterPublic]
    count: int


# --------------------------------------------------------------------------------
# Тип подписи
# --------------------------------------------------------------------------------
class SignatureTypeBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)


class SignatureTypeCreate(SignatureTypeBase):
    pass


class SignatureTypeUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)


class SignatureType(SignatureTypeBase, IDMixin, TimestampsMixin, table=True):
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="signature_types")  # pyright: ignore[reportAny]
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="signature_type", cascade_delete=True
    )


class SignatureTypePublic(SignatureTypeBase):
    id: uuid.UUID
    owner: UserPublic
    created_at: datetime
    updated_at: datetime


class SignatureTypesPublic(SQLModel):
    data: list[SignatureTypePublic]
    count: int


# --------------------------------------------------------------------------------
# Сотрудники
# --------------------------------------------------------------------------------
class EmployeeBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    position: str = Field(min_length=1, max_length=255)


class EmployeeCreate(EmployeeBase):
    organization_id: uuid.UUID


class EmployeeUpdate(SQLModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    position: str | None = Field(default=None, min_length=1, max_length=255)


class Employee(EmployeeBase, IDMixin, TimestampsMixin, table=True):
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE", index=True
    )
    owner: User = Relationship(back_populates="employees")  # pyright: ignore[reportAny]
    organization_id: uuid.UUID = Field(
        foreign_key="organization.id", nullable=False, ondelete="CASCADE", index=True
    )
    organization: Organization | None = Relationship(back_populates="employees")  # pyright: ignore[reportAny]
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="employee", cascade_delete=True
    )


class EmployeePublic(EmployeeBase):
    id: uuid.UUID
    owner: UserPublic
    organization: OrganizationPublic
    created_at: datetime
    updated_at: datetime


class EmployeesPublic(SQLModel):
    data: list[EmployeePublic]
    count: int


# --------------------------------------------------------------------------------
# Электронная цифровая подпись
# --------------------------------------------------------------------------------
class ElectronicDigitalSignatureBase(SQLModel):
    date_certificate: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
        description="Дата окончания срока действия сертификата",
    )
    file_certificate: str = Field(
        sa_column=Column(Text), description="Сертификат в формате Base64"
    )
    date_container: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
        description="Дата окончания срока действия контейнера",
    )
    file_container: str = Field(
        sa_column=Column(Text), description="Контейнер в формате Base64"
    )


class ElectronicDigitalSignatureCreate(ElectronicDigitalSignatureBase):
    organization_id: uuid.UUID
    signature_type_id: uuid.UUID
    employee_id: uuid.UUID | None = None
    certification_center_id: uuid.UUID


class ElectronicDigitalSignatureUpdate(SQLModel):
    date_certificate: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
    )
    file_certificate: bytes = Field(sa_column=Column(LargeBinary))
    date_container: datetime = Field(
        default_factory=get_datetime_utc,
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
    )
    file_container: bytes = Field(sa_column=Column(LargeBinary))


class ElectronicDigitalSignature(
    ElectronicDigitalSignatureBase, IDMixin, TimestampsMixin, table=True
):
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="electronic_digital_signatures")  # pyright: ignore[reportAny]
    organization_id: uuid.UUID = Field(
        foreign_key="organization.id", nullable=False, ondelete="CASCADE"
    )
    organization: Organization | None = Relationship(  # pyright: ignore[reportAny]
        back_populates="electronic_digital_signatures"
    )
    signature_type_id: uuid.UUID = Field(
        foreign_key="signaturetype.id", nullable=False, ondelete="CASCADE"
    )
    signature_type: SignatureType | None = Relationship(  # pyright: ignore[reportAny]
        back_populates="electronic_digital_signatures"
    )
    employee_id: uuid.UUID = Field(
        foreign_key="employee.id", nullable=True, ondelete="CASCADE"
    )
    employee: Employee | None = Relationship(  # pyright: ignore[reportAny]
        back_populates="electronic_digital_signatures"
    )
    certification_center_id: uuid.UUID = Field(
        foreign_key="certificationcenter.id", nullable=False, ondelete="CASCADE"
    )
    certification_center: CertificationCenter | None = Relationship(  # pyright: ignore[reportAny]
        back_populates="electronic_digital_signatures"
    )


class ElectronicDigitalSignaturePublic(ElectronicDigitalSignatureBase):
    id: uuid.UUID
    owner: UserPublic
    organization: OrganizationPublic
    signature_type: SignatureTypePublic
    employee: EmployeePublic
    certification_center: CertificationCenterPublic
    created_at: datetime
    updated_at: datetime


class ElectronicDigitalSignaturesPublic(SQLModel):
    data: list[ElectronicDigitalSignaturePublic]
    count: int
