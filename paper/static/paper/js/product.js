$(document).ready(function(){
	$(".ajaxLoader").hide();

	// Product Filter Start
	$(".filter-checkbox,#priceFilterBtn").on('click',function(){
		var _filterObj={};
		var _categoryid = $('#category').val();
		var _minPrice=$('#maxPrice').attr('min');
		var _maxPrice=$('#maxPrice').val();
		_filterObj.minPrice=_minPrice;
		_filterObj.maxPrice=_maxPrice;
		_filterObj.categoryid=_categoryid;

		$(".filter-checkbox").each(function(index,ele){
			var _filterVal=$(this).val();
			var _filterKey=$(this).data('filter');
			_filterObj[_filterKey]=Array.from(document.querySelectorAll('input[data-filter='+_filterKey+']:checked')).map(function(el){
			 	return el.value;
			});
		});

		// Run Ajax
		$.ajax({
            type: 'GET',
			url:'/filter-data/',
			data:_filterObj,

			dataType:'json',

			beforeSend:function(){
				$(".ajaxLoader").show();
			},
			success:function(res){
				console.log(res);
				console.log(_filterObj)
				$("#filteredProducts").html(res.data);
				$(".ajaxLoader").hide();
			}
		});





	});
	// End

	// Filter Product According to the price
	$("#maxPrice").on('blur',function(){
		var _min=$(this).attr('min');
		var _max=$(this).attr('max');
		var _value=$(this).val();
		console.log(_value,_min,_max);
		if(_value < parseInt(_min) || _value > parseInt(_max)){
			alert('Values should be '+_min+'-'+_max);
			$(this).val(_min);
			$(this).focus();
			$("#rangeInput").val(_min);
			return false;
		}
	});
	// End

	// const alertBox = document.getElementById('alert-box')
	// const imgBox = document.getElementById('img-box')
	// const productForm = document.getElementById('p-form')
	// const imagesForm = document.getElementById('i-form')
	// const variantsForm = document.getElementById('v-form')
	//
	// const tital = document.getElementById('id_title')
	// const cat = document.getElementById('id_categories')
	// const code = document.getElementById('id_code')
	// const slug = document.getElementById('id_slug')
	// const brand = document.getElementById('id_brand')
	// const description = document.getElementById('id_description')
	// const keywords = document.getElementById('id_keywords')
	// const image = document.getElementById('id_image')
	// const price = document.getElementById('id_price')
	// const discountPrice = document.getElementById('id_discount_price')
	// const amount = document.getElementById('id_amount')
	// const minAmount = document.getElementById('id_min_amount')
	// const variant = document.getElementById('id_variant')
	// const detail = document.getElementById('id_detail')
	//
    // const csrf = document.getElementsByName('csrfmiddlewaretoken')
	// console.log(csrf)
	//
    // const url = ""
	// image.addEventListener('change',()=>{
	// 	const img_data = image.files[0]
	// 	const url = URL.createObjectURL(img_data)
	// 	console.log(url)
	// 	imgBox.innerHTML = '<img src="${url}" width="100%">'
	// })
	// productForm.addEventListener('submit', e=>{
	// 	e.preventDefault()
	// 	const fd = new FormData()
	// 	fd.append('csrfmiddlewaretoken',csrf[0].value)
	// 	fd.append('tital',tital.value)
	// 	fd.append('cat',cat.value)
	// 	fd.append('code',code.value)
	// 	fd.append('keywords',keywords.value)
	// 	fd.append('brand',brand.value)
	// 	fd.append('description',description.value)
	// 	fd.append('image',image.files[0])
	// 	fd.append('price',price.value)
	// 	fd.append('discountPrice',discountPrice.value)
	// 	fd.append('amount',amount.value)
	// 	fd.append('minAmount',minAmount.value)
	// 	fd.append('variant',variant.value)
	// 	fd.append('detail',detail.value)
	// 	fd.append('slug',slug.value)
	//
	// 	$.ajax({
	// 		type:'POST',
	// 		url:/new_product/,
	// 		enctype:'multipart/form-data',
	// 		data:fd,
	// 		success: function (response) {
	// 			console.log(response)
	// 		},
	// 		error: function(error){
	// 			console.log(error)
	// 		},
	// 		cache: false,
	// 		contentType: false,
	// 		processData:false,
	//
	// 		})
	//
	//
	// })
	//
	//
	// console.log(productForm)
	// console.log(imagesForm)
	// console.log(variantsForm)

});

