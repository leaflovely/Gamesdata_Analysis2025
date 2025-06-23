from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Game(models.Model):
    # 基础信息
    name = models.CharField(max_length=255, verbose_name="游戏名称")
    platform = models.CharField(max_length=50, verbose_name="平台")  # 简化为字符字段[6](@ref)
    release_date = models.DateField(verbose_name="发行日期")  # 日期类型[6](@ref)

    # Meta评分相关
    meta_reviews_number = models.PositiveIntegerField(
        default=0, verbose_name="Meta评价数量"
    )
    meta_score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Meta评分"
    )
    meta_positive = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Meta好评率(%)"
    )
    meta_mixed = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Meta中立评价率(%)"
    )
    meta_negative = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="Meta差评率(%)"
    )

    # 用户评分相关
    user_reviews_number = models.PositiveIntegerField(
        default=0, verbose_name="用户评价数量"
    )
    user_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
        verbose_name="用户评分"
    )
    user_positive = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="用户好评率(%)"
    )
    user_mixed = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="用户中立评价率(%)"
    )
    user_negative = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="用户差评率(%)"
    )

    # 开发与发行信息
    developer = models.CharField(max_length=100, blank=True, verbose_name="开发商")  # 允许为空[8](@ref)
    publisher = models.CharField(max_length=100, blank=True, verbose_name="发行商")
    genres = models.TextField(verbose_name="游戏类型")  # 多类型用文本存储（如"Open-World, Action"）[6](@ref)

    class Meta:
        verbose_name = "游戏"  # 后台显示名称[7](@ref)
        verbose_name_plural = "游戏列表"
        ordering = ["-release_date"]  # 按发行日期倒序[1](@ref)
        indexes = [
            models.Index(fields=["name"]),  # 名称索引优化查询[7](@ref)
            models.Index(fields=["meta_score", "user_score"]),
        ]

    def __str__(self):
        return f"{self.name} ({self.release_date.year})"