$(document).ready(function()
{
    $('#reviews ul').jcarousel();
    $('#partners ul').jcarousel({scroll: 6});
    $('#promo_slider').jcarousel({scroll: 1, wrap: 'circular',
        itemVisibleInCallback: promo_slider_item,
        animationStepCallback: function(){
            $('.promo_slider_head img').fadeOut();
            //$('#countdown').fadeOut();
        },
        auto: 10
    });

    function promo_slider_item(event, item)
    {
        $('#slider_selector_cont .round').removeClass('activated').eq((event.last - 1) % event.options.size).addClass('activated');
        var $itemPhoto = $(item).find('.slider_photo');

        $('.promo_slider_head img').replaceWith($(item).find('.slider_photo').html());
        $('.promo_slider_head img').fadeIn();
        $('.promo_slider_head').attr('href', $itemPhoto.data('href'));
        //$('#countdown').fadeIn();
    }

    $(".slider_selector_inner .round").click(function () {
        if (!$(this).hasClass('activated')) {
            $('#promo_slider').jcarousel('scroll', parseInt($(this).attr('rel')) + 1);
            $(".slider_selector_inner .round").removeClass("activated");
            $(this).addClass("activated");
        }
    });
    
    if ($('#additions ul li').length){
	    $('#additions ul').jcarousel({scroll: 3});
    }
    
    if ($('#additions_delivery_main ul li').length){
	    $('#additions_delivery_main ul').jcarousel({scroll: 6});
    }

    $('#popup_form a.close').on('click', function()
    {
        $('#popup_form').hide();
    });

    $('#delivery input[type="radio"]').on('click', function()
    {
        $('.delivery_block').removeClass('active');
        var parentBlock = $(this).parents('.delivery_block');
        parentBlock.addClass('active');
        $('#delivery_type').attr('value', parentBlock.attr('rel'));
    });


    $('#id_customer_is_destination, #id_anonymous_delivery, #id_phone_only').on('change', function()
    {
        orderFormChanged();
    });

    $.datepicker.regional['ru'] =
    {
        closeText: 'Закрыть',
        prevText: 'Назад',
        nextText: 'Вперед',
        currentText: '',
        monthNames: ['Январь','Февраль','Март','Апрель','Май','Июнь',
            'Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь'],
        monthNamesShort: ['Янв.','Фев.','Март','Апр.','Май','Июнь',
            'Июль','Авг.','Сент.','Окт.','Нояб.','Дек.'],
        dayNames: ['Воскресенье','Понедельник','Вторник','Среда','Четверг','Пятница','Суббота'],
        dayNamesShort: ['Вс','Пн','Вт','Ср','Чт', 'Пт','Сб'],
        dayNamesMin: ['Вс','Пн','Вт','Ср','Чт', 'Пт','Сб'],
        weekHeader: 'Нед.',
        dateFormat: 'dd.mm.yy',
        firstDay: 1,
        isRTL: false,
        showMonthAfterYear: false,
        yearSuffix: '',
        minDate: parseInt((new Date(2015, 0, 6) - new Date()) / 24 / 60 / 60 / 1000)
    };


    var deliveryDateSettings = $.extend(
        true,
        {
            onSelect: function(val){
                var tmp = val.split('.'),
                    tmp_ = tmp[1],
                    d = new Date();
                tmp[1] = tmp[0];
                tmp[0] = tmp_;

                d.setHours(0);
                d.setSeconds(0);
                d.setMinutes(0);
                var selectedDate = new Date(tmp.join('.'));

                if (d.toString() == selectedDate.toString()){
                    $('#attention_delivery, .delivery_blocker .header[rel=7]').show();
                }
                else{
                    $('#attention_delivery, .delivery_blocker .header[rel=7]').hide();

                    if ($('.delivery_blocker .header.active').attr('rel') == '7') {
                        $(".delivery_blocker .header[rel=1]").click();
                    }
                }
            },
            showOn: "both",
            buttonImage: static_url + "images/date_icon.jpg",
            buttonImageOnly: false
        },
        $.datepicker.regional['ru']
    );

    $("#id_delivery_date").datepicker(deliveryDateSettings);
    $("#id_pay_for_delivery_date").datepicker($.datepicker.regional["ru"]);

    $('.menu li').hover(
        function()
        {
            if($(this).hasClass('active'))
            {
                $(this).attr('rel', 'active');
            }
            $(this).addClass('active');
        },
        function()
        {
            if($(this).attr('rel') != 'active')
            {
                $(this).removeClass('active');
            }
        }
    );

    $('#additions_delivery a.close').on('click', function()
    {
        $('#additions_delivery').hide();
    });
});

