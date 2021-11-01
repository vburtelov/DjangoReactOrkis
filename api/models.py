from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User, AbstractUser, PermissionsMixin, Group
from django.db import models

from .managers import EmployeeManager


class Passport(models.Model):
    PASSPORT_TYPE = (
        ("1", "Загранпаспорт"),
        ("2", "Паспорт РФ"),
    )

    pass_series = models.IntegerField(verbose_name="Серия")
    pass_number = models.IntegerField(verbose_name="Номер")
    date_of_receiving = models.DateField(verbose_name="Дата получения")
    date_of_expiry = models.DateField(verbose_name="Срок действия")
    place_of_issue = models.CharField(max_length=200, verbose_name="Место получения")

    type = models.CharField(
        max_length=13,
        choices=PASSPORT_TYPE,
        default=PASSPORT_TYPE[0],
        verbose_name="Тип паспорта",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "паспорт"
        verbose_name_plural = "паспорта"

    def __str__(self):
        return f'{self.type}: {self.pass_series} {self.pass_number}'


class Client(models.Model):
    class ClientGender(models.TextChoices):
        WOMEN = 'ЖЕНЩИНА', 'Женщина'
        MEN = 'МУЖЧИНА', 'Мужчина'

    class ClientStatus(models.TextChoices):
        COMMON = 'ОБЫЧНЫЙ', 'Обычный'
        VIP = 'VIP', 'Vip'
        PREMIUM = 'ПРИВИЛЕГИРОВАННЫЙ', 'Привилегированный'

    fio = models.CharField(max_length=45, verbose_name="ФИО")
    gender = models.CharField(
        max_length=7,
        choices=ClientGender.choices,
        default=ClientGender.MEN,
        verbose_name="Пол"
    )
    date_of_birth = models.DateField(verbose_name="Дата рождения")
    place_of_birth = models.CharField(max_length=200, verbose_name="Место рождения")

    status = models.CharField(
        max_length=17,
        choices=ClientStatus.choices,
        default=ClientStatus.COMMON,
        verbose_name="Статус"
    )

    russian_passport = models.OneToOneField(
        Passport,
        on_delete=models.CASCADE,
        unique=True,
        related_name='russian_passport',
        verbose_name="Паспорт РФ"
    )

    international_passport = models.OneToOneField(
        Passport,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='international_passport',
        verbose_name="Загранпаспорт"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "клиент"
        verbose_name_plural = "клиенты"

    def __str__(self):
        return self.fio


class Organization(models.Model):
    name = models.CharField(max_length=45, verbose_name="Название")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=45, verbose_name="Номер телефона")

    class Meta:
        verbose_name = "организация"
        verbose_name_plural = "организации"

    def __str__(self):
        return self.name


class Employee(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(verbose_name='Имя пользователя', max_length=30, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=30)
    last_name = models.CharField(verbose_name='Фамилия', max_length=30)
    middle_name = models.CharField(verbose_name='Отчество', max_length=30)
    date_of_birth = models.DateField(verbose_name='День рождения', blank=True, null=True)

    groups = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        verbose_name='Должность',
        blank=True,
        related_name="group_set",
        related_query_name="group",
        null=True
    )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Организация",
        related_name="organization_set",
        related_query_name="organization",
    )
    photo = models.ImageField(verbose_name="Фотография", blank=True, null=True, upload_to='static/media/')
    is_superuser = models.BooleanField(verbose_name="Суперадмин?", default=False)
    is_admin = models.BooleanField(verbose_name="Админ?", default=False)
    is_active = models.BooleanField(verbose_name="Активный?", default=True)
    is_staff = models.BooleanField(verbose_name="Персонал?", default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'middle_name']

    objects = EmployeeManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "сотрудник"
        verbose_name_plural = "сотрудники"

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.middle_name}'


class Country(models.Model):
    name = models.CharField(max_length=45, unique=True, verbose_name="Название")

    class Meta:
        verbose_name = "страна"
        verbose_name_plural = "страны"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=45, verbose_name="Название")

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name="Страна"
    )

    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"

    def __str__(self):
        return f'{self.name}, {self.country.name}'


class PreAgreement(models.Model):
    date_of_start = models.DateField(verbose_name="Дата начала тура")
    date_of_end = models.DateField(verbose_name="Дата окончания тура")
    cities_to_visit = models.ManyToManyField(
        City,
        verbose_name="Города посещения"
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        verbose_name="Клиент"
    )
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Сотрудник"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "предварительное соглашение"
        verbose_name_plural = "предварительные соглашения"

    def __str__(self):
        return f'Предварительное соглашение от {self.created_at} с {self.client.fio}'


class Currency(models.Model):
    code = models.CharField(max_length=45, verbose_name="Код валюты")
    currency = models.FloatField(verbose_name="Курс")
    date = models.DateField(verbose_name="Дата", auto_now_add=True)

    class Meta:
        verbose_name = "курс валюты"
        verbose_name_plural = "курсы валют"

    def __str__(self):
        return f'{self.code} на {self.date}'


