let nomenclature = document.getElementById('nomenclature');
let name = document.getElementById('name');
let editButton = document.getElementById('editButton');
let concurrencyBtn = document.getElementById('concurrencyBtn');
let concurrencyHeader = document.getElementById('concurrencyHeader');
let oldData = document.getElementById('old');
let newData = document.getElementById('new');

function editNomenclatureName(name, nomID, nomVersion) {
    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/nomenclature/${nomID}/update/`,
        method: 'patch',
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        data: JSON.stringify({
            'name': name,
            'version': nomVersion
        }),
        dataType: 'json',
        contentType: 'application/json',
        success: function (data) {
            if (data['error'] === undefined) {
                nomenclature.selectedOptions[0].innerText = data['name'];
                nomenclature.selectedOptions[0].dataset['version'] = data['version'];
            } else {
                concurrencyBtn.click();

                concurrencyHeader.innerText = data['error'];
                oldData.innerText = data['current_data']['name'];
                newData.innerText = data['new_data']['name'];

                let updateBtn = document.getElementById('updateBtn');
                let closeBtn1 = document.getElementById('closeBtn1');
                let closeBtn2 = document.getElementById('closeBtn2');

                updateBtn.addEventListener('click', e => {
                    $.ajax({
                        url: `${locationHost}/org/1/tp/${tpID}/nomenclature/${nomID}/update/concurrency/`,
                        method: 'patch',
                        headers: {'X-CSRFToken': $.cookie('csrftoken')},
                        data: JSON.stringify({
                            'name': data['new_data']['name'],
                        }),
                        dataType: 'json',
                        contentType: 'application/json',
                        success: (data) => {
                            nomenclature.selectedOptions[0].innerText = data['name'];
                            name.value = nomenclature.selectedOptions[0].innerText;
                            nomenclature.selectedOptions[0].dataset['version'] = data['version'];
                        }
                    })
                })

                closeBtn1.addEventListener('click', e => {
                    $.ajax({
                        url: `${locationHost}/org/1/tp/${tpID}/nomenclature/${nomID}/update/`,
                        method: 'get',
                        success: (data) => {
                            let name = document.getElementById('name');
                            nomenclature.selectedOptions[0].innerText = data['name'];
                            name.value = data['name'];
                            nomenclature.selectedOptions[0].dataset['version'] = data['version'];
                        }
                    })
                })
                closeBtn2.addEventListener('click', e => {
                    $.ajax({
                        url: `${locationHost}/org/1/tp/${tpID}/nomenclature/${nomID}/update/`,
                        method: 'get',
                        success: (data) => {
                            let name = document.getElementById('name');
                            nomenclature.selectedOptions[0].innerText = data['name'];
                            name.value = data['name'];
                            nomenclature.selectedOptions[0].dataset['version'] = data['version'];
                        }
                    })
                })
            }
        },
        error: function (response) {
            console.log(response);
        }
    });
}

name.value = nomenclature.selectedOptions[0].innerText;

editButton.addEventListener('click', () => {
    editNomenclatureName(name.value, nomenclature.value, eval(nomenclature.selectedOptions[0].dataset['version']));
})

nomenclature.addEventListener('change', (e) => {
    name.value = nomenclature.selectedOptions[0].innerText;
})
