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

jQuery(document).ready(function ($) {
     msg('Welcome to Partnership 4 Kids Attendance System')
        $(document).on('click', '.navbar-burger', function() {
          $(".navbar-burger").toggleClass("is-active");
          $(".navbar-menu").toggleClass("is-active");

      })
})