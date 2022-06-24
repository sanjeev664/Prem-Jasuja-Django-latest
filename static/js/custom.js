$(document).ready(function() {
    var maxLength = 240;
    $(".right_part p").each(function() {
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

$(window).on("load", function() {
    var viewPortWidth = $(window).width();
    if (viewPortWidth < 992) {
        $(".mbl-search button").click(function(e) {
            $(".header-search.mbl-search").toggleClass("active");
        });

        $(".navbar-toggler").click(function(e) {
            $(".header-search.mbl-search, .header-search.mbl-search .dropdown").toggleClass("invisible");
        });
    };

    $(".red-hearta").on("click", function() {
        $(this).parent().parent().parent().parent().siblings().children().removeClass("active");
        $(this).parent().parent().parent().toggleClass("active");
    });

    var viewPortWidth = $(window).width();
    if (viewPortWidth > 992) {
        $(".user-icon .nav-link").on("click", function() {
            $(this).parent().toggleClass("active");
        });
    };
});

//favicon
function setFavicons(favImg) {
    let headTitle = document.querySelector('head');
    let setFavicon = document.createElement('link');
    setFavicon.setAttribute('rel', 'shortcut icon');
    setFavicon.setAttribute('href', favImg);
    headTitle.appendChild(setFavicon);
}
setFavicons('./images/1.png');

//verification
// function verifyUser() {
//     if (!sessionStorage.getItem("user-details")) {
//         window.location.pathname = "/"
//     }
// }
// verifyUser();

//category sorting
const dropdownPlaceholder = document.querySelectorAll('.sort-categories .placeholder');
const sortDropdownList = document.querySelectorAll('.sort-dropdown');
const sortDropdownListIcon = document.querySelectorAll('.sort-categories .placeholder .icon');
const tagsList = document.querySelector('.tags-list');


function resetDropdown() {
    sortDropdownList.forEach(e => e.classList.remove('open'));
    sortDropdownListIcon.forEach(e => {
        e.style.transform = 'rotate(45deg)';
        e.style.top = '-3px';
    });
}

function createRipple(event) {
    const button = event.currentTarget;
    const circle = document.createElement('span');
    console.log();
    const diameter = Math.max(button.clientWidth, button.clientHeight);
    const radius = diameter / 2;
    circle.style.width = circle.style.height = `${diameter}px`;
    circle.style.left = `${button.clientWidth - (button.offsetLeft + radius)}px`;
    circle.style.top = `${button.clientHeight - (button.offsetTop + radius)}px`;
    console.log(event.clientX, button.clientWidth);
    circle.classList.add('ripple');
    let ripple = document.getElementsByClassName('ripple')[0];
    if (ripple) {
        ripple.remove()
    }
    button.appendChild(circle);
}


for (let i = 0; i < dropdownPlaceholder.length; i++) {
    dropdownPlaceholder[i].onclick = (e) => {
        createRipple(e);
        if (sortDropdownList[i].classList.contains('open')) {
            sortDropdownList[i].classList.remove('open');
            sortDropdownListIcon[i].style.transform = 'rotate(45deg)';
            sortDropdownListIcon[i].style.top = '-3px';
        } else {
            resetDropdown();
            sortDropdownList[i].classList.add('open');
            sortDropdownListIcon[i].style.transform = 'rotate(-135deg)';
            sortDropdownListIcon[i].style.top = '0px';
        }

    }
}

window.onclick = e => {
    if (!e.target.classList.contains('placeholder')) {
        resetDropdown();
    }
}

sortDropdownList.forEach(e => {
    let items = e.children;
    for (let i = 0; i < items.length; i++) {
        items[i].onclick = e => {
            let tag = document.createElement('li');
            let closeIcon = document.createElement('span')
            tag.classList.add('tag');
            closeIcon.classList.add('close-icon');
            closeIcon.onclick = () => tagsList.removeChild(tag);
            closeIcon.innerHTML = 'x';
            tag.innerHTML = e.target.innerHTML;
            tag.appendChild(closeIcon);
            tagsList.appendChild(tag)
        }
    }
})