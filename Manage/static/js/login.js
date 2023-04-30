
$(document).ready(function () {
    $('input[name="username"]').focus();
});
(function ($) {
    "use strict";
    $('.input100').each(function () {
        $(this).on('blur', function () {
            if ($(this).val().trim() != "") {
                $(this).addClass('has-val');
            }
            else {
                $(this).removeClass('has-val');
            }
        })
    })


    /*==================================================================
    [ Validate ]*/
    /*==================================================================
    [ Validate ]*/
    var input = $('#form1 .validate-input .input100');

    $('#form1 .validate-form').on('submit', function () {
        var check = true;
        console.log(2)
        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }

        return check;
    });

    $('#form1 .validate-form .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });
    var input = $('#form2 .validate-input .input100');

    $('#form2 .validate-form').on('submit', function () {
        var check = true;
        console.log(2)
        for (var i = 0; i < input.length; i++) {
            if (validate(input[i]) == false) {
                showValidate(input[i]);
                check = false;
            }
        }

        return check;
    });

    $('#form2 .validate-form .input100').each(function () {
        $(this).focus(function () {
            hideValidate(this);
        });
    });
    function validate(input) {
        if ($(input).val().trim() == '') {
            return false;
        }
    }

    function showValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).addClass('alert-validate');
    }

    function hideValidate(input) {
        var thisAlert = $(input).parent();
        $(thisAlert).removeClass('alert-validate');
    }


})(jQuery);