class Hotel(models.Model):
    class HotelCategory(models.TextChoices):
        FIVE_STAR = 'ПЯТИЗВЕЗДОЧНЫЙ', 'Пятизвездочный'
        FOUR_STAR = 'ЧЕТЫРЕХЗВЕЗДОЧНЫЙ', 'Четырехзвездочный'
        THREE_STAR = 'ТРЕХЗВЕЗДОЧНЫЙ', 'Трехзвездочный'
        TWO_STAR = 'ДВУХЗВЕЗДОЧНЫЙ ', 'Двухзвездочный'
        ONE_STAR = 'ОДНОЗВЕЗДОЧНЫЙ', 'Однозвездочный '
        APARTMENTS = 'АПАРТАМЕНТЫ ', 'Апартаменты'

    name = models.CharField(max_length=45, verbose_name="Название")
    category = models.CharField(
        max_length=17,
        choices=HotelCategory.choices,
        default=HotelCategory.FOUR_STAR,
        verbose_name="Категория"
    )
    address = models.CharField(max_length=200, verbose_name="Адрес")
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="Город"
    )

    class Meta:
        verbose_name = "отель"
        verbose_name_plural = "отели"

    def __str__(self):
        return f'{self.name} в {self.city.country.name}, {self.city.name}'


class Room(models.Model):
    name = models.CharField(max_length=45, verbose_name="Название")
    number_of_beds = models.IntegerField(default=1, verbose_name="Количество кроватей")
    number_of_clients = models.IntegerField(default=1, verbose_name="Максимальное количество гостей")
    balcony = models.BooleanField(default=False, verbose_name="Есть балкон?")
    food_included = models.BooleanField(default=False, verbose_name="Включена еда?")
    is_free = models.BooleanField(default=False, verbose_name="Номер занят?")

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        verbose_name="Отель"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "номер"
        verbose_name_plural = "номера"

    def __str__(self):
        return f'Номер {self.name}. Количество мест: {self.number_of_clients}'


class Route(models.Model):
    start_date = models.DateField(verbose_name="Начало маршрута")
    end_date = models.DateField(verbose_name="Конец маршрута")

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        verbose_name="Город"
    )

    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        verbose_name="Отель"
    )

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        verbose_name="Номер в отеле"
    )

    class Meta:
        verbose_name = "маршрут"
        verbose_name_plural = "маршруты"

    def __str__(self):
        return f'Маршрут номер: {self.id}'


class Tour(models.Model):
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        verbose_name="Страна"
    )

    routes = models.ManyToManyField(
        Route,
        verbose_name="Маршруты"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "тур"
        verbose_name_plural = "туры"

    def __str__(self):
        return f'Тур номер: {self.id}'


class Contract(models.Model):
    date_of_start = models.DateField(verbose_name="Дата начала путешествия")
    date_of_end = models.DateField(verbose_name="Дата завершения путешествия")
    money_sum = models.FloatField(verbose_name="Сумма")
    currency = models.ForeignKey(
        Currency,
        on_delete=models.PROTECT,
        verbose_name="Валюта"
    )

    tourists = models.ManyToManyField(
        Client,
        verbose_name="Туристы"
    )

    tour = models.OneToOneField(
        Tour,
        on_delete=models.PROTECT,
        verbose_name="Тур"
    )

    pre_agreement = models.OneToOneField(
        PreAgreement,
        on_delete=models.CASCADE,
        verbose_name="Предварительное соглашение"
    )

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Сотрудник"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "контракт"
        verbose_name_plural = "контракты"

    def __str__(self):
        return f'Контракт {self.id} с {self.pre_agreement.client.fio} от {self.created_at} '


class Payment(models.Model):
    date_expired = models.DateField(verbose_name="Дата истечения срока платежа")
    date_payment = models.DateField(blank=True, null=True, verbose_name="Дата успешной оплаты")
    isPayed = models.BooleanField(default=False, verbose_name="Оплачен?")
    amount_in_rouble = models.FloatField(verbose_name="Сумма в рублях")

    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name="Бухгалтер"
    )

    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        verbose_name="Контракт"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "платеж"
        verbose_name_plural = "платежи"

    def __str__(self):
        return f'Платеж номер: {self.id}'


class Voucher(models.Model):
    transfer_included = models.BooleanField(default=False, verbose_name="Трансфер включен?")
    travel_docs = models.CharField(max_length=255, verbose_name="Документы")

    class TransportType(models.TextChoices):
        NO = "БЕЗ ТРАНСФЕРА", "Без трансфера"
        AUTO = 'АВТОМОБИЛЬ', 'Автомобиль'
        BUS = 'АВТОБУС', 'Автобус'

    transport = models.CharField(
        max_length=13,
        choices=TransportType.choices,
        default=TransportType.NO,
        verbose_name="Транспорт"
    )

    payment = models.OneToOneField(
        Payment,
        on_delete=models.CASCADE,
        verbose_name="Платеж"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "ваучер"
        verbose_name_plural = "ваучеры"

    def __str__(self):
        return f'Ваучер номер: {self.id}'
