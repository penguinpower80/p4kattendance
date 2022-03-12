jQuery(document).ready(function($){
    $(document).on('click', '[data-action="collapse"]', function(e){
        e.preventDefault()
        $(this).closest('article').find('> .message-body').toggleClass('collapsed')
    })

    // $(document).on('click', '.p4kaccordian input[type="checkbox"]', function(){
    //     if ( this.checked ) {
    //         $(this).closest('article').find('input').prop('checked', true);
    //     }
    // })
})