$(window).load(function()
{
    $('#partners li img').each(function()
    {
        $(this).css('margin-top', (($(this).parent('li').height() - $(this).outerHeight()) / 2.0).toString() + 'px');
    });
});


$(window).on('scroll', function(event){
   $('#popup_form').css('top', (window.scrollY + 25).toString() + 'px');
});


function destination_phone()
{
}


function show_call_form()
{
    $('#popup_form').show();
    $.placeholder.shim();
}

function remove_from_basket(basket_id)
{
    $('#remove_basket_product').attr('value', basket_id.toString());
    $.ajax({
        url: '/ajax_basket_remove/',
        data: $('form[name="remove_frm"]').serialize(),
        type: 'post',
        dataType: 'json',
        success: function(response)
        {
            $('#basket').html(response.basket);
            $('#basket_goods_count, .basket_goods_count').html(response.goods_count);
            $('.basket_summary').html(response.summary);

            if(!response.goods_count){
                $('.mega_button').hide();
            }
            else{
                $('.mega_button').show();
            }

            updateBasketForSummary(response.summary);
        },
        error: function()
        {
            alert('Произошла ошибка. Попробуйте позже.');
        }
    })
}


function updateBasketForSummary(basketSummary){
    var basketSummaryInt = parseInt(basketSummary.replace(' ', ''));

    if (basketSummaryInt > 0) {
        $('#basket_right_cont .basket_price').html(basketSummaryInt + ' р.');
        $('#order_summ').html(basketSummaryInt + (selectedDeliveryPrice || 0) + ' ' + rupluralize(basketSummaryInt, 'рубль,брубля,рублей'));

        if (window.freeDeliveryPrice) {
            var $freeDeliveryBlock = $('.delivery_blocker .header[rel=4]');
            if (basketSummaryInt < window.freeDeliveryPrice) {
                $freeDeliveryBlock.addClass('unactive');
                if ($freeDeliveryBlock.is('.active')) {
                    $('.delivery_blocker .header[rel=1]').click();
                }
            }
            else {
                $freeDeliveryBlock.removeClass('unactive');

                if (!$('.header.active').length && !$freeDeliveryBlock.is('.active')) {
                    $freeDeliveryBlock.click();
                }
            }
        }

        if (window.addToyPrice) {
            var $addToyInput = $('#id_add_toy');
            if (basketSummaryInt < window.addToyPrice) {
                $addToyInput.attr('disabled', '').prop('checked', false);
            }
            else {
                $addToyInput.removeAttr('disabled');
            }
        }
    }
    /*else{
        window.location.href = '/';
    }*/
}


