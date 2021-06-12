let form = document.getElementById('contact-form');

form.addEventListener('submit', function (event) {
    event.preventDefault();
    send_form_ajax();
});

function send_form_ajax() {
    $.ajax({
        url: '/',
        data: $('form').serialize(),
        type: 'POST',
        success: function (response) {
            // console.log(data);
            console.log(response);
        },
        error: function (error) {
            console.log(error);
        }
    });
}