let contractor = document.getElementById('contractor');
let own = document.getElementById('own');
let contractorLinks = document.getElementById('contractor-links');
let ownLinks = document.getElementById('own-links');
let contractorInfo = document.getElementById('contractorInfo');
let ownInfo = document.getElementById('ownInfo');
let contractorDetailLink = document.getElementById('contractor-detail-link');


if (own.value != '' && contractor.value != '') {
    if (contractorDetailLink != null) {
        contractorDetailLink.remove();
    }

    contractorLinks.innerHTML += `<a href="${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}" class="link-primary" id="contractor-detail-link">Подробнее о контрагенте</a>`;
    ownLinks.innerHTML = `<a href="${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}/own/create?next=order_create_stage1" class="link-primary">Создать собственность</a>`


    if (contractor.selectedOptions[0].dataset['address'] === '') {
        contractorInfo.innerHTML = `<div class="d-flex">
                                        <div class="me-5" style="width: 250px;">
                                            <div><strong>Наименование:</strong></div>
                                            <div><strong>ИИН/БИН:</strong></div>
                                            <div><strong>Телефон:</strong></div>
                                            <div><strong>Адрес:</strong></div>
                                        </div>
                                        <div>
                                            <div>${contractor.selectedOptions[0].innerText}</div>
                                            <div>${contractor.selectedOptions[0].dataset['subtext']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['phone']}</div>
                                            <div>Не указан</div>
                                        </div>
                                    </div>`
    }
    else {
        contractorInfo.innerHTML = `<div class="d-flex">
                                        <div class="me-5" style="width: 250px;">
                                            <div><strong>Наименование:</strong></div>
                                            <div><strong>ИИН/БИН:</strong></div>
                                            <div><strong>Телефон:</strong></div>
                                            <div><strong>Адрес:</strong></div>
                                        </div>
                                        <div>
                                            <div>${contractor.selectedOptions[0].innerText}</div>
                                            <div>${contractor.selectedOptions[0].dataset['subtext']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['phone']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['address']}</div>
                                        </div>
                                    </div>`
    }


    if (own.selectedOptions[0].dataset['isPart'] === 'false') {
        if (own.selectedOptions[0].dataset['comment'] != 'null') {
            ownInfo.innerHTML = `<div class="d-flex">
                                <div class="me-5" style="width: 250px;">
                                    <div><strong>Наименование:</strong></div>
                                    <div><strong>Номер:</strong></div>
                                    <div><strong>Доп. информация:</strong></div>
                                </div>
                                <div>
                                    <div>${own.selectedOptions[0].innerText}</div>
                                    <div>${own.selectedOptions[0].dataset['number']}</div>
                                    <div>${own.selectedOptions[0].dataset['comment']}</div>
                                </div>
                            </div>`
        }
        else {
            ownInfo.innerHTML = `<div class="d-flex">
                                <div class="me-5" style="width: 250px;">
                                    <div><strong>Наименование:</strong></div>
                                    <div><strong>Номер:</strong></div>
                                    <div><strong>Доп. информация:</strong></div>
                                </div>
                                <div>
                                    <div>${own.selectedOptions[0].innerText}</div>
                                    <div>${own.selectedOptions[0].dataset['number']}</div>
                                    <div>Не указано</div>
                                </div>
                            </div>`
        }
    }
    else {
        if (own.selectedOptions[0].dataset['comment'] != 'null') {
            ownInfo.innerHTML = `<div class="d-flex">
                                <div class="me-5" style="width: 250px;">
                                    <div><strong>Наименование:</strong></div>
                                    <div><strong>Доп. информация:</strong></div>
                                </div>
                                <div>
                                    <div>${own.selectedOptions[0].innerText}</div>
                                    <div>${own.selectedOptions[0].dataset['comment']}</div>
                                </div>
                            </div>`
        }
        else {
            ownInfo.innerHTML = `<div class="d-flex">
                                <div class="me-5" style="width: 250px;">
                                    <div><strong>Наименование:</strong></div>
                                    <div><strong>Доп. информация:</strong></div>
                                </div>
                                <div>
                                    <div>${own.selectedOptions[0].innerText}</div>
                                    <div>Не указано</div>
                                </div>
                            </div>`
        }
    }
}


