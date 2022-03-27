const Toast = Swal.mixin({
    toast: true,
    position: 'top-end',
    showConfirmButton: false,
    showCloseButton: true,
    timer: 2000,
    timerProgressBar: true,
    didOpen: (toast) => {
        //toast.addEventListener('mouseenter', Swal.stopTimer)
        //toast.addEventListener('mouseleave', Swal.resumeTimer)
    }
})

function msg(text, type) {
    if (typeof type == 'undefined') type = 'success'
    Toast.fire({
        icon: type,
        title: text,
    })
}

function removeMessage() {
    $('.systemmessage').slideUp(350, function () {
        $(this).remove();
    })
}


jQuery(document).ready(function ($) {
    /* https://bulma.io/documentation/components/navbar/ */
    // Check for click events on the navbar burger icon
    $(".navbar-burger").click(function () {
        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
        $(".navbar-burger").toggleClass("is-active");
        $(".navbar-menu").toggleClass("is-active");

    });

    // show a welcome messag eon home page - probably remove at some point
    if ($('.home').length) {
        msg('Welcome to Partnership 4 Kids Attendance System')
        $(document).on('click', '.navbar-burger', function () {
            $(".navbar-burger").toggleClass("is-active");
            $(".navbar-menu").toggleClass("is-active");

        })
    }

    $(document).on('click', '.notification .delete', function () {
            $(this).closest('.notification').slideUp(500, function(){
                remove();
            })
        })

    if ($('.systemmessage').length) {
        $(document).on('click', '.systemmessage .delete', function () {
            removeMessage()
        })

        setTimeout(function () {
            removeMessage()
        }, 5000)
    }

    $(document).on('click', '.studentattendancerow button', function () {
        $parent = $(this).closest('.studentattendancerow');
        if ($(this).hasClass('is-primary')) {
            $(this).removeClass('is-primary');
        } else {
            $parent.find('button').removeClass('is-primary');
            $(this).addClass('is-primary')
        }
    })




})