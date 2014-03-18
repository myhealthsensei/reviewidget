function init() {

    $('#publicbutton').on('click', buttonclick);
    $('#publicbutton').click().click()  // silly, but spares some templating code

    }

function buttonclick() {
    var val = $('#publicinput').val();
    var input = $('#publicinput');

    if ( val == 'True' ) {
        $(this).html('Resource is PRIVATE');
        input.val('False');
            
        } else {
        $(this).html('Resource is PUBLIC');
        input.val('True');
        }

    $(this).toggleClass('True False')
    
    }

$(document).ready(init)
