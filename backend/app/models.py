import uuid
from datetime import datetime
from pathlib import Path

from pydantic import EmailStr, computed_field
from sqlalchemy import DateTime
from sqlmodel import Field, Relationship, SQLModel

from app.core.s3 import generate_presigned_url

from .common import get_datetime_utc
from .mixins import IDMixin, TimestampsMixin


# Shared properties
class UserBase(SQLModel):
    """
    Базовые свойства пользователя.
    """
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    """
    Свойства для создания пользователя через API.
    """
    password: str = Field(min_length=8, max_length=128)


class UserRegister(SQLModel):
    """
    Свойства для регистрации пользователя через API.
    """
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(SQLModel):
    """
    Свойства для обновления пользователя через API.
    Все свойства являются необязательными.
    """
    email: EmailStr | None = Field(default=None, max_length=255)
    is_active: bool | None = None
    is_superuser: bool | None = None
    full_name: str | None = Field(default=None, max_length=255)
    password: str | None = Field(default=None, min_length=8, max_length=128)


class UserUpdateMe(SQLModel):
    """
    Свойства для обновления данных пользователя через API.
    Все свойства являются необязательными.
    """
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    """
    Свойства для обновления пароля пользователя через API.
    """
    current_password: str = Field(min_length=8, max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    """
    Модель пользователя в базе данных.
    """
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
    """
    Свойства для возврата пользователя через API.
    Всегда требуется идентификатор.
    """
    id: uuid.UUID
    created_at: datetime | None = None


class UsersPublic(SQLModel):
    """
    Свойства для возврата списка пользователей через API.
    """
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    """
    Базовые свойства элемента.
    """
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    """
    Свойства для создания элемента.
    """


# Properties to receive on item update
class ItemUpdate(SQLModel):
    """
    Свойства для обновления элемента.
    Все свойства являются необязательными.
    """
    title: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    """
    Модель элемента в базе данных.
    """
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
    """
    Свойства для возврата элемента через API.
    Всегда требуется идентификатор.
    """
    id: uuid.UUID
    owner_id: uuid.UUID
    created_at: datetime | None = None


class ItemsPublic(SQLModel):
    """
    Свойства для возврата списка элементов через API.
    """
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    """
    Общее сообщение.
    """
    message: str


# JSON payload containing access token
class Token(SQLModel):
    """
    Пакет данных, содержащий токен доступа.
    """
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    """
    Содержимое JWT токена.
    """
    sub: str | None = None


class NewPassword(SQLModel):
    """
    Пакет данных для обновления пароля.
    """
    token: str
    new_password: str = Field(min_length=8, max_length=128)


# --------------------------------------------------------------------------------
# Организации
# --------------------------------------------------------------------------------
class OrganizationBase(SQLModel):
    """
    Базовые свойства организации.
    """
    name: str = Field(min_length=1, max_length=255)


class OrganizationCreate(OrganizationBase):
    """
    Свойства для создания организации через API.
    """


class OrganizationUpdate(SQLModel):
    """
    Свойства для обновления организации через API.
    Все свойства являются необязательными.
    """
    name: str | None = Field(default=None, min_length=1, max_length=255)


class Organization(OrganizationBase, IDMixin, TimestampsMixin, table=True):
    """
    Модель организации в базе данных.
    """
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="organizations")  # pyright: ignore[reportAny]
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="organization", cascade_delete=True
    )


class OrganizationPublic(OrganizationBase):
    """
    Свойства для возврата организации через API.
    Всегда требуется идентификатор.
    """
    id: uuid.UUID
    owner: UserPublic
    created_at: datetime
    updated_at: datetime


class OrganizationsPublic(SQLModel):
    """
    Свойства для возврата списка организаций через API.
    """
    data: list[OrganizationPublic]
    count: int


# --------------------------------------------------------------------------------
# Удостоверяющий центр
# --------------------------------------------------------------------------------
class CertificationCenterBase(SQLModel):
    """
    Базовые свойства удостоверяющего центра.
    """
    name: str = Field(min_length=1, max_length=255)


class CertificationCenterCreate(CertificationCenterBase):
    """
    Свойства для создания удостоверяющего центра через API.
    """


class CertificationCenterUpdate(SQLModel):
    """
    Свойства для обновления удостоверяющего центра через API.
    Все свойства являются необязательными.
    """
    name: str | None = Field(default=None, min_length=1, max_length=255)


class CertificationCenter(
    CertificationCenterBase, IDMixin, TimestampsMixin, table=True
):
    """
    Модель удостоверяющего центра в базе данных.
    """
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="certification_centers")  # pyright: ignore[reportAny]
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="certification_center", cascade_delete=True
    )


class CertificationCenterPublic(CertificationCenterBase):
    """
    Свойства для возврата удостоверяющего центра через API.
    Всегда требуется идентификатор.
    """
    id: uuid.UUID
    owner: UserPublic
    created_at: datetime
    updated_at: datetime


class CertificationCentersPublic(SQLModel):
    """
    Свойства для возврата списка удостоверяющих центров через API.
    """
    data: list[CertificationCenterPublic]
    count: int


# --------------------------------------------------------------------------------
# Тип подписи
# --------------------------------------------------------------------------------
class SignatureTypeBase(SQLModel):
    """
    Базовые свойства типа подписи.
    """
    name: str = Field(min_length=1, max_length=255)


