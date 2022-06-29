let tableBody = document.getElementById('tableBody');
let tableHead = document.getElementById('tableHead');
let emptyBody = document.getElementById('emptyBody');
let isPart = document.getElementById('isPart');
let isNotPart = document.getElementById('isNotPart');
let numberTitle = document.getElementById('numberTitle');
let btnDelete = document.getElementById('btnDelete');


window.addEventListener('load', () => {
    $.ajax({
        url: `http://127.0.0.1:8000/org/1/tp/${tpID}/contractor/${contrID}/own/list/filter/?is_part=false`,
        method: 'GET',
        success: (data) => {
            console.log(data);
            console.log('onload');
            isNotPart.checked = true;
            isPart.checked = false;
            tableHead.innerHTML += '<tr><td>' + 'Наименование' + '</td><td>' + 'Номер' + '</td><td>' + 'Комментарий' + '</td></tr>'
            tableBody.innerHTML = '';
            if (data.results.length) {
                data.results.forEach(function (item) {
                    if (item.comment == null) {
                        item.comment = '';
                    }
                    if (item.number == null) {
                        item.number = '';
                    }
                    if (item.contractor === contrID && item.is_deleted === false) {
                        tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>` + item.name + '</td><td>' + item.number + '</td><td>' + item.comment + `</td><td class="d-flex justify-content-end"><a class="btn btn-danger buttonDelete" data-bs-toggle="modal" data-own_name='${item.name}' data-own_auto_number="${item.number}" data-own_id="${item.id}" data-contr_id="${contrID}" data-org_id="${orgID}" data-bs-target="#own_modal">Удалить</a><a class="btn btn-secondary" style="margin-left: 15px" href="${locationHost}/org/${orgID}/tp/${tpID}/order/create/stage/1/?contractor=${contrID}&own=${item.id}">Заказ-наряд</a></td></tr>`
                    }
                })
            } else {
                tableHead.innerHTML = '';
                tableBody.innerHTML = '';
                emptyBody.innerHTML = '';
                emptyBody.innerHTML += '<p class="text-danger" style="text-align: center; margin-top: 15px">У данного контрагента пока отсутствуют собственности. Создайте нажав кнопку "Добавить собственность"</p>';
            }
        },
        error: (response) => {
            console.log(response);
        }
    })
})


isPart.addEventListener('click', () => {
    $.ajax({
        url: `http://127.0.0.1:8000/org/1/tp/${tpID}/contractor/${contrID}/own/list/filter/?is_part=true`,
        method: 'GET',
        success: (data) => {
            console.log('isPart clicked');
            isPart.checked = true;
            isNotPart.checked = false;
            tableHead.innerHTML = '';
            tableBody.innerHTML = '';
            tableHead.innerHTML += '<tr><td>' + 'Наименование' + '</td><td>' + 'Комментарий' + '</td></tr>'
            if (data.results.length) {
                data.results.forEach(function (item) {
                    if (item.comment == null) {
                        item.comment = '';
                    }
                    if (item.number == null) {
                        item.number = '';
                    }
                    if (item.contractor === contrID && item.is_deleted === false && item.is_part) {
                        tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>` + item.name + '</td><td>' + item.comment + `</td><td class="d-flex justify-content-end"><a class="btn btn-danger buttonDelete" data-bs-toggle="modal" data-own_name='${item.name}' data-own_auto_number="${item.number}" data-own_id="${item.id}" data-contr_id="${contrID}" data-org_id="${orgID}" data-bs-target="#own_modal">Удалить</a><a class="btn btn-secondary" style="margin-left: 15px" href="${locationHost}/org/${orgID}/tp/${tpID}/order/create/stage/1/?contractor=${contrID}&own=${item.id}">Заказ-наряд</a></td></tr>`
                    }
                })
            } else {
                tableHead.innerHTML = '';
                tableBody.innerHTML = '';
                emptyBody.innerHTML = '';
                emptyBody.innerHTML += '<p class="text-danger" style="text-align: center; margin-top: 15px">У данного контрагента пока отсутствуют собственности. Создайте нажав кнопку "Добавить собственность"</p>';
            }
        },
        error: (response) => {
            console.log(response);
        }
    })



})

isNotPart.addEventListener('click', () => {
     $.ajax({
        url: `http://127.0.0.1:8000/org/1/tp/${tpID}/contractor/${contrID}/own/list/filter/?is_part=false`,
        method: 'GET',
        success: (data) => {
            console.log('isNotPart clicked');
            isNotPart.checked = true;
            isPart.checked = false;
            tableHead.innerHTML = '';
            tableBody.innerHTML = '';
            tableHead.innerHTML += '<tr><td>' + 'Наименование' + '</td><td>' + 'Номер' + '</td><td>' + 'Комментарий' + '</td></tr>'
            if (data.results.length) {
                data.results.forEach(function (item) {
                    if (item.comment == null) {
                        item.comment = '';
                    }
                    if (item.contractor === contrID && item.is_deleted === false && item.is_part === false) {
                        tableBody.innerHTML += `<tr id="own_instance_${item.id}"><td>` + item.name + '</td><td>' + item.number + '</td><td>' + item.comment + `</td><td class="d-flex justify-content-end"><a class="btn btn-danger buttonDelete" data-bs-toggle="modal" data-own_name='${item.name}' data-own_auto_number="${item.number}" data-own_id="${item.id}" data-contr_id="${contrID}" data-org_id="${orgID}" data-bs-target="#own_modal">Удалить</a><a class="btn btn-secondary" style="margin-left: 15px" href="${locationHost}/org/${orgID}/tp/${tpID}/order/create/stage/1/?contractor=${contrID}&own=${item.id}">Заказ-наряд</a></td></tr>`
                    }
                })
            } else {
                tableHead.innerHTML = '';
                tableBody.innerHTML = '';
                emptyBody.innerHTML = '';
                emptyBody.innerHTML += '<p class="text-danger" style="text-align: center; margin-top: 15px">У данного контрагента пока отсутствуют собственности. Создайте нажав кнопку "Добавить собственность"</p>';
            }
        },
        error: (response) => {
            console.log(response);
        }
    })
})
