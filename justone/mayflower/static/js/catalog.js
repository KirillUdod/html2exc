$('document').ready(function(){
    $(".header, .header_mo").click(function(){
        if (!$(this).hasClass('unactive')){
            $(this).addClass("active");
            $(this).siblings().removeClass("active");
            $(".delivery_block").removeClass("active");

            var selectedDeliveryType = $(this).attr('rel');
            $(".delivery_block[rel='" + selectedDeliveryType + "']").addClass("active");
            updateDeliveryType(selectedDeliveryType);
        }
    });

    $("#delivery .delivery_row").addClass("active");
    $("#delivery .delivery_row_mo").removeClass("active");

    $(".country_but").addClass("active").click(function(){
        if (!$(".delivery_blocker .header.active").length){
            $(".delivery_blocker .header:first").click();
        }
        $(this).addClass("active");
        $(".delivery_row").addClass("active");
        $(".delivery_row_mo").removeClass("active");
        $(".country_but_mo").removeClass("active");

        var $active = $(".delivery_blocker .header.active:visible");

        if ($active.length){
            $active.click();
        }
        else{
            $(".delivery_blocker .header:visible:first").click();
        }
    });

    $(".country_but_mo").click(function(){
        if (!$(".delivery_blocker_mo .header_mo.active").length){
            $(".delivery_blocker_mo .header_mo:first").click();
        }
        $(".delivery_row, #dd_delivery").removeClass("active");
        $(".delivery_row_mo").addClass("active");
        $(this).addClass("active");
        $(".country_but").removeClass("active");

        var selectedDeliveryType = $(".delivery_blocker_mo .header_mo.active").attr('rel');
        $(".delivery_block[rel='" + selectedDeliveryType + "']").addClass("active");
        updateDeliveryType(selectedDeliveryType);
    });

    $('.mo_price').on('change', function(){
        var selectedType = $(this).attr('name').split('_');
        updateDeliveryType(selectedType[selectedType.length - 1]);
    });

    var selectedDeliveryType = parseInt('{{ order_form.cleaned_data.delivery_type }}');

    if (selectedDeliveryType == 5 || selectedDeliveryType == 6){
        $(".delivery_blocker_mo .header_mo[rel='" + selectedDeliveryType + "']").click();
        $(".country_but_mo").click();
    }
    else {
        var defaultDeliveryType = '1';

        if (!$('.header[rel=4]').hasClass('unactive')) defaultDeliveryType = '4';


        $(".delivery_blocker .header[rel='" + (selectedDeliveryType || defaultDeliveryType) + "']").click();
    }
});


function updateDeliveryType(selectedDeliveryType){
    if (window.deliveryTypes) {
        $('#delivery_type').val(selectedDeliveryType);

        selectedDeliveryType = parseInt(selectedDeliveryType);
        var price = deliveryTypes[selectedDeliveryType];

        if ($.isArray(price)) {
            price = price[parseInt($('select[name="delivery_price_' + selectedDeliveryType + '"]').val())]
        }

        var orderSummWithoutDelivery = parseInt($('#order_summ').html().replace(' ', '')) - selectedDeliveryPrice;

        selectedDeliveryPrice = price;
        updateBasketForSummary(orderSummWithoutDelivery.toString());
        $('#order_delivery_price span').html(price);
    }
}