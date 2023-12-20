import uuid as uuid
from django.contrib.auth import get_user_model
from django.db import models

# User = get_user_model()


class Organization(models.Model):
    """Описание модели организации."""

    id = models.BigAutoField(
        primary_key=True,
        help_text='Идентификатор организации в БД')

    # uuid = models.UUIDField(
    #     default=uuid.uuid4,
    #     editable=False,
    #     unique=True)

    full_name = models.TextField(
        'Полное наименование',
        null=False,
        blank=False,
        help_text='Полное наименование организации')

    short_name = models.TextField(
        'Сокращенное наименование',
        null=True,
        blank=True,
        help_text='Сокращенное наименование организации')

    inn = models.CharField(
        'ИНН',
        max_length=12,
        null=True,
        blank=True,
        help_text='ИНН организации')

    factual_address = models.TextField(
        'Адрес',
        help_text='Адрес местонахождения организации')

    date_added = models.DateTimeField(
        'Дата создания организации в БД',
        auto_now=True,
        help_text='Дата внесения организации в БД')

    longitude = models.FloatField(
        verbose_name='Долгота',
        help_text='Долгота расположения '
                  'организации',
        null=False, blank=False)

    latitude = models.FloatField(
        verbose_name='Широта',
        help_text='Широта расположения '
                  'организации',
        null=False, blank=False)

    site = models.CharField(
        'Сайт организации',
        max_length=100,
        null=True,
        blank=True,
        help_text='Сайт организации'
    )

    email = models.EmailField(
        'E-mail организации',
        max_length=100,
        null=True,
        blank=True,
        help_text='E-mail организации')

    is_gov = models.BooleanField(
        'Государственная?',
        default=False,
        help_text='Является ли организация государственной'
    )

    is_full_time = models.BooleanField(
        'Круглосуточная?',
        default=False,
        help_text='Является ли организация круглосуточной'
    )

    about = models.TextField(
        'Дополнительная информация',
        null=True,
        blank=True,
        help_text='Дополнительная информация об организации'
    )
    # town = models.ForeignKey(
    #     Town,
    #     on_delete=models.SET_NULL,
    #     verbose_name='Город организации',
    #     null=True,
    #     related_name='organizations',
    #     help_text='Город организации'
    # )
    #
    # district = models.ForeignKey(
    #     District,
    #     on_delete=models.SET_NULL,
    #     verbose_name='Район организации',
    #     null=True,
    #     related_name='organizations',
    #     help_text='Район организации'
    # )

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return f'<Организация {self.full_name}>'


class ModerationReviews(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)


class Review(models.Model):

    CHOICES = [(i, i) for i in range(1, 6)]

    # APPROVED = "1"
    # REJECTED = "2"
    # PENDING = "3"
    #
    # STATUS_CHOICES = (
    #     (APPROVED, ("Approved")),
    #     (PENDING, ("Pending")),
    #     (REJECTED, ("Rejected")),
    # )
    #
    # review_status = models.CharField(
    #     ("Review Status"),
    #     max_length=1,
    #     choices=STATUS_CHOICES,
    #     default=PENDING,
    #     blank=True,
    #     db_index=True,
    # )

    text = models.CharField(
        'Текст отзыва',
        max_length=1000
    )

    # author = models.ForeignKey(
    #     User,
    #     on_delete=models.CASCADE,
    #     verbose_name='Автор'
    # )

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )

    estimation = models.PositiveSmallIntegerField(
        'Оценка',
        choices=CHOICES,
    )

    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True
    )

    status = models.BooleanField(
        'Видимость отзыва',
        default=False
    )

    objects = ModerationReviews()

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        # constraints = [
        #     models.UniqueConstraint(
        #         fields=('title', 'author',),
        #         name='unique_review'
        #     )
        # ]
        # ordering = ['-pub_date']

    def __str__(self):
        return self.text
