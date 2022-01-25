const form   = document.getElementById('form');
const alerts = document.getElementById('alerts');
const image = document.getElementById('image');

$('#upload').change(function(){
    let path = $(this).val().replace('C:\\fakepath\\', '');
    $('#selectFile').html(path);
})

const flash = (message, level) => {
    alerts.innerHTML += `
        <div class="alert alert-${level}" role="alert">
            <p id="closeAlert" class="close" data-dismiss="alert" aria-label="Close"></p>
            <strong>${message}</strong>
        </div>
    `;
};

form.addEventListener('submit', e => {
    e.preventDefault();

    let image = $('#upload')[0].files[0]

    let formData = new FormData();
    formData.append('file', image);

    axios
        .post('/api/upload', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(({ data }) => {
            if (!data.image) {
                flash(data.message, 'danger');
            } else {
                $('#image').attr('src', data.image);
            }
        })
});