class SignatureTypeCreate(SignatureTypeBase):
    """
    Свойства для создания типа подписи через API.
    """


class SignatureTypeUpdate(SQLModel):
    """
    Свойства для обновления типа подписи через API.
    Все свойства являются необязательными.
    """
    name: str | None = Field(default=None, min_length=1, max_length=255)


class SignatureType(SignatureTypeBase, IDMixin, TimestampsMixin, table=True):
    """
    Модель типа подписи в базе данных.
    """
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="signature_types")  # pyright: ignore[reportAny]
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="signature_type", cascade_delete=True
    )


class SignatureTypePublic(SignatureTypeBase):
    """
    Свойства для возврата типа подписи через API.
    Всегда требуется идентификатор.
    """
    id: uuid.UUID
    owner: UserPublic
    created_at: datetime
    updated_at: datetime


class SignatureTypesPublic(SQLModel):
    """
    Свойства для возврата списка типов подписи через API.
    """
    data: list[SignatureTypePublic]
    count: int


# --------------------------------------------------------------------------------
# Сотрудники
# --------------------------------------------------------------------------------
class EmployeeBase(SQLModel):
    """
    Базовые свойства сотрудника.
    """
    name: str = Field(min_length=1, max_length=255)
    position: str = Field(min_length=1, max_length=255)


class EmployeeCreate(EmployeeBase): ...


class EmployeeUpdate(SQLModel):
    """
    Свойства для обновления сотрудника через API.
    Все свойства являются необязательными.
    """
    name: str | None = Field(default=None, min_length=1, max_length=255)
    position: str | None = Field(default=None, min_length=1, max_length=255)


class Employee(EmployeeBase, IDMixin, TimestampsMixin, table=True):
    """
    Модель сотрудника в базе данных.
    """
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE", index=True
    )
    owner: User = Relationship(back_populates="employees")  # pyright: ignore[reportAny]
    electronic_digital_signatures: list[ElectronicDigitalSignature] = Relationship(  # pyright: ignore[reportAny]
        back_populates="employee", cascade_delete=True
    )


class EmployeePublic(EmployeeBase):
    """
    Свойства для возврата сотрудника через API.
    Всегда требуется идентификатор.
    """
    id: uuid.UUID
    owner: UserPublic
    created_at: datetime
    updated_at: datetime


class EmployeesPublic(SQLModel):
    """
    Свойства для возврата списка сотрудников через API.
    """
    data: list[EmployeePublic]
    count: int


# --------------------------------------------------------------------------------
# Электронная цифровая подпись
# --------------------------------------------------------------------------------
class ElectronicDigitalSignatureBase(SQLModel):
    """
    Базовые свойства электронной цифровой подписи.
    """
    date_certificate: datetime = Field(
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
        description="Дата окончания срока действия сертификата",
    )
    date_container: datetime = Field(
        sa_type=DateTime(timezone=True),  # pyright: ignore[reportArgumentType]
        description="Дата окончания срока действия контейнера",
    )


class ElectronicDigitalSignatureCreate(ElectronicDigitalSignatureBase):
    """
    Свойства для создания электронной цифровой подписи через API.
    """
    organization_id: uuid.UUID
    signature_type_id: uuid.UUID
    employee_id: uuid.UUID
    certification_center_id: uuid.UUID
    file_certificate: str = Field(max_length=1024, nullable=False)
    file_container: str = Field(max_length=1024, nullable=False)


class ElectronicDigitalSignatureUpdate(SQLModel):
    """
    Свойства для обновления электронной цифровой подписи через API.
    Все свойства являются необязательными.
    """
    date_certificate: datetime | None = None
    date_container: datetime | None = None
    organization_id: uuid.UUID | None = None
    signature_type_id: uuid.UUID | None = None
    employee_id: uuid.UUID | None = None
    certification_center_id: uuid.UUID | None = None


class ElectronicDigitalSignature(
    ElectronicDigitalSignatureBase, IDMixin, TimestampsMixin, table=True
):
    """
    Модель электронной цифровой подписи в базе данных.
    """
    file_certificate: str = Field(max_length=1024, nullable=False)
    file_container: str = Field(max_length=1024, nullable=False)

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
        foreign_key="employee.id", nullable=False, ondelete="CASCADE"
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
    """
    Свойства для возврата электронной цифровой подписи через API.
    Всегда требуется идентификатор.
    """
    id: uuid.UUID
    file_certificate: str
    file_container: str
    owner: UserPublic
    organization: OrganizationPublic
    signature_type: SignatureTypePublic
    employee: EmployeePublic
    certification_center: CertificationCenterPublic
    created_at: datetime
    updated_at: datetime

    @computed_field
    @property
    def certificate_url(self) -> str:
        ext = Path(self.file_certificate).suffix
        return generate_presigned_url(
            self.file_certificate,
            filename=f"certificate_{self.id}{ext}",
        )

    @computed_field
    @property
    def container_url(self) -> str:
        ext = Path(self.file_container).suffix
        return generate_presigned_url(
            self.file_container,
            filename=f"container_{self.id}{ext}",
        )


class ElectronicDigitalSignaturesPublic(SQLModel):
    """
    Свойства для возврата списка электронных цифровых подписей через API.
    """
    data: list[ElectronicDigitalSignaturePublic]
    count: int
