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

    $.post('/reviews', {'review':review})

    }

function render(data) {

    // grab reviews as JSON, append to <div>

    }
