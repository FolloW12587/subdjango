from django.db import models

# Create your models here.


class MessageSending(models.Model):
    STATUSES = (
        ("CREATED", "Создана"),
        ("TEST", "Тест"),
        ("UPCOMING", "Предстоящая"),
        ("PROCESSING", "В обработке"),
        ("COMPLETED", "Выполненна"),
        ("FAILED", "Ошибка"),
    )
    status = models.CharField(
        "Статус",
        max_length=31,
        choices=STATUSES,
        editable=False,
        default="CREATED",
        help_text="""
Статусы:
"Создана" - рассылка создана, но пока не стоит на очередь в обработку
"Предстоящая" - рассылка стоит на очереди в обработку
"В обработке" - рассылка происходит в данный момент
"Выполненна" - рассылка завершена
"Ошибка" - произошла ошибка при обработке рассылки
"Тест" - поставили в очередь на тест. При тесте, сообщение будет отправлено \
только в админскую группу
""",
    )
    started_at = models.DateTimeField(
        "Начата в", editable=False, null=True, blank=True, default=None
    )
    ended_at = models.DateTimeField(
        "Закончена в", editable=False, null=True, blank=True, default=None
    )
    text = models.TextField("Текст")
    image = models.ImageField(
        upload_to="message_sendings/",
        null=True,
        blank=True,
        verbose_name="Изображение",
        default=None,
    )

    # Статы
    users_to_notify = models.PositiveIntegerField(
        "Пользователей к уведомлению",
        editable=False,
        null=True,
        blank=True,
        default=None,
    )
    users_notified = models.PositiveIntegerField(
        "Пользователей уведомлено", editable=False, null=True, blank=True, default=None
    )
    error_message = models.TextField(
        "Тeкст ошибки", default=None, null=True, blank=True
    )

    class Meta:
        managed = False
        db_table = "message_sendings"
        verbose_name = "Рассылка"
        verbose_name_plural = "Рассылки"

    def __str__(self):
        return f"{self.text[:30]}"


class MessageSendingButton(models.Model):
    TYPES = (
        ("TEXT", "Текст"),
        ("DATA", "Данные"),
        ("URL", "Ссылка"),
        ("KEYBOARD", "Кнопка в меню"),
    )
    message_sending = models.ForeignKey(
        MessageSending, on_delete=models.CASCADE, verbose_name="Рассылка"
    )
    type = models.CharField(
        "Тип",
        max_length=31,
        choices=TYPES,
        help_text="""
Тип кнопки говорит о том, как она будет отображаться и какие данные отправлять.
                            
Текст, Данные и Ссылка - это кнопки непосредственно под сообщением. Их можно отправлять \
вместе друг с другом.
"Кнопка в меню" - это кнопки, которые ты видишь при открытии бота (Настройки, Подписка и Посмотреть товары). \
Не рекомендую их отправлять в принципе, но если сильно надо, кнопки можно обновить так этой рассылкой.
Кнопки в меню не сочетаются с остальными. Если хочется обновить кнопки в меню и добавить кнопку под сообщением, \
то нужно сделать две рассылки.

Кнопка "Текст". При нажатии на нее отправится текст кнопки в чат.
Кнопка "Данные". В чат ничего не отправится, но в бота передадутся данные, указанные ниже.
Кнопка "Ссылка". Откроется ссылка, которая была передана ниже.
""",
    )
    text = models.CharField("Текст", max_length=127)
    data = models.CharField(
        "Данные",
        max_length=127,
        null=True,
        blank=True,
        default=None,
        help_text="""
Данные, которые будут отправлены с кнопкой. 
Если это тип кнопки "Текст" или "Кнопка в меню", то данные игнорируются.
Если "Ссылка", то нужно передать ссылку на внешний источник.
Если "Данные"
""",
    )

    class Meta:
        managed = False
        db_table = "message_sending_butttons"
        verbose_name = "Кнопка рассылки"
        verbose_name_plural = "Кнопки рассылок"
