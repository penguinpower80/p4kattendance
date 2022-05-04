jQuery(document).ready(function($){
    $(document).on('click', '[data-action="collapse"]', function(e){
        e.preventDefault()

        $(this).find('.fas').toggleClass('fa-caret-right fa-caret-down')
        $(this).find('.action').toggleClass('is-hidden')



        let $parent = $(this).closest('article')
        $parent.find('> .message-body').toggleClass('collapsed')



        if ( $(this).hasClass('active')  ) {
            $(this).removeClass('active')

        } else {

            $(this).addClass('active')
            let type = $(this).data('type')
            if (type === 'C') {
                let id = $(this).data('id')
                getMeetingList(type, id, function(list){
                    if ( list.length ) {
                        $parent.find('.is-meeting').remove()
                        for (x in list) {
                            let thisList = list[x]
                            let link = "<li><a id='meeting-"+thisList.id+"' class='is-meeting button is-fullwidth is-outlined is-info' href='/meeting/"+ thisList.id+"'>" + thisList.formatted + "</a></li>"
                            if ( thisList.type == 'C' ) {
                                $('#classroom-' + id).find('#classroommeetings_' + thisList.tid).append( link )
                            }
                            if ( thisList.type == 'P' ) {
                                $('#classroom-' + id).find('#studentmeetings_' + thisList.tid).append( link )
                            }
                        }
                    }
                    else {
                        console.log('no meetings')
                    }
                })
            }
        }

    })

    // $(document).on('click', '.p4kaccordian input[type="checkbox"]', function(){
    //     if ( this.checked ) {
    //         $(this).closest('article').find('input').prop('checked', true);
    //     }
    // })
})