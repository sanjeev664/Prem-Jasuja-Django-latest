const feedback = document.querySelector(".alert");
$('#UserForm').on('submit', function(e) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val()

    e.preventDefault();
    $.ajax({
        type: "POST",
        url: "/accounts/signup/",
        caches: false,
        data: {
            csrfmiddlewaretoken: csrf_token,
            username: $('#username').val(),
            email: $('#email').val(),
            dob: $('#dob').val(),
            phone: $('#phone').val(),
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
            console.log(data)
            console.log(data)
            debugger
            if (data.status == true) {
                // $.notifyBar({
                //     cssClass: "success",
                //     html: data.msg,
                //     close: true,
                //     waitingForClose: false,
                // });

                feedback.style.visibility = "visible"
                feedback.textContent = data.msg;
                // setTimeout(function() {
                //     // window.location.href = '/'
                //     // window.location.replace("/");
                //     window.location.pathname = "/";

                // }, 1000);
                if (data.html == false) {
                    setTimeout(function() {
                        window.location.href = '/'
                            // window.location.replace("/");
                            // window.location.pathname = "/";
                    }, 1000);
                } else {
                    $('body').html(data.html);
                }
            } else {
                feedback.style.visibility = "visible"
                feedback.textContent = data.msg;
                return
                // $.notifyBar({
                //     cssClass: "error",
                //     html: data.msg,
                //     close: true,
                //     waitingForClose: false,
                // });
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

//forgot password
$('#forgotpassword-form').on('submit', function(e) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val()
    e.preventDefault();
    new_password = $('#email').val();

    $('#send-email').on('click', function(e) {
        alert("email")

    });
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



$('#forgotpassword-form').on('submit', function(e) {
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val()
    e.preventDefault();
    email = $('#email').val();
    step = $('#submit_btn').attr("steptype");

    console.log($('#code').val(), "************")
        //  $('#send-email').on('click', function(e) {
        //      alert("email")
        //  });
    $.ajax({
        type: "POST",
        url: "/accounts/forgot-password",
        data: {
            csrfmiddlewaretoken: csrf_token,
            email: $('#email').val(),
            step: step,
            otpfeild: $('#code').val(),
            dataType: "json",
        },
        beforeSend: function() {
            $('#loader').removeClass('hidden')
        },

        success: function(data) {
            console.log(data)
            if (data.status == 200) {

                $("#emaillegend").html(` <legend>
                <label for="code">Code:</label>
                <div class="input-group d-flex">
                    <input type="tel"  maxlength="7"  id="code" />
                    <button class="code_btn">Send code <span class="countdown"></span></button>
                </div>
            </legend>`)
            } else {

                feedback.style.visibility = "visible"
                feedback.textContent = data.msg;
            }
        },

        failure: function() {

        },
        complete: function() {
            $('#loader').addClass('hidden')
        },


    });


});