if (contractor.value != '' && own.value === '') {
    if (contractorDetailLink != null) {
        contractorDetailLink.remove();
    }

    contractorLinks.innerHTML += `<a href="${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}" class="link-primary" id="contractor-detail-link">Подробнее о контрагенте</a>`;

    if (contractor.selectedOptions[0].dataset['address'] === '') {
        contractorInfo.innerHTML = `<div class="d-flex">
                                        <div class="me-2" style="width: 250px;">
                                            <div><strong>Наименование:</strong></div>
                                            <div><strong>ИИН/БИН:</strong></div>
                                            <div><strong>Телефон:</strong></div>
                                            <div><strong>Адрес:</strong></div>
                                        </div>
                                        <div>
                                            <div>${contractor.selectedOptions[0].innerText}</div>
                                            <div>${contractor.selectedOptions[0].dataset['subtext']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['phone']}</div>
                                            <div>Не указан</div>
                                        </div>
                                    </div>`
    }
    else {
        contractorInfo.innerHTML = `<div class="d-flex">
                                        <div class="me-2" style="width: 250px;">
                                            <div><strong>Наименование:</strong></div>
                                            <div><strong>ИИН/БИН:</strong></div>
                                            <div><strong>Телефон:</strong></div>
                                            <div><strong>Адрес:</strong></div>
                                        </div>
                                        <div>
                                            <div>${contractor.selectedOptions[0].innerText}</div>
                                            <div>${contractor.selectedOptions[0].dataset['subtext']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['phone']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['address']}</div>
                                        </div>
                                    </div>`
    }

    own.innerHTML = ''

    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}/own/?contrID=${contractor.value}`,
        method: 'get',
        success: (data) => {
            if (data.length != 0) {
                if (own.attributes.getNamedItem('disabled')) {
                    own.attributes.removeNamedItem('disabled')

                    ownLinks.innerHTML = `<a href="${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}/own/create/" class="link-primary">Создать собственность</a>`
                }
                data.forEach(element => {
                    own.innerHTML += `<option value="${element.id}" data-number="${element.number}" data-is-part="${element.is_part}" data-comment="${element.comment}">${element.name}</option>`
                });

                if (own.selectedOptions[0].dataset['isPart'] === 'false') {
                    if (own.selectedOptions[0].dataset['comment'] != 'null') {
                        ownInfo.innerHTML = `<div class="d-flex">
                                            <div class="me-5" style="width: 250px;">
                                                <div><strong>Наименование:</strong></div>
                                                <div><strong>Номер:</strong></div>
                                                <div><strong>Доп. информация:</strong></div>
                                            </div>
                                            <div>
                                                <div>${own.selectedOptions[0].innerText}</div>
                                                <div>${own.selectedOptions[0].dataset['number']}</div>
                                                <div>${own.selectedOptions[0].dataset['comment']}</div>
                                            </div>
                                        </div>`
                    }
                    else {
                        ownInfo.innerHTML = `<div class="d-flex">
                                            <div class="me-5" style="width: 250px;">
                                                <div><strong>Наименование:</strong></div>
                                                <div><strong>Номер:</strong></div>
                                                <div><strong>Доп. информация:</strong></div>
                                            </div>
                                            <div>
                                                <div>${own.selectedOptions[0].innerText}</div>
                                                <div>${own.selectedOptions[0].dataset['number']}</div>
                                                <div>Не указано</div>
                                            </div>
                                        </div>`
                    }
                }
                else {
                    if (own.selectedOptions[0].dataset['comment'] != 'null') {
                        ownInfo.innerHTML = `<div class="d-flex">
                                            <div class="me-5" style="width: 250px;">
                                                <div><strong>Наименование:</strong></div>
                                                <div><strong>Доп. информация:</strong></div>
                                            </div>
                                            <div>
                                                <div>${own.selectedOptions[0].innerText}</div>
                                                <div>${own.selectedOptions[0].dataset['comment']}</div>
                                            </div>
                                        </div>`
                    }
                    else {
                        ownInfo.innerHTML = `<div class="d-flex">
                                            <div class="me-5" style="width: 250px;">
                                                <div><strong>Наименование:</strong></div>
                                                <div><strong>Доп. информация:</strong></div>
                                            </div>
                                            <div>
                                                <div>${own.selectedOptions[0].innerText}</div>
                                                <div>Не указано</div>
                                            </div>
                                        </div>`
                    }
                }
            }
            else {
                own.innerHTML = '<option>У контрагента нет собственностей</option>'

                ownLinks.innerHTML = `<a href="${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}/own/create?next=order_create_stage1" class="link-primary">Создать собственность</a>`
            }
        },
        error: (response) => {
            if (!(own.attributes.getNamedItem('disabled'))) {
                own.disabled = true;
                own.innerHTML = '<option>-</option>'
            }
        }
    })
}


contractor.addEventListener('change', (e) => {
    if (contractorDetailLink != null) {
        contractorDetailLink.remove();
    }

    contractorLinks.innerHTML += `<a href="${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}" class="link-primary" id="contractor-detail-link">Подробнее о контрагенте</a>`;

    if (contractor.selectedOptions[0].dataset['address'] === '') {
        contractorInfo.innerHTML = `<div class="d-flex">
                                        <div class="me-5" style="width: 250px;">
                                            <div><strong>Наименование:</strong></div>
                                            <div><strong>ИИН/БИН:</strong></div>
                                            <div><strong>Телефон:</strong></div>
                                            <div><strong>Адрес:</strong></div>
                                        </div>
                                        <div>
                                            <div>${contractor.selectedOptions[0].innerText}</div>
                                            <div>${contractor.selectedOptions[0].dataset['subtext']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['phone']}</div>
                                            <div>Не указан</div>
                                        </div>
                                    </div>`
    }
    else {
        contractorInfo.innerHTML = `<div class="d-flex">
                                        <div class="me-5" style="width: 250px;">
                                            <div><strong>Наименование:</strong></div>
                                            <div><strong>ИИН/БИН:</strong></div>
                                            <div><strong>Телефон:</strong></div>
                                            <div><strong>Адрес:</strong></div>
                                        </div>
                                        <div>
                                            <div>${contractor.selectedOptions[0].innerText}</div>
                                            <div>${contractor.selectedOptions[0].dataset['subtext']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['phone']}</div>
                                            <div>${contractor.selectedOptions[0].dataset['address']}</div>
                                        </div>
                                    </div>`
    }

    own.innerHTML = ''

    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}/own/?contrID=${contractor.value}`,
        method: 'get',
        success: (data) => {
            if (data.length != 0) {
                if (own.attributes.getNamedItem('disabled')) {
                    own.attributes.removeNamedItem('disabled')

                    ownLinks.innerHTML = `<a href="${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}/own/create/" class="link-primary">Создать собственность</a>`
                }
                data.forEach(element => {
                    own.innerHTML += `<option value="${element.id}" data-number="${element.number}" data-is-part="${element.is_part}" data-comment="${element.comment}">${element.name}</option>`
                });

                if (own.selectedOptions[0].dataset['isPart'] === 'false') {
                    if (own.selectedOptions[0].dataset['comment'] != 'null') {
                        ownInfo.innerHTML = `<div class="d-flex">
                                            <div class="me-5" style="width: 250px;">
                                                <div><strong>Наименование:</strong></div>
                                                <div><strong>Номер:</strong></div>
                                                <div><strong>Доп. информация:</strong></div>
                                            </div>
                                            <div>
                                                <div>${own.selectedOptions[0].innerText}</div>
                                                <div>${own.selectedOptions[0].dataset['number']}</div>
                                                <div>${own.selectedOptions[0].dataset['comment']}</div>
                                            </div>
                                        </div>`
                    }
                    else {
                        ownInfo.innerHTML = `<div class="d-flex">
                                            <div class="me-5" style="width: 250px;">
                                                <div><strong>Наименование:</strong></div>
                                                <div><strong>Номер:</strong></div>
                                                <div><strong>Доп. информация:</strong></div>
                                            </div>
                                            <div>
                                                <div>${own.selectedOptions[0].innerText}</div>
                                                <div>${own.selectedOptions[0].dataset['number']}</div>
                                                <div>Не указано</div>
                                            </div>
                                        </div>`
                    }
                }
                else {
                    if (own.selectedOptions[0].dataset['comment'] != 'null') {
                        ownInfo.innerHTML = `<div class="d-flex">
                                            <div class="me-5" style="width: 250px;">
                                                <div><strong>Наименование:</strong></div>
                                                <div><strong>Доп. информация:</strong></div>
                                            </div>
                                            <div>
                                                <div>${own.selectedOptions[0].innerText}</div>
                                                <div>${own.selectedOptions[0].dataset['comment']}</div>
                                            </div>
                                        </div>`
                    }
                    else {
                        ownInfo.innerHTML = `<div class="d-flex">
                                            <div class="me-5" style="width: 250px;">
                                                <div><strong>Наименование:</strong></div>
                                                <div><strong>Доп. информация:</strong></div>
                                            </div>
                                            <div>
                                                <div>${own.selectedOptions[0].innerText}</div>
                                                <div>Не указано</div>
                                            </div>
                                        </div>`
                    }
                }
            }
            else {
                own.innerHTML = '<option>У контрагента нет собственностей</option>'

                ownLinks.innerHTML = `<a href="${locationHost}/org/1/tp/${tpID}/contractor/${contractor.value}/own/create?next=order_create_stage1" class="link-primary">Создать собственность</a>`
            }
        },
        error: (response) => {
            if (!(own.attributes.getNamedItem('disabled'))) {
                own.disabled = true;
                own.innerHTML = '<option>-</option>'
            }
        }
    })
})


