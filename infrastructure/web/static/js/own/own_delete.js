var ownDeleteForm = document.getElementById('ownDeleteForm');
var modalString = document.getElementById('ownModalQuestion')


ownDeleteForm.addEventListener('submit', (e) => {
    e.preventDefault();
    console.log('Удалить')
    var ownIdInput = document.getElementById('own_id');
    $.ajax({
        url: `${locationHost}/org/${ownIdInput.dataset['orgId']}/tp/${tpID}/contractor/${ownIdInput.dataset['contrId']}/own/${ownIdInput.value}/delete/`,
        method: 'post',
        dataType: 'json',
        contentType: 'application/json',
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: JSON.stringify({
            own_id: ownIdInput.value
        }),
        success: (response) => {
            var modal = document.getElementById('own_modal');
            var modalBackDrop = document.getElementsByClassName('modal-backdrop')[0];
            modal.classList.remove('show');
            modalBackDrop.classList.remove('show');

            var div = document.getElementById(`own_instance_${ownIdInput.value}`);
            tableBody.removeChild(div);
            if (!tableBody.hasChildNodes()) {
                tableHead.innerHTML = '';
                emptyBody.innerHTML = '<p style="text-align:center; margin-top: 15px">Добавьте собственность в список</p>';
            }
        },
        error: (response) => {
            console.log(response);
        }
    })
})
