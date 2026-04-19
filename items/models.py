from django.conf import settings
from django.db import models


class Item(models.Model):
    TYPE_LOST = "lost"
    TYPE_FOUND = "found"
    TYPE_CHOICES = [(TYPE_LOST, "失物"), (TYPE_FOUND, "招领")]

    CATEGORY_ELECTRONICS = "electronics"
    CATEGORY_ID = "id"
    CATEGORY_BOOKS = "books"
    CATEGORY_DAILY = "daily"
    CATEGORY_OTHER = "other"

    CATEGORY_CHOICES = [
        (CATEGORY_ELECTRONICS, "电子产品"),
        (CATEGORY_ID, "证件卡片"),
        (CATEGORY_BOOKS, "书籍资料"),
        (CATEGORY_DAILY, "生活用品"),
        (CATEGORY_OTHER, "其他物品"),
    ]

    STATUS_OPEN = "open"
    STATUS_CLOSED = "closed"
    STATUS_CHOICES = [(STATUS_OPEN, "待认领"), (STATUS_CLOSED, "已完成")]

    type = models.CharField(max_length=16, choices=TYPE_CHOICES, db_index=True)
    title = models.CharField(max_length=100, db_index=True)
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, db_index=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, db_index=True)
    time = models.DateTimeField(help_text="物品遗失或拾获的时间")
    contact = models.CharField(max_length=100)
    image = models.ImageField(upload_to="items/%Y/%m/", blank=True, null=True)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="items",
    )

    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=STATUS_OPEN,
        db_index=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.get_type_display()} - {self.title}"
