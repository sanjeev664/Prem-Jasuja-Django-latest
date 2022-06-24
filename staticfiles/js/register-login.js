$('#UserForm').on('submit', function(e) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val()
    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/accounts/register/",
        data: {
            csrfmiddlewaretoken: csrf_token,
            username: $('#username').val(),
            email: $('#email').val(),
            fullname: $('#fullname').val(),
            password: $('#password').val(),
            confirm_password: $('#confirm-password').val(),
            page_type: $('#page-type').val(),
            dataType: "json",
        },
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        },

        success: function(data) {
            if (data.status == true) {
                $.notifyBar({
                    cssClass: "success",
                    html: data.msg,
                    close: true,
                    waitingForClose: false,
                });
                if (data.html ==false) {
                    setTimeout(function () {
                     window.location.href = '/'
                 }, 1000);
                }
                else {
                  $('body').html(data.html);  
                }
            } 
            else {

                $.notifyBar({
                    cssClass: "error",
                    html: data.msg,
                    close: true,
                    waitingForClose: false,
                });
            }
        },

        failure: function() {

        },
        complete: function() {
            $('#loader').addClass('hidden')
        },


    });


});



$('#PasswordForm').on('submit', function(e) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val()
    e.preventDefault();
    new_password = $('#new_password').val();
    confirm_password = $('#confirm_password').val();

    $.ajax({
        type: "POST",
        url: "/accounts/change-password/",
        data: {
            csrfmiddlewaretoken: csrf_token,
            old_password: $('#old_password').val(),
            new_password: $('#new_password').val(),
            confirm_password: $('#confirm_password').val(),
            dataType: "json",
        },
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        },

        success: function(data) {
            if (data.status == true) {
                $.notifyBar({
                    cssClass: "success",
                    html: data.msg,
                    close: true,
                    waitingForClose: false,
                });
                setTimeout(function() {
                    window.location.href = "/"
                }, 1000);
            } else {

                $.notifyBar({
                    cssClass: "error",
                    html: data.msg,
                    close: true,
                    waitingForClose: false,
                });
            }
        },

        failure: function() {

        },
        complete: function() {
            $('#loader').addClass('hidden')
        },


    });


});