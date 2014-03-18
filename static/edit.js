function init() {

    $('#publicbutton').on('click', buttonclick);
    $('#publicbutton').click().click()  // silly, but spares some templating code

    }

function buttonclick() {
    var val = $(this).val();

    if ( val == 'True' ) {
        $(this).val('False').html('Resource is PRIVATE')
        } else {
        $(this).val('True').html('Resource is PUBLIC')
        }

    $(this).toggleClass('True False')
    
    }

$(document).ready(init)
