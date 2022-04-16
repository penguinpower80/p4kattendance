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

const buttonClass = {
    confirmButton: 'button is-primary',
    cancelButton: 'button is-danger'
}

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

function setMeetingDate(meeting, timestamp, callback) {
    jQuery.post('/ajax/setmeetingdate/' + meeting, {
        timestamp: timestamp,
        csrfmiddlewaretoken: csrftoken
    }, function (data) {
        msg('Date set to ' + data)
        if (callback) callback(data)
    }).always(function () {
    }).fail(function (d) {
        if (d.status == 401) {
            msg('You are not allowed to do this.', 'error')
        } else {
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
        if (callback) callback(data)
    }).always(function () {
    }).fail(function (d) {
        if (d.status == 401) {
            msg('You are not assigned to this user.', 'error')
        } else {
            msg('There was an error marking attendance.', 'error')
        }
    })
}

function saveNote(entity, id, visible, note, callback) {
    jQuery.post('/ajax/savenote/' + entity + '/' + id, {
        text: note,
        visible: visible,
        csrfmiddlewaretoken: csrftoken
    }, function (data) {
        msg('Note Saved!')
        if (callback) callback(data)
    }).always(function () {
    }).fail(function (d) {
        if (d.responseText) {
            msg(d.responseText, 'error')
        } else if (d.status == 401) {
            msg('You are not assigned to this user.', 'error')
        } else {
            msg('There was an error saving the note.', 'error')
        }
    })
}

function updateNote(id, visible, note, callback) {
    jQuery.post('/ajax/updatenote/' + id, {
        text: note,
        visible: visible,
        csrfmiddlewaretoken: csrftoken
    }, function (data) {
        msg('Note Updated!')
        if (callback) callback(data)
    }).always(function () {
    }).fail(function (d) {
        if (d.responseText) {
            msg(d.responseText, 'error')
        } else if (d.status == 401) {
            msg('You are not assigned to this user.', 'error')
        } else {
            msg('There was an error updating the note.', 'error')
        }
    })
}

function getMeetingList(type, id, callback) {
    jQuery.get('/ajax/meetinglist/' + type + '/' + id, function (data) {
        if (callback) callback(data)

    }).always(function () {
    }).fail(function (d) {
        if (d.status == 401) {
            msg('You are not assigned to this user.', 'error')
        } else {
            msg('There was an error retrieving meeting list.', 'error')
        }
    })
}


function deleteNote(id, callback) {
    jQuery.get('/ajax/note/delete/' + id, function (data) {
        if (callback) callback(data)
    }).always(function () {
    }).fail(function (d) {
        if (d.status == 401) {
            msg('You do not have these permissions.', 'error')
        } else {
            msg('There was an error deleting this note.', 'error')
        }
    })
}

function getNoteList(type, id, callback) {
    jQuery.get('/ajax/noteslist/' + type + '/' + id, function (data) {
        if (callback) callback(data)
    }).always(function () {
    }).fail(function (d) {
        if (d.status == 401) {
            msg('You are not assigned to this entity.', 'error')
        } else {
            msg('There was an error retrieving notes list.', 'error')
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
    const options = {
        showClearButton: false,
        displayMode: 'dialog',

    };
    const calendars = bulmaCalendar.attach('[type="date"]', options);
    if (calendars && calendars[0]) {
        calendars[0].on('select', date => {
            let meeting_id = date.data.element.dataset['meeting']
            setMeetingDate(meeting_id, date.data.value(), function (d) {


            })


        });
    }
    // show a welcome messag eon home page - probably remove at some point
    if ($('.home').length) {
        msg('Welcome to Partnership 4 Kids Attendance System')
        $(document).on('click', '.navbar-burger', function () {
            $(".navbar-burger").toggleClass("is-active");
            $(".navbar-menu").toggleClass("is-active");

        })
    }

    if ($('.systemmessage').length) {
        $(document).on('click', '.systemmessage .delete', function () {
            removeMessage()
        })

        setTimeout(function () {
            removeMessage()
        }, 5000)
    }

    $(document).on('click', '.notification .delete', function () {
        $(this).closest('.notification').slideUp(500, function () {
            remove();
        })
    })

    $(document).on('click', '.studentattendancerow .attendance button', function (e) {

        $parent = $(this).closest('.studentattendancerow');

        let $button = $(this)
        let student_id = $button.data('rel')
        let status = $button.data('status')
        let meeting_id = $button.data('meeting')

        if ($(this).is('is-primary is-warning is-danger')) {
            markStudentAttendance(meeting_id, student_id, 'remove', function (d) {
                $button.removeClass('is-primary is-warning is-danger');
                e.preventDefault()
            })

        } else {
            let $button = $(this)
            let student_id = $(this).data('rel')
            let status = $(this).data('status')
            let meeting_id = $(this).data('meeting')
            markStudentAttendance(meeting_id, student_id, status, function (d) {
                $parent.find('.attendance button').removeClass('is-primary is-warning is-danger');
                if (status == 'p')
                    $button.addClass('is-primary')
                else if (status == 'a')
                    $button.addClass('is-danger')
                else if (status == 't')
                    $button.addClass('is-warning')
            })
            e.preventDefault()
        }
    })

    $(document).on('click', '.deletemeeting', function (e) {
        e.preventDefault()
        let $button = $(this)
        let meeting = $button.data('rel');
        Swal.fire({
            customClass: buttonClass,
            title: 'Are you sure?',
            text: 'This will permanently delete this meeting and related attendance events!',
            icon: 'warning',
            showCancelButton: true,
            cancelButtonText: 'Cancel',
            confirmButtonText: 'Delete'
        }).then((result) => {
            if (result.isConfirmed) {
                parent.location = '/meeting/delete/' + meeting
            }
        })
    })

    $(document).on('click', '.deletenote', function (e) {
        e.preventDefault()
        let $button = $(this)
        let note = $button.data('rel');
        Swal.fire({
            customClass: buttonClass,
            title: 'Are you sure?',
            text: 'This will permanently delete this note!',
            icon: 'warning',
            showCancelButton: true,
            cancelButtonText: 'Cancel',
            confirmButtonText: 'Delete'
        }).then((result) => {
            if (result.isConfirmed) {
                deleteNote(note, function (d) {
                    $button.closest('.noterow').remove()
                    msg('Note deleted!')
                })
            }
        })
    })
})

$(document).on('click', '.editnote', function (e) {
    e.preventDefault()
    let $button = $(this)
    let note = $button.data('rel');
    let content = $button.closest('.card').find('.content').html()
    $button.closest('.card').css('opacity', '0.25')
    noteData['noteid'] = note
    CKEDITOR.instances['id_Note'].setData(content)
})

let noteData = {}
// from bulma.io doc's
document.addEventListener('DOMContentLoaded', () => {
    // Functions to open and close a modal
    function openModal($el) {
        $el.classList.add('is-active');
    }

    function closeModal($el) {
        noteData = {}
        $el.classList.remove('is-active');
        $('#noteslist').html('')
    }

    function closeAllModals() {
        (document.querySelectorAll('.modal') || []).forEach(($modal) => {
            closeModal($modal);
        });
    }

    // Add a click event on buttons to open a specific modal
    (document.querySelectorAll('.note-trigger') || []).forEach(($trigger) => {
        const modal = $trigger.dataset.target;
        const $target = document.getElementById(modal);


        $trigger.addEventListener('click', () => {
            const name = $trigger.dataset.name;
            const id = $trigger.dataset.id;
            const type = $trigger.dataset.type
            noteData = {
                name: name,
                id: id,
                type: type
            }
            $($target).find('.modal-card-title').html(name)

            $('#notevisible').prop('checked', true)
            openModal($target);
        });
    });

    // Add a click event on various child elements to close the parent modal
    (document.querySelectorAll('.modal-background, .modal-close, .modal-card-head .delete, .modal-card-foot .button.cancelnote') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            closeModal($target);
            CKEDITOR.instances['id_Note'].setData('')
        });
    });


    (document.querySelectorAll('.modal-card-foot .button.deletenote') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            closeModal($target);
            CKEDITOR.instances['id_Note'].setData('')
        });
    });


    (document.querySelectorAll('.modal-card-foot .button.savenote') || []).forEach(($close) => {
        const $target = $close.closest('.modal');

        $close.addEventListener('click', () => {
            note = CKEDITOR.instances['id_Note'].getData()
            let visible = 'true'
            if ($('#notevisible').length) {
                visible = $('#notevisible')[0].checked
            }

            if (noteData.noteid) {
                updateNote(noteData.noteid, visible, note, function (d) {
                    CKEDITOR.instances['id_Note'].setData('')
                    delete noteData.noteid
                    $('.modal-card-foot .button.listnotes').trigger('click')
                })
            } else {
                saveNote(noteData.type, noteData.id, visible, note, function (d) {
                    closeModal($target);
                    CKEDITOR.instances['id_Note'].setData('')
                })
            }


        });
    });
    (document.querySelectorAll('.modal-card-foot .button.listnotes') || []).forEach(($close) => {
        const $target = $close.closest('.modal');
        $close.addEventListener('click', () => {
            getNoteList(noteData.type, noteData.id, function (d) {
                let $holder = $('#noteslist')
                $holder.html('')
                if (d.msg) msg(d.msg)
                if (d.notes && d.notes.length) {
                    let template = document.querySelector('#noterow');
                    for (let note in d.notes) {
                        let thisNote = d.notes[note]
                        let clone = template.content.cloneNode(true)
                        clone.querySelectorAll('.card-header-title')[0].textContent = thisNote.author + ', ' + thisNote.created
                        if ( thisNote.created != thisNote.updated ) {
                            clone.querySelectorAll('.extranoteinfo')[0].textContent = "(updated " + thisNote.updated + ")";
                        }


                        clone.querySelectorAll('.content')[0].innerHTML = thisNote.text
                        /* clone.querySelectorAll('.updated')[0].textContent = thisNote.updated*/
                        /*clone.querySelectorAll('.editnote')[0].dataset.rel = thisNote.id*/
                        clone.querySelectorAll('.deletenote')[0].dataset.rel = thisNote.id
                        clone.querySelectorAll('.editnote')[0].dataset.rel = thisNote.id
                        if (thisNote.can_modify) {

                            clone.querySelectorAll('.deletenote')[0].classList.remove('is-hidden')
                            clone.querySelectorAll('.editnote')[0].classList.remove('is-hidden')
                            /*clone.querySelectorAll('.editnote')[0].classList.remove('is-hidden')*/
                        } else {
                            /*clone.querySelectorAll('.editnote')[0].classList.add('is-hidden')*/
                            clone.querySelectorAll('.deletenote')[0].classList.add('is-hidden')
                            clone.querySelectorAll('.editnote')[0].classList.add('is-hidden')
                        }
                        $holder.append(clone)
                    }
                }
            })
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