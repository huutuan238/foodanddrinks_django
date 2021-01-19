$(document).ready(function () {
    var element = document.getElementsByClassName('btn_profile');
    for (var x = 0; x < element.length; x++) {
        if (element[x].getAttribute('value') == localStorage.getItem("current")) {
            element[x].className = "btn_profile activated";
            localStorage.setItem("current", $(this).attr('value'));

        }
    }

    $('.btn_profile').click(function () {
        for (var x = 0; x < element.length; x++) {
            if (element[x].getAttribute('value') == $(this).attr('value')) {
                localStorage.setItem("current", $(this).attr('value'));
            }
        }
    });

    $('#user').click(function () {
        localStorage.setItem("current", 0);
    });
});

