$(document).ready(function () {
    var maxLength = 240;
    $(".right_part p").each(function () {
        var myStr = $(this).text();
        if ($.trim(myStr).length > maxLength) {
            var newStr = myStr.substring(0, maxLength);
            var removedStr = myStr.substring(maxLength, $.trim(myStr).length);
            $(this).empty().html(newStr);
            $(this).append('...');
            //$(this).append('<span class="more-text">' + removedStr + '</span>');
        }
    });
});

$(window).on("load", function () {
    var viewPortWidth = $(window).width();
    if (viewPortWidth < 992) {
        $(".mbl-search button").click(function (e) {
            $(".header-search.mbl-search").toggleClass("active");
        });

        $(".navbar-toggler").click(function (e) {
            $(".header-search.mbl-search, .header-search.mbl-search .dropdown").toggleClass("invisible");
        });
    };

    $(".red-hearta").on("click", function () {
        $(this).parent().parent().parent().parent().siblings().children().removeClass("active");
        $(this).parent().parent().parent().toggleClass("active");
    });

    var viewPortWidth = $(window).width();
    if (viewPortWidth > 992) {
        $(".user-icon .nav-link").on("click", function () {
            $(this).parent().toggleClass("active");
        });
    };
});


