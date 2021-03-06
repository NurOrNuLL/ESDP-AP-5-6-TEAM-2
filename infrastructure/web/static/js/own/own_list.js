tableBody = document.getElementById('tableBody');
tableHead = document.getElementById('tableHead');
emptyBody = document.getElementById('emptyBody');
isPart = document.getElementById('isPart');
isNotPart = document.getElementById('isNotPart');
var buttonColection = document.getElementsByClassName('buttonDelete')


window.addEventListener('load', () => {
    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/contractor/${contrID}/own/list/filter/?is_part=false`,
        method: 'GET',
        success: (data) => {
            var ownIdInput = document.getElementById('own_id');
            isNotPart.checked = true;
            isPart.checked = false;
            tableHead.innerHTML = '';
            tableHead.innerHTML += '<tr><th class="col-2">Наименование</th><th class="col-2">Номер</th><th class="col-6">Комментарий</th><th class="col-2"></th></tr>'
            tableBody.innerHTML = '';
            emptyBody.innerHTML = '';

            if (data.results.length) {
                data.results.forEach(function (item) {
                    if (item.comment == null) {
                        item.comment = '';
                    }

                    if (requestUserIsStaff === true || requestUserEmployeeRole === 'Управляющий' && requestUserEmployeeTpID === tradepointID) {
                         if (item.contractor === contrID && item.is_deleted === false) {
                            tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>${item.name}</td>
                            <td>${item.number}</td><td>${item.comment}</td><td class="d-flex justify-content-end">
                            <button type="button" class="btn btn-danger buttonDelete" data-bs-toggle="modal"
                            data-own_name=${item.name} data-own_auto_number=${item.number}
                            data-own_id=${item.id} data-contr_id=${contrID}
                            data-org_id=${orgID} data-bs-target="#own_modal">Удалить</button>
                            <a class="btn btn-secondary" style="margin-left: 15px"
                            href="${locationHost}/org/${orgID}/tp/${tpID}/order/create/stage/1/?contractor=${contrID}&own=${item.id}">Заказ-наряд</a></td></tr>`
                        }
                    }
                    else {
                        if (item.contractor === contrID && item.is_deleted === false) {
                            tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>${item.name}</td>
                            <td>${item.number}</td><td>${item.comment}</td>`
                        }
                    }
                })
                Array.from(buttonColection).forEach(function(element) {
                    element.addEventListener('click', (e) => {
                        var ownId = element.dataset['own_id'];
                        var ownName = element.dataset['own_name'];
                        var ownAutoNumber = element.dataset['own_auto_number'];
                        ownIdInput.value = ownId;
                        ownIdInput.dataset['orgId'] = element.dataset['org_id'];
                        ownIdInput.dataset['contrId'] = element.dataset['contr_id'];

                        modalString.innerHTML = `<p>Автомобиль: ${ownName} <br>Госномер:  ${ownAutoNumber} <br><br>Будет удален из списка навсегда. Вы уверены?</p>`
                    })
                })
            }
            if (!tableBody.hasChildNodes()) {
                tableHead.innerHTML = '';
                emptyBody.innerHTML = '<p class="text-danger" style="text-align:center; margin-top: 15px">В списке данного контрагента пока отсутствуют собственности. Создайте нажав кнопку "Добавить собственность"</p>';
            }
        },
        error: (response) => {
            console.log(response);
        }
    })
})


isPart.addEventListener('click', () => {
    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/contractor/${contrID}/own/list/filter/?is_part=true`,
        method: 'GET',
        success: (data) => {
            var ownIdInput = document.getElementById('own_id');
            isPart.checked = true;
            isNotPart.checked = false;
            tableHead.innerHTML = '';
            tableBody.innerHTML = '';
            emptyBody.innerHTML = '';
            tableHead.innerHTML += '<tr><th class="col-2">Наименование</th><th class="col-2"></th><th class="col-6">Комментарий</th><th class="col-2"></th></tr>'
            if (data.results.length) {
                data.results.forEach(function (item) {
                    if (item.comment == null) {
                        item.comment = '';
                    }
                    if (item.number == null) {
                        item.number = '';
                    }
                    if (requestUserIsStaff === true || requestUserEmployeeRole === 'Управляющий' && requestUserEmployeeTpID === tradepointID) {
                        if (item.contractor === contrID && item.is_deleted === false && item.is_part) {
                            tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>${item.name}</td>
                            <td>${item.number}</td><td>${item.comment}</td><td class="d-flex justify-content-end">
                            <button type="button" class="btn btn-danger buttonDelete" data-bs-toggle="modal"
                            data-own_name=${item.name}
                            data-own_id=${item.id} data-contr_id=${contrID}
                            data-org_id=${orgID} data-bs-target="#own_modal">Удалить</button>
                            <a class="btn btn-secondary" style="margin-left: 15px"
                            href="${locationHost}/org/${orgID}/tp/${tpID}/order/create/stage/1/?contractor=${contrID}&own=${item.id}">Заказ-наряд</a></td></tr>`
                        }
                    }
                    else {
                        if (item.contractor === contrID && item.is_deleted === false && item.is_part) {
                            tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>${item.name}</td>
                            <td>${item.number}</td><td>${item.comment}</td>`
                        }
                    }
                })
                Array.from(buttonColection).forEach(function(element) {
                    element.addEventListener('click', (e) => {
                        var ownId = element.dataset['own_id'];
                        var ownName = element.dataset['own_name'];
                        ownIdInput.value = ownId;

                        ownIdInput.dataset['orgId'] = element.dataset['org_id'];
                        ownIdInput.dataset['contrId'] = element.dataset['contr_id'];

                        modalString.innerHTML = `<p>Запчасть: ${ownName}<br>Будет удалена из списка навсегда. Вы уверены?</p>`
                    })
                })
            }
            if (!tableBody.hasChildNodes()) {
                tableHead.innerHTML = '';
                emptyBody.innerHTML = '<p class="text-danger" style="text-align:center; margin-top: 15px">В списке данного контрагента пока отсутствуют запчасти. Создайте нажав кнопку "Добавить собственность"</p>';
            }
        },
        error: (response) => {
            console.log(response);
        }
    })
})