own.addEventListener('change', e => {
    if (own.selectedOptions[0].dataset['isPart'] === 'false') {
        if (own.selectedOptions[0].dataset['comment'] != 'null') {
            ownInfo.innerHTML = `<div class="d-flex">
                                <div class="me-5" style="width: 250px;">
                                    <div><strong>Наименование:</strong></div>
                                    <div><strong>Номер:</strong></div>
                                    <div><strong>Доп. информация:</strong></div>
                                </div>
                                <div>
                                    <div>${own.selectedOptions[0].innerText}</div>
                                    <div>${own.selectedOptions[0].dataset['number']}</div>
                                    <div>${own.selectedOptions[0].dataset['comment']}</div>
                                </div>
                            </div>`
        }
        else {
            ownInfo.innerHTML = `<div class="d-flex">
                                <div class="me-5" style="width: 250px;">
                                    <div><strong>Наименование:</strong></div>
                                    <div><strong>Номер:</strong></div>
                                    <div><strong>Доп. информация:</strong></div>
                                </div>
                                <div>
                                    <div>${own.selectedOptions[0].innerText}</div>
                                    <div>${own.selectedOptions[0].dataset['number']}</div>
                                    <div>Не указано</div>
                                </div>
                            </div>`
        }
    }
    else {
        if (own.selectedOptions[0].dataset['comment'] != 'null') {
            ownInfo.innerHTML = `<div class="d-flex">
                                <div class="me-5" style="width: 250px;">
                                    <div><strong>Наименование:</strong></div>
                                    <div><strong>Доп. информация:</strong></div>
                                </div>
                                <div>
                                    <div>${own.selectedOptions[0].innerText}</div>
                                    <div>${own.selectedOptions[0].dataset['comment']}</div>
                                </div>
                            </div>`
        }
        else {
            ownInfo.innerHTML = `<div class="d-flex">
                                <div class="me-5" style="width: 250px;">
                                    <div><strong>Наименование:</strong></div>
                                    <div><strong>Доп. информация:</strong></div>
                                </div>
                                <div>
                                    <div>${own.selectedOptions[0].innerText}</div>
                                    <div>Не указано</div>
                                </div>
                            </div>`
        }
    }
})
