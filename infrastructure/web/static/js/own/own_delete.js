var ownDeleteForm = document.getElementById('ownDeleteForm');
var btnDeleteList = Object.values(document.getElementsByClassName('buttonDelete'));
var modalString = document.getElementById('ownModalQuestion')

btnDeleteList.forEach(element => {
    element.addEventListener('click', (e) => {
        var ownIdInput = document.getElementById('own_id');
        var ownId = element.dataset['own_id'];

        ownIdInput.value = ownId;
        ownIdInput.dataset['orgId'] = element.dataset['org_id'];
        ownIdInput.dataset['contrId'] = element.dataset['contr_id'];

        modalString.innerHTML = `<p>Собственность #${ownIdInput.value} будет удалена из списка навсегда. Вы уверены?</p>`
    })
})

ownDeleteForm.addEventListener('submit', (e) => {
    e.preventDefault();

    var ownIdInput = document.getElementById('own_id');


    $.ajax({
        url: `http://127.0.0.1:8000/org/${ownIdInput.dataset['orgId']}/tp/${tpID}/contractor/${ownIdInput.dataset['contrId']}/own/${ownIdInput.value}/delete/`,
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
            div.remove();
            const element = document.createElement("div");
            element.appendChild(document.createTextNode('У этого котрактора пока нет собственности'));
            document.getElementById('w').appendChild(element);
        },
        error: (response) => {
            console.log(response);
        }
    })
})