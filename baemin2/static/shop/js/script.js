$(document).ready(function(){
		//#search 크기 줄이기
		$('#search').css('height', '100px').css('background-position-y', 'bottom');
		$('#search form').removeClass("mt-5 pt-5");

		//음식점 count
		(function(){
			var restaurant_count = $('.restaurant-list').length;
			$('#restaurant-count').text(restaurant_count).css('color','red');
		})();

		//메뉴 url이동과 크기 지정 및 active 동작,
		(function(){
			$('#menu_list li').css('width', '81.6px').css('height', '100%').css('text-align', 'center');

			$('li.category').hover(
				function(){
					$(this).css('background-color', 'rgba(51,51,51)').css('color', 'white');
				},
				function(){
					$(this).css('background-color', 'white').css('color', 'black');
				}
			);

			$('li.category').click(function(){
				location.href = "http://localhost:8000/shop/category/" + this.id;
			});

		})();

		//category_detail view로 검색 데이터 전달
		(function(){
			$('#search-form').prop('action', location.href);
		})();

		
	});