function basket_add(product_id, category_type)
{
    if(!$('#popup_layout').length)
    {
        $('<div/>').attr('id', 'popup_layout').appendTo('body');
    }
    $('#popup_layout').show();
    var data = {'csrfmiddlewaretoken': csrf_token, 'product_id': product_id};
    var selectedHeight = $('#product_height_' + product_id.toString() + ' option:selected').attr('value');
    if (window.productsPrices){
        var priceInfo = window.productsPrices[product_id];
        var selectedCount = $('#product_count_' + product_id.toString() + ' option:selected').attr('value');

        if (selectedHeight){
            priceInfo = priceInfo[selectedHeight];
        }
        if (selectedCount){
            priceInfo = priceInfo[selectedCount];
        }

        if(priceInfo){
            data['product_price_id'] = priceInfo['id'];
        }
    }

    var $priceType = $('[name="price_type"]');
    if ($priceType.length){
        data['price_type'] = $priceType.filter(':checked').val();
    }

    if (category_type){
        data['category_type'] = category_type;
    }

    $.ajax({
        data: data,
        url: '/ajax_basket_add/',
        type: 'post',
        dataType: 'json',
        success: function(response)
        {
            if (!$('#basket').length)
            {
               $("<div/>").attr("id", "basket").insertAfter('#main_content');
            }
            $('#basket').replaceWith(response.basket);
            $('#basket_goods_count, .in_basket_right, .basket_goods_count').html(response.goods_count);
            $('.basket_summary').html(response.summary);

            if(!response.goods_count){
                $('.mega_button').hide();
            }
            else{
                $('.mega_button').show();
            }

            $('#product_basket_btn').show();
            $('#product_order_btn').show();
            $('.order_block').show();

            var basket_popup = $(response.basket_popup);
            basket_popup.appendTo($('body'));

            //basket_popup.find('.price').html(response.price);
            //basket_popup.find('.description').html(response.text);
            //basket_popup.find('.left img').attr('src', $('#good .picture').attr('src'));

            basket_popup.css({
                //left: ($(window).width() - basket_popup.width()) / 2,
                top: ($(window).height() - basket_popup.height()) / 2
            });

            basket_popup.show();

            updateBasketForSummary(response.summary);
        },
        error: function()
        {
            alert('Произошла ошибка. Попробуйте позже.');
            $('#popup_layout').hide();
        }
    });
}

$(document).ready(
    function()
    {
        $(document).on('click', '#basket_popup a, #popup_layout, #basket_popup .close', function()
        {
            $('#basket_popup').remove();
            $('#popup_layout').hide();
        });
    }
);

if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i))) {
    $("#upmenu>li>ul>li>a").click(function(){
    });
}

$(function(){
    $('#upmenu li').hover(
        function () {
            $('ul', this).stop().slideDown(1);
        },
        function () {
            $('ul', this).stop().slideUp(1);
        }
    );
});

if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i))) {
    $("#upmenu>li>ul>li>ul>li>a").click(function(){
    });
}


if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i))) {
    $("#upmenu2>li>ul>li>a").click(function(){
    });
}

$(function(){
    $('#upmenu2 li').hover(
        function () {
            $('ul', this).stop().slideDown(1);
        },
        function () {
            $('ul', this).stop().slideUp(1);
        }
    );
});

if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i))) {
    $("#upmenu2>li>ul>li>ul>li>a").click(function(){
    });
}

if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i))) {
    $("#good_menu>li>ul>li>a").click(function(){
    });
}

$(function(){
    $('#good_menu li').hover(
        function () {
            $('ul', this).stop().slideDown(1);
        },
        function () {
            $('ul', this).stop().slideUp(1);
        }
    );
});

if((navigator.userAgent.match(/iPhone/i)) || (navigator.userAgent.match(/iPod/i)) || (navigator.userAgent.match(/iPad/i))) {
    $("#good_menu>li>ul>li>ul>li>a").click(function(){
    });
}


$(function(){
    var main_block = $('#goods_list_main');
    var block = $('#goods_list_main .menu');

    if(main_block.length)
    {
        $(window).scroll(function() {
            if ($(document).scrollTop() > main_block.offset().top - block.height() / 3)
            {
                block.css({'position': 'fixed', 'top': 0});
                var fix_pos = main_block.offset().top + main_block.height() - block.height();
                if($(document).scrollTop() > fix_pos)
                {
                    block.css({'position': 'absolute'});
                    block.offset({top: fix_pos});
                }
            }
            else
            {
                block.css({'position': 'relative', top: 0});
            }
        });
    }
});

function getPriceCounts(productID){
    var pricesInfo = window.productsPrices[parseInt(productID)];
    if($('#product_height_' + productID).length){
        pricesInfo = pricesInfo[parseInt($('#product_height_' + productID + ' option:selected').attr('value'))];
    }

    return pricesInfo;
}


function updateProductPrice(productID, priceInfo){
    var oldPriceBlock = $('#product_old_price_' + productID),
        priceBlock = $('#product_price_' + productID);

    if(oldPriceBlock.length){
        if(priceInfo.old_price){
            oldPriceBlock.html(priceInfo.old_price);
        }
        else{
            oldPriceBlock.html('');
        }
    }

    if(priceBlock.length){
        priceBlock.html(priceInfo.price + ' ' + rupluralize(priceInfo.price, window.pluralizeString));
    }

    if (priceInfo.price >= freeDeliveryPrice){
        $('#free_delivery').show();
        $('#base_delivery').hide();
    }
    else{
        $('#free_delivery').hide();
        $('#base_delivery').show();
    }

    $('#product_price_id').attr('value', priceInfo.id);
}


