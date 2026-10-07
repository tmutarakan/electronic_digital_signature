"""
Скрипт для заполнения базы тестовыми данными (синхронный).

Запуск:
    python -m app.scripts.seed

Опции (через env):
    SEED_RESET=1   — удалить все данные перед заполнением
"""

import io
import logging
import os
import random
import uuid
from collections.abc import Sequence, Iterable
from datetime import datetime, timedelta, timezone

from botocore.exceptions import ClientError
from faker import Faker
from sqlmodel import Session, create_engine, select

from app.core.config import settings
from app.core.s3 import s3_client
from app.core.security import get_password_hash
from app.models import (
    CertificationCenter,
    ElectronicDigitalSignature,
    Employee,
    Item,
    Organization,
    SignatureType,
    User,
)

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("seed")

fake = Faker("ru_RU")
Faker.seed(42)
random.seed(42)

RESET = os.getenv("SEED_RESET", "0") == "1"
UPLOAD_S3 = os.getenv("SEED_S3", "1") == "1"

# -----------------------------------------------------------------------------
# Движок
# -----------------------------------------------------------------------------
engine = create_engine(str(settings.DATABASE_URL), echo=False)


# -----------------------------------------------------------------------------
# S3 / MinIO клиент
# -----------------------------------------------------------------------------
def upload_fake_file(
    client,
    bucket: str,
    key: str,
    content: bytes,
    content_type: str = "application/octet-stream",
) -> None:
    """Загружает байты в S3/MinIO."""
    try:
        client.put_object(
            Bucket=bucket,
            Key=key,
            Body=io.BytesIO(content),
            ContentType=content_type,
        )
        logger.debug("Загружен %s", key)
    except ClientError as e:
        logger.error("Ошибка загрузки %s: %s", key, e)
        raise


# -----------------------------------------------------------------------------
# Хелперы
# -----------------------------------------------------------------------------
def get_or_create(session: Session, model, defaults: dict | None = None, **kwargs):
    """Возвращает существующую запись или создаёт новую."""
    stmt = select(model)
    for k, v in kwargs.items():
        stmt = stmt.where(getattr(model, k) == v)
    obj = session.exec(stmt).first()
    if obj:
        return obj, False
    obj = model(**{**kwargs, **(defaults or {})})
    session.add(obj)
    session.flush()
    return obj, True


def fake_datetime(days_from_now: int = 365) -> datetime:
    """Случайная дата в будущем (для сертификатов/контейнеров)."""
    delta = timedelta(days=random.randint(30, days_from_now))
    return datetime.now(timezone.utc) + delta


# -----------------------------------------------------------------------------
# Очистка
# -----------------------------------------------------------------------------
def reset_db(session: Session) -> None:
    logger.warning("SEED_RESET=1 — удаляю все данные...")
    # Порядок важен: сначала дочерние таблицы
    for model in (
        ElectronicDigitalSignature,
        Employee,
        SignatureType,
        CertificationCenter,
        Organization,
        Item,
        User,
    ):
        for row in session.exec(select(model)).all():
            session.delete(row)
    session.commit()
    logger.info("База очищена.")


# -----------------------------------------------------------------------------
# Пользователи
# -----------------------------------------------------------------------------
def seed_users(session: Session) -> list[User]:
    users_data = [
        {
            "email": "nonadmin@example.com",
            "password": "noadmin12345",
            "full_name": "Не Администратор Системы",
            "is_superuser": False,
            "is_active": True,
        },
        {
            "email": "user@example.com",
            "password": "user12345",
            "full_name": "Иван Иванов",
            "is_superuser": False,
            "is_active": True,
        },
        {
            "email": "petrova@example.com",
            "password": "petrova12345",
            "full_name": "Мария Петрова",
            "is_superuser": False,
            "is_active": True,
        },
    ]

    users: list[User] = []
    for data in users_data:
        user, created = get_or_create(
            session,
            User,
            email=data["email"],
            defaults={
                "hashed_password": get_password_hash(data["password"]),
                "full_name": data["full_name"],
                "is_superuser": data["is_superuser"],
                "is_active": data["is_active"],
            },
        )
        users.append(user)
        logger.info(
            "Пользователь %s %s",
            data["email"],
            "создан" if created else "уже есть",
        )

    session.commit()
    return users


# -----------------------------------------------------------------------------
# Items (демо из шаблона)
# -----------------------------------------------------------------------------
def seed_items(session: Session, owner: User) -> None:
    for i in range(1, 6):
        _, created = get_or_create(
            session,
            Item,
            title=f"Тестовый элемент #{i}",
            owner_id=owner.id,
            defaults={"description": fake.sentence(nb_words=10)},
        )
        if created:
            logger.info("Item #%d создан", i)
    session.commit()


# -----------------------------------------------------------------------------
# Организации
# -----------------------------------------------------------------------------
def seed_organizations(session: Session, owner: User) -> list[Organization]:
    names = [
        "ООО «Ромашка»",
        "АО «ТехноСофт»",
        "ИП Сидоров А.А.",
    ]
    orgs: list[Organization] = []
    for name in names:
        org, created = get_or_create(
            session, Organization, name=name, owner_id=owner.id
        )
        orgs.append(org)
        logger.info("Организация %s %s", name, "создана" if created else "уже есть")
    session.commit()
    return orgs