isNotPart.addEventListener('click', () => {
     $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/contractor/${contrID}/own/list/filter/?is_part=false`,
        method: 'GET',
        success: (data) => {
            var ownIdInput = document.getElementById('own_id');
            isNotPart.checked = true;
            isPart.checked = false;
            tableHead.innerHTML = '';
            tableBody.innerHTML = '';
            emptyBody.innerHTML = '';
            tableHead.innerHTML += '<tr><th class="col-2">Наименование</th><th class="col-2">Номер</th><th class="col-6">Комментарий</th><th class="col-2"></th></tr>'
            if (data.results.length) {
                data.results.forEach(function (item) {
                    if (item.comment == null) {
                        item.comment = '';
                    }
                    if (requestUserIsStaff === true || requestUserEmployeeRole === 'Управляющий' && requestUserEmployeeTpID === tradepointID) {
                        if (item.contractor === contrID && item.is_deleted === false) {
                            tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>${item.name}</td>
                            <td>${item.number}</td><td>${item.comment}</td><td class="d-flex justify-content-end">
                            <button type="button" class="btn btn-danger buttonDelete" data-bs-toggle="modal"
                            data-own_name=${item.name} data-own_auto_number=${item.number}
                            data-own_id=${item.id} data-contr_id=${contrID}
                            data-org_id=${orgID} data-bs-target="#own_modal">Удалить</button>
                            <a class="btn btn-secondary" style="margin-left: 15px"
                            href="${locationHost}/org/${orgID}/tp/${tpID}/order/create/stage/1/?contractor=${contrID}&own=${item.id}">Заказ-наряд</a></td></tr>`
                        }
                    }
                    else {
                        if (item.contractor === contrID && item.is_deleted === false) {
                            tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>${item.name}</td>
                            <td>${item.number}</td><td>${item.comment}</td>`
                        }
                    }
                })
                Array.from(buttonColection).forEach(function(element) {
                    element.addEventListener('click', (e) => {
                        var ownId = element.dataset['own_id'];
                        var ownName = element.dataset['own_name'];
                        var ownAutoNumber = element.dataset['own_auto_number'];
                        ownIdInput.value = ownId;
                        ownIdInput.dataset['orgId'] = element.dataset['org_id'];
                        ownIdInput.dataset['contrId'] = element.dataset['contr_id'];

                        modalString.innerHTML = `<p>Автомобиль: ${ownName} <br>Госномер:  ${ownAutoNumber} <br><br>Будет удален из списка навсегда. Вы уверены?</p>`
                    })
                })
            }
            if (!tableBody.hasChildNodes()) {
                tableHead.innerHTML = '';
                emptyBody.innerHTML = '<p class="text-danger" style="text-align:center; margin-top: 15px">В списке данного контрагента пока отсутствуют автомобили. Создайте нажав кнопку "Добавить собственность"</p>';
            }
        },
        error: (response) => {
            console.log(response);
        }
    })
})