function productHeightChanged(productID){
    productID = productID.toString();
    var pricesInfo = getPriceCounts(productID);
    var productHeightHtml = '';
    var i = 0;
    var priceInfo = {};

    for(var count in pricesInfo){
        if(pricesInfo.hasOwnProperty(count))
        {
            if(!i){
                priceInfo = pricesInfo[count];
                i++;
            }
            productHeightHtml += '<option value="' + count + '">' + count + ' шт.</option>';
        }
    }

    $('#product_count_' + productID).html(productHeightHtml);
    updateProductPrice(productID, priceInfo);
}


function productCountChanged(productID){
    productID = productID.toString();
    var priceInfo = getPriceCounts(productID);
    priceInfo = priceInfo[parseInt($('#product_count_' + productID + ' option:selected').attr('value'))];
    $('#product_price_id').attr('value', priceInfo['id'].toString());
    updateProductPrice(productID, priceInfo);
}


function rupluralize(value, arg){
    var bits = arg.split(',');
    if(value % 10 == 1 && value % 100 != 11)
        return bits[0];
    else if (2 <= value % 10 && value % 10 <= 4 && (value % 100 < 10 || value % 100 >= 20))
        return bits[1];
    else
        return bits[2];
}

function show_plus_payment()
{
    $('#additions_delivery').show();
    $.placeholder.shim();
}


function orderFormChanged(){
//    Если выбран способ оплаты наличными курьеру или стоит галка Я сам являюсь получателем, то потухает (они не активны) везти без звонка, отправить смс, сделать фото.
    var pay_type = $('#pay_type').val(),
        customer_is_destination = $('#id_customer_is_destination'),
        phone_only = $('#id_phone_only'),
        anonymous_delivery = $('#id_anonymous_delivery');

    if (phone_only.prop('checked')){
        if (customer_is_destination.prop('checked')) {
            customer_is_destination.click();
        }
        customer_is_destination.attr('disabled', '');

        $('#id_destination_address').attr('disabled', '');
    }
    else{
        $('#id_destination_address').removeAttr('disabled');

        if (anonymous_delivery.prop('checked')){
            if (customer_is_destination.prop('checked')) {
                customer_is_destination.click();
            }
            customer_is_destination.attr('disabled', '')
        }
        else{
            $('#id_customer_is_destination').removeAttr('disabled');
        }
    }


    if(customer_is_destination.prop('checked')){
        $('#id_destination_name, #id_destination_phone').attr('disabled', '');

        if (anonymous_delivery.prop('checked')){
            anonymous_delivery.click();
        }
        anonymous_delivery.attr('disabled', '');

        if (phone_only.prop('checked')){
            phone_only.click();
        }
        phone_only.attr('disabled', '');
    }
    else{
        $('#id_destination_name, #id_destination_phone').removeAttr('disabled');

        anonymous_delivery.removeAttr('disabled');
        phone_only.removeAttr('disabled');
    }

    if (pay_type == 'nalk' || customer_is_destination.prop('checked')){
        $('#clarify_type_0').click();
        $('#clarify_type_1').attr('disabled', '');

        $('#id_make_photo, #id_send_sms').attr('disabled', '').prop('checked', false).removeAttr('checked');
    }
    else{
        $('#clarify_type_1').removeAttr('disabled');

        $('#id_make_photo, #id_send_sms').removeAttr('disabled');
    }
}














$(document).ready(
    function()
    {
        $(document).on('click', '.first_menu.Alert', function()
        {
            $('#alert_popup').css("display", "block");
            $('#popup_layout').show();
        });
    }
);

$(document).ready(
    function()
    {
        $(document).on('click', '#alert_popup a, #popup_layout, #alert_popup .close', function()
        {
			$('#alert_popup').css("display", "none");
            $('#popup_layout').hide();
        });
    }
);