# -----------------------------------------------------------------------------
# Удостоверяющие центры
# -----------------------------------------------------------------------------
def seed_certification_centers(
    session: Session, owner: User
) -> list[CertificationCenter]:
    names = [
        "АО «Аналитический центр»",
        "УЦ «Основание»",
    ]
    centers: list[CertificationCenter] = []
    for name in names:
        center, created = get_or_create(
            session, CertificationCenter, name=name, owner_id=owner.id
        )
        centers.append(center)
        logger.info("УЦ %s %s", name, "создан" if created else "уже есть")
    session.commit()
    return centers


# -----------------------------------------------------------------------------
# Типы подписи
# -----------------------------------------------------------------------------
def seed_signature_types(session: Session, owner: User) -> list[SignatureType]:
    names = [
        "Квалифицированная",
        "Усиленная неквалифицированная",
        "Простая электронная",
    ]
    types: list[SignatureType] = []
    for name in names:
        st, created = get_or_create(
            session, SignatureType, name=name, owner_id=owner.id
        )
        types.append(st)
        logger.info("Тип подписи %s %s", name, "создан" if created else "уже есть")
    session.commit()
    return types


# -----------------------------------------------------------------------------
# Сотрудники
# -----------------------------------------------------------------------------
def seed_employees(
    session: Session, owner: User, count: int = 100
) -> list[Employee] | Sequence[Employee]:
    positions = [
        "Генеральный директор",
        "Главный бухгалтер",
        "Менеджер",
        "Юрист",
        "Инженер",
        "Аналитик",
        "Специалист по кадрам",
        "Экономист",
        "Логист",
        "Системный администратор",
    ]

    existing = session.exec(select(Employee).where(Employee.owner_id == owner.id)).all()

    if len(existing) >= count:
        logger.info("Сотрудники уже созданы: %d", len(existing))
        return existing

    employees: list[Employee] = list(existing)
    to_create = count - len(existing)

    for i in range(to_create):
        emp = Employee(
            name=fake.name(),
            position=random.choice(positions),
            owner_id=owner.id,
        )
        session.add(emp)
        employees.append(emp)

    session.commit()
    logger.info("Сотрудников создано: %d (всего: %d)", to_create, len(employees))
    return employees


# -----------------------------------------------------------------------------
# ЭЦП
# -----------------------------------------------------------------------------
def seed_signatures(
    session: Session,
    owner: User,
    orgs: Iterable[Organization],
    centers: Iterable[CertificationCenter],
    sig_types: Iterable[SignatureType],
    employees: Iterable[Employee],
    s3_client=None,
    count: int = 200,
    batch_size: int = 50,
) -> None:
    existing_count = len(
        session.exec(
            select(ElectronicDigitalSignature).where(
                ElectronicDigitalSignature.owner_id == owner.id
            )
        ).all()
    )

    if existing_count >= count:
        logger.info("ЭЦП уже созданы: %d", existing_count)
        return

    to_create = count - existing_count
    logger.info("Создаю %d ЭЦП...", to_create)

    created = 0
    for i in range(to_create):
        org = random.choice(tuple(orgs))
        center = random.choice(tuple(centers))
        sig_type = random.choice(tuple(sig_types))
        emp = random.choice(tuple(employees))

        cert_key = f"certificates/seed/{uuid.uuid4()}.cer"
        cont_key = f"containers/seed/{uuid.uuid4()}.pfx"

        sig = ElectronicDigitalSignature(
            date_certificate=fake_datetime(365),
            date_container=fake_datetime(365),
            file_certificate=cert_key,
            file_container=cont_key,
            owner_id=owner.id,
            organization_id=org.id,
            signature_type_id=sig_type.id,
            employee_id=emp.id,
            certification_center_id=center.id,
        )
        session.add(sig)

        if s3_client and UPLOAD_S3:
            cert_content = (
                f"FAKE CERTIFICATE\n"
                f"Owner: {emp.name}\n"
                f"Organization: {org.name}\n"
                f"Center: {center.name}\n"
                f"Type: {sig_type.name}\n"
                f"Date: {sig.date_certificate.isoformat()}\n"
                f"UUID: {uuid.uuid4()}\n"
            ).encode()
            cont_content = os.urandom(2048)

            upload_fake_file(
                s3_client,
                settings.S3_BUCKET,
                cert_key,
                cert_content,
                "application/x-x509-ca-cert",
            )
            upload_fake_file(
                s3_client,
                settings.S3_BUCKET,
                cont_key,
                cont_content,
                "application/x-pkcs12",
            )

        created += 1

        # коммит батчами — быстрее и не держит всё в памяти
        if created % batch_size == 0:
            session.commit()
            logger.info("Прогресс: %d / %d", created, to_create)

    session.commit()
    logger.info("ЭЦП создано: %d (всего: %d)", created, existing_count + created)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
def main() -> None:
    with Session(engine) as session:
        if RESET:
            reset_db(session)

        users = seed_users(session)
        admin = users[0]

        seed_items(session, admin)
        orgs = seed_organizations(session, admin)
        centers = seed_certification_centers(session, admin)
        sig_types = seed_signature_types(session, admin)
        employees = seed_employees(session, admin)

        seed_signatures(
            session,
            admin,
            orgs,
            centers,
            sig_types,
            employees,
            s3_client,
            count=200,
            batch_size=50,
        )

    logger.info("✅ Заполнение завершено.")


if __name__ == "__main__":
    main()
