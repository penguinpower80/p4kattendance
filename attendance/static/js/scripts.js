const Toast = Swal.mixin({
    toast: true,
    position: 'bottom-end',
    showConfirmButton: false,
    showCloseButton: true,
    timer: 1000,
    timerProgressBar: false,
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

function setMeetingDate(meeting, timestamp, callback){
        jQuery.post('/ajax/setmeetingdate/' + meeting, {
            timestamp: timestamp,
            csrfmiddlewaretoken: csrftoken
        }, function (data) {
            msg('Date set to ' + data)
            if ( callback ) callback(data)
        }).always(function () {
        }).fail(function (d) {
            if (d.status == 401) {
                msg('You are not allowed to do this.', 'error')
            }
            else {
                msg('There was an error setting the meeting date.', 'error')
            }
        })
}


function markStudentAttendance(meeting, student, status, callback) {
    jQuery.post('/ajax/markattendance/' + meeting + '/' + student, {
            status: status,
            csrfmiddlewaretoken: csrftoken
        }, function (data) {
            msg('Attendance marked!')
            if ( callback ) callback(data)
        }).always(function () {
        }).fail(function (d) {
            if (d.status == 401) {
                msg('You are not assigned to this user.', 'error')
            }
            else {
                msg('There was an error marking attendance.', 'error')
            }
        })
}

function getMeetingList(type, id, callback) {
    jQuery.get('/ajax/meetinglist/' + type + '/' + id, function (data) {
            if ( callback ) callback(data)

        }).always(function () {
        }).fail(function (d) {
            if (d.status == 401) {
                msg('You are not assigned to this user.', 'error')
            }
            else {
                msg('There was an error retrieving meeting list.', 'error')
            }



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

    // Initialize all input of type date
    var options = {
        showClearButton: false,
        displayMode: 'dialog',

    }
    var calendars = bulmaCalendar.attach('[type="date"]', options);

    calendars[ 0 ].on('select', date => {
        let meeting_id = date.data.element.dataset['meeting']
        setMeetingDate(meeting_id, date.data.value(), function(d){


        } )


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

    $(document).on('click', '.studentattendancerow .attendance button', function (e) {

        $parent = $(this).closest('.studentattendancerow');

        let $button = $(this)
        let student_id = $button.data('rel')
        let status = $button.data('status')
        let meeting_id = $button.data('meeting')

        if ($(this).is('is-primary is-warning is-danger')) {
            markStudentAttendance(meeting_id, student_id, 'remove', function(d){
                $button.removeClass('is-primary is-warning is-danger');
                e.preventDefault()
            })

        } else {
            let $button = $(this)
            let student_id = $(this).data('rel')
            let status = $(this).data('status')
            let meeting_id = $(this).data('meeting')
            markStudentAttendance(meeting_id, student_id, status, function(d){
                $parent.find('.attendance button').removeClass('is-primary is-warning is-danger');
                if ( status == 'p' )
                    $button.addClass('is-primary')
                else if( status=='a')
                    $button.addClass('is-danger')
                else if( status=='t')
                    $button.addClass('is-warning')
            })
            e.preventDefault()
        }
    })

})

// from bulma.io doc's
document.addEventListener('DOMContentLoaded', () => {
  // Functions to open and close a modal
  function openModal($el) {
    $el.classList.add('is-active');
  }

  function closeModal($el) {
    $el.classList.remove('is-active');
  }

  function closeAllModals() {
    (document.querySelectorAll('.modal') || []).forEach(($modal) => {
      closeModal($modal);
    });
  }

  // Add a click event on buttons to open a specific modal
  (document.querySelectorAll('.note-trigger') || []).forEach(($trigger) => {
    const modal = $trigger.dataset.target;
    const name = $trigger.dataset.name;
    const id = $trigger.dataset.id;
    const type = $trigger.dataset.typel
    const $target = document.getElementById(modal);


    $($target).find('.modal-card-title').html(name)

    $trigger.addEventListener('click', () => {
      openModal($target);
    });
  });

  // Add a click event on various child elements to close the parent modal
  (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button') || []).forEach(($close) => {
    const $target = $close.closest('.modal');

    $close.addEventListener('click', () => {
      closeModal($target);
    });
  });

  // Add a keyboard event to close all modals
  document.addEventListener('keydown', (event) => {
    const e = event || window.event;

    if (e.keyCode === 27) { // Escape key
      closeAllModals();
    }
  });
});