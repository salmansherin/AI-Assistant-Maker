$(document).ready(function () {
    let $form = $('#assistant-form');
    let $fileForm = $('#upload-file-form');
    let $fileInput = $('#file-input');
    let assistant_id = $('#assistant_id').val();

    $form.on('submit', function (e) {
        e.preventDefault();
        $.ajax({
            type: 'POST', url: $form.attr('action'), data: $form.serialize(), success: function (response) {
                console.log(response);
                $('#assistant-response').html(response);
            },
        });
    });

    $fileInput.on('change', function (e) {
        let file = this.files[0]; // Get the selected file
        let formData = new FormData();
        formData.append('file', file); // Append the file to the form data
        $fileForm.find('input:not([type=file])').each(function () {
            formData.append(this.name, this.value);
        });
        $.ajax({
            url: '/files/' + assistant_id, // Replace with your upload URL
            type: 'POST', data: formData, processData: false, // Important! Tell jQuery not to process the data
            contentType: false, // Important! Tell jQuery not to set contentType
            success: function (response) {
                console.log('File uploaded successfully');
                $fileForm[0].reset()
            }, error: function (jqXHR, textStatus, errorThrown) {
                console.log('File upload failed');
                $fileForm[0].reset()
            }
        });
    });

    getFiles(assistant_id);

});

function formatTimestamp(timestamp) {
    let date = new Date(timestamp * 1000); // Convert timestamp to milliseconds
    let year = date.getFullYear();
    let month = date.getMonth() + 1; // Months are zero based
    let day = date.getDate();
    let hours = date.getHours();
    let minutes = "0" + date.getMinutes();
    let ampm = hours >= 12 ? 'pm' : 'am';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0' + minutes : minutes;
    let strTime = month + "/" + day + "/" + year + " " + hours + ':' + minutes.substr(-2) + ' ' + ampm;
    return strTime;
}

/**
 * Get assistant files
 * @param assistant_id
 */
const getFiles = (assistant_id) => {
    let $table = $('#assistant-files > tbody');
    $table.empty();
    $.ajax({
        type: 'GET', url: '/files/' + assistant_id, success: function (res) {
            res.data.map(item => {
                $table.append(`<tr>
<td>${item.id}</td>
<td>${item.object}</td>
<td>${formatTimestamp(item.created_at)}</td>
<td></td>
</tr>`);
            })
        },
    });
}// getFiles