function showPreloader(){
    var $popup = $('#preloader_popup'),
        $preloader = $('#preloader');
    $popup.show();
    $preloader.css({left: ($popup.width() - $preloader.width()) / 2, top: ($popup.height() - $preloader.height()) / 2});
}

function hidePreloader(){
    $('#preloader_popup').hide();
}


function updateCompositionBackground(imagePath){
    var img = new Image();
    img.onload = function(){
        hidePreloader();
        $('#composition').css('background-image', 'url(' + imagePath + ')');
    };
    img.src = imagePath;
}


function calcCompositionHeight(){
    return Math.max(
            $(window).height() - $('#header').outerHeight() - $('#composition_name').outerHeight() - $('#footer').outerHeight(),
            $('#composition_description_wrap').outerHeight(true) + $('#category_carousel').outerHeight()
    );
}

function setComposition(number){
    number = parseInt(number);

    if (window.current_number == number){
        return;
    }

    if (number < 1 || number > window.categoryCompositionsUrls.length){
        return;
    }

    showPreloader();

    $.ajax({
        url: window.categoryCompositionsUrls[number - 1],
        success: function(response){
            updateCompositionBackground(response.image);
            var prev_number = number - 1,
                next_number = number + 1;

            if (prev_number < 1){
                $('#previous_composition').hide().attr('href', '');
            }
            else{
                $('#previous_composition').show().attr('href', window.categoryCompositionsUrls[prev_number - 1]);
            }

            if (next_number > window.categoryCompositionsUrls.length){
                $('.next_composition').hide();
            }
            else{
                $('.next_composition').show().attr('href', window.categoryCompositionsUrls[next_number - 1]);
            }

            for (var key in response){
                if (response.hasOwnProperty(key)){
                    $('#composition_' + key + ', .composition_' + key).html(response[key]);
                }
            }
            $("#owl-carousel").trigger("owl.jumpTo", number - 1);
            $('#composition_number').html(number);
            $('#composition_description_wrap .toolBar__card, #composition_description_wrap .toolBar__cardClose a').slideDown();

            window.current_number = number;
            history.replaceState({}, '', window.categoryCompositionsUrls[number - 1]);
        },
        error: function(){
            alert('Произошла ошибка. Попробуйте позже.');
        }
    });


}

$('document').ready(function(){
    $('.toolBar__cardClose > a').click(function(){
        $('.toolBar__card').slideUp(200);
        $(this).slideUp(10);
    });

   	if (typeof($.fn.owlCarousel)!="undefined") {
		$('#owl-carousel').owlCarousel({
			loop:false,
			navText: false,
			margin: 1,
			nav: true,
			items : 6,
			itemsCustom : false,
			singleItem : false,
			itemsScaleUp : false,
            responsive: false,
            autoWidth: true
		});
        $("#owl-carousel").trigger("owl.jumpTo", window.currentNumber - 1);
	}

    $('#composition').height(calcCompositionHeight());

    $('#category_carousel a.compositions').on('click', function(event){
        event.preventDefault();
        setComposition($(this).attr('rel'));
        return false;
    });

    $('.next_composition').on('click', function(event){
        event.preventDefault();
        var next_comp_number = window.current_number + 1;

        if (next_comp_number > categoryCompositionsUrls.length){
            $(this).hide();
            return;
        }

        setComposition(next_comp_number);
    });

    $('#previous_composition').on('click', function(event){
        event.preventDefault();
        var prev_comp_number = window.current_number - 1;

        if (prev_comp_number < 1){
            $(this).hide();
            return;
        }

        setComposition(prev_comp_number);
    });
});

$(window).on("resize",function(){
    $('#composition').height(calcCompositionHeight());
});