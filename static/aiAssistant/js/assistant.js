$(document).ready(function () {
    let $form = $('#assistant-form');


    $form.on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST', url: $form.attr('action'), data: $form.serialize(), success: function (response) {
                console.log(response);
                $('#assistant-response').html(response);
            },
        });
    });

});