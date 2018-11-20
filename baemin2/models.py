from django.db import models
from django.urls import reverse
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.utils import timezone

class Category(models.Model):
	name = models.CharField(max_length=50, db_index=True)
	en_name = models.CharField(max_length=50, null=True, blank=True)
	slug = models.SlugField(unique=True, allow_unicode=True, null=True)
	icon = models.ImageField(blank=True)
	is_public = models.BooleanField(default=False, db_index=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:category_detail', args=[self.slug])

	def save(self, *args, **kwargs):
		self.slug = slugify(self.en_name, allow_unicode=True)
		super().save(*args, **kwargs)


class Shop(models.Model):
	category = models.ManyToManyField(Category)
	name = models.CharField(max_length=50, db_index=True)
	photo = models.ImageField(blank=True)
	lnglat = models.CharField(max_length=100, blank=True)
	#meta = JSONField(null=True)
	is_public = models.BooleanField(default=False, db_index=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:shop_detail', args=[self.pk])

class ShopDesc(models.Model):
	shop = models.OneToOneField(Shop, on_delete=models.CASCADE, null=True)
	intro_message = models.TextField(verbose_name="사장님알림", blank=True, null=True)
	start_time = models.CharField(max_length=10, verbose_name="영업시작 시간", blank=True)
	finished_time = models.CharField(max_length=10, verbose_name="영업종료 시간", blank=True)
	min_order_amount = models.PositiveIntegerField(verbose_name="최소주문금액", blank=True)
	method_of_payment = models.CharField(max_length=50, blank=True, verbose_name="결제수단")
	business_name = models.CharField(max_length=50, blank=True, verbose_name="상호명")
	company_registration_number = models.CharField(max_length=50, verbose_name="사업자등록번호", blank=True)
	origin_info = models.TextField(verbose_name="원산지 정보", blank=True)
	delivery_time = models.CharField(max_length=10, blank=True)

	def __str__(self):
		return self.shop.name

class MenuCategory(models.Model):
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True)
	name = models.CharField(max_length=50, db_index=True)

	def __str__(self):
		return self.name

class Review(models.Model):
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
	author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	message = models.TextField()
	photo = models.ImageField(blank=True)
	flaver_rating = models.SmallIntegerField(validators=[MinValueValidator(0),
				MaxValueValidator(5)])
	amount_of_food_rating = models.SmallIntegerField(validators=[MinValueValidator(0),
				MaxValueValidator(5)])
	delivery_rating = models.SmallIntegerField(validators=[MinValueValidator(0),
				MaxValueValidator(5)])
	created_at = models.DateTimeField(auto_now_add=True, null=True)
	modify_at = models.DateTimeField(auto_now=True, null=True)

	class Meta:
		ordering = ('-modify_at',)

	def __str__(self):
		return self.message

	def total_review(self):
		total = float(self.flaver_rating + self.amount_of_food_rating + self.delivery_rating) / 3.0
		return round(total, 1)

	def get_datetime_format(self):
		tz_now = timezone.now()
		time = tz_now - self.created_at
		if(time.seconds < 3600):
			t = time.seconds / 60
			t_str = "{}분 전".format(t)
		elif(time.days < 1):
			t = time.seconds / 3600
			t_str = "{}시간 전".format(t)
		elif(time.days < 7):
			t = time.days
			t_str = "{}일 전".format(t)
		else:
			t_str = self.created_at.strftime("%Y %m %d")

		return t_str

	@property
	def aver_rating(self):
		if self.flavor_rating and self.amount_of_food_rating and self.delivery_rating:
			return (self.flavor_rating + self.amount_of_food_rating + self.delivery_rating) / 3.0
		return None

class Item(models.Model):
	shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
	menu_category = models.ForeignKey(MenuCategory, on_delete=models.SET_NULL, null=True)
	name = models.CharField(max_length=50, db_index=True)
	desc = models.TextField(blank=True)
	amount = models.PositiveIntegerField()
	photo = models.ImageField(blank=True)
	#meta = JSONField(null=True)
	is_public = models.BooleanField(default=False, db_index=True)

	def __str__(self):
		return self.name
