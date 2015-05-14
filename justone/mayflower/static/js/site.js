$(function() {
    $('a[href="#"]').on("click", function() {
        return false
    });

	if (typeof($.fn.responsiveSlides)!="undefined") {
		$(".hSl__slider").responsiveSlides({
			manualControls: '.hSl__pagination',
			//maxwidth: 1240,
			auto: true,
			pager: true,
			nav: true,
			speed: 500,
			prevText: '',
			nextText: ''
		  });
	}
	// === DATEPICKER === //

	if (typeof($.fn.datepicker)!="undefined") {
		var datePicObj = $('#blog_calendar');
        window.selectedMonth = '';

		datePicObj.datepicker();

        if (window.filteredDate){
            datePicObj.datepicker("setDate", window.filteredDate);
        }

        datePicObj.datepicker('option', 'onChangeMonthYear', function(year, month) {
            window.selectedMonth = year + '.' + month;
        });

        datePicObj.datepicker('option', 'onSelect', function(){
            var currentDate = $(this).datepicker('getDate');
            window.location.href = window.location.pathname +
                '?date=' + currentDate.getFullYear().toString() + '.' + (currentDate.getMonth() + 1).toString()
                + '.' + currentDate.getDate();
        });

        datePicObj.on('click', '.ui-datepicker-title', function(){
            if (window.selectedMonth){
                window.location.href = window.location.pathname + '?month=' + window.selectedMonth;
            }
            else{
                var currentDate = datePicObj.datepicker('getDate');
                window.location.href = window.location.pathname +
                    '?month=' + currentDate.getFullYear().toString() + '.' + (currentDate.getMonth() + 1).toString();
            }
        });
	}

	// === BLOGS BORDER === //

		var blogObj = $('.bgNews__item');
		if (blogObj) {
			var blogObjSize = blogObj.size();
			for (var i = blogObjSize - blogObjSize % 3; i < blogObjSize; i++) {
				$(blogObj[i]).css({"border-bottom":"0"});
			}
		}

	// === CATALOG === //
		$('.mCa__item').on("focusin mouseenter", function () {
			$(this).find('.upLayer').show(300);
        }).on("focusout mouseleave", function () {
			$(this).find('.upLayer').hide(300);
        });

	// === Product ToolBar ===
		if (typeof($.fn.mCustomScrollbar)!="undefined") {
			$(window).load(function(){
				$(".mCa__scrollArea .mCa__list").mCustomScrollbar({
					axis:"y",
					setHeight: 800,
					setWidth: 1240
				});
			});
		}

	// === FeedBack popUp Form
	$(".hOv__callOrder").click(function(){
		var callObj = $('#back_call_form').parents('.hOv__callPopUp');
		callObj.show();

		$('body').keyup(function(e) {
		    if (e.keyCode == 27) {
				callObj.hide();
			}
		});
	});

	$('.feedBack .close').click(function(){
		$('.hOv__callPopUp').fadeOut();
	});

    $('#back_call_form').on('submit', function(event){
        event.preventDefault();

        $.ajax({
            url: $(this).attr('action'),
            data: $(this).serialize(),
            type: $(this).attr('method'),
            success: function(response){
                $('#back_call_form').html(response);
            },
            error: function(){
                alert('Произошла ошибка. Попробуйте позже.');
            }
        });

        return false;
    });

    ajaxForm(
        $('#login_popup form'),
        function(response){
            if (response.redirect){
                window.location = response.redirect;
            }

            if (response.form){
                $(this).html(response.form);
            }
        }
    );


    ajaxForm(
        $('#register_popup form'),
        function(response){
            if (response.redirect){
                window.location = response.redirect;
            }

            if (response.form){
                $(this).html(response.form);
                makeSelect2();
            }
        }
    );
});


function ajaxForm($targetForm, successCallback, errorCallback){
    $targetForm.on('submit', function(event){
        event.preventDefault();
        $.ajax({
            url: $targetForm.attr('action') || window.location.href,
            data: $targetForm.serialize(),
            type: $targetForm.attr('method') || 'get',
            cache: false,
            success: function (response) {
                if (successCallback) {
                    successCallback.call(this, response);
                }
            }.bind(this),
            error: function (xhr) {
                if (errorCallback) {
                    errorCallback.call(this, xhr);
                }
                else {
                    alert('Произошла ошибка. Попробуйте еще раз.');
                }
            }.bind(this)
        });
        return false;
    });
}

function login(){
    $('#login_popup').show();

    return false;
}


function register(){
    makeSelect2();
    $('#register_popup').show();

    return false;
}

function makeSelect2(){
    $('.hOv__callPopUp select').select2({
        width: 'style'
    });
}