// phone home to load any comments
$.get('/reviews', render)

// bind to the form button to handle posts
$(document).ready( function() {
    $('#reviewsubmit').on('click', submit)
    })

function submit () {
    console.log('CLICK')

    // pick the values out of the form
    var review = $('#reviewidget textarea').val()
    var author = $('#author').val()
    var email = $('#email').val()

    $.post('/reviews', {'review':review, 'author':author, 'email':email})

    }

function render(data) {

    // grab reviews as JSON, append to <div>

    }
