from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import *
from django.db.models import Q
import json

class CategoryList(ListView):
	model = Category
index = CategoryList.as_view()


class CategoryDetail(DetailView):
	model = Category

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		if self.request.GET.get('search', ''):
			search_result = self.request.GET['search']
			shop_list = Shop.objects.filter(Q(name__icontains=search_result)|
				Q(item__name__icontains=search_result))
			context['shop_list'] = shop_list
		else:
			shop_list = Shop.objects.filter(category__slug=self.kwargs['slug'])
			context['shop_list'] = shop_list
		return context

category_detail = CategoryDetail.as_view()


class ShopDetail(DetailView):
	model = Shop

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		#대표메뉴
		if MenuCategory.objects.filter(name='대표메뉴').exists():
			#exists()는 queryset 메소드라서 get(queryset 리턴x)다음에 사용 불가
			rep_menu = get_object_or_404(MenuCategory, name='대표메뉴')
			context['rep_menu'] = rep_menu

		#대표 메뉴를 제외한 메뉴 카테고리
		menu_category = MenuCategory.objects.exclude(name__icontains="대표메뉴")
		context['menu_category'] = menu_category

		#review(평점과, 개수)
		context['total_review'], context['flavor_rate'], context['amount_rate'], context['delivery_rate'] = self.get_review()

		#review_id_list
		context['review_id_list'] = self.get_review_id_list()

		#각 리뷰에 대한 총 평점
		context['total_review_list'] = self.get_total_review()

		return context

	def get_review(self):
		review_list = Shop.objects.get(id=self.kwargs['pk']).review_set.all()
		review_count = review_list.count()
		flavor_rate, amount_rate, delivery_rate, total_review = 0.0, 0.0, 0.0, 0.0

		for review in review_list:
			flavor_rate += review.flaver_rating
			amount_rate += review.amount_of_food_rating
			delivery_rate += review.delivery_rating
			total_review += review.total_review()

		if(review_count > 0):
			flavor_rate = round(float(flavor_rate) / float(review_count), 1)
			amount_rate = round(float(amount_rate) / float(review_count) , 1)
			delivery_rate = round(float(delivery_rate) / float(review_count), 1)
			total_review = round(float(total_review) / float(review_count), 1)
		return total_review, flavor_rate, amount_rate, delivery_rate

	def get_review_id_list(self):
		review_list = Review.objects.all()
		review_id_list = []
		for review in review_list:
			review_id_list.append(review.id)

		review_id_list = json.dumps(review_id_list)
		return review_id_list

	def get_total_review(self):
		review_list = Review.objects.all()
		total_review_list = []
		for review in review_list:
			total_review_list.append(review.total_review())

		total_review_list = json.dumps(total_review_list)
		return total_review_list

shop_detail = ShopDetail.as_view()
