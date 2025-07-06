from django.contrib.auth import get_user_model
import factory

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save=True

    username = factory.Sequence(lambda n: f"user_{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@example.com")
    password = factory.PostGeneration(
        lambda obj, *args, **kwargs: obj.set_password("testpass123")
    )


class BaseAbstractModelFactory(factory.django.DjangoModelFactory):
    """Базовый класс для фабрик моделей, наследующих от абстрактных"""

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """Переопределяем метод создания для работы с абстрактными моделями"""
        return super()._create(model_class, *args, **kwargs)
