let service = document.getElementById('service');
let serviceName = document.getElementById('service_name');
let servicePrice = document.getElementById('service_name');

let employee = document.getElementById('employee');

let tableBody = document.getElementById('selectedServicesTable');
let nothingSelected = document.getElementById('nothingSelected');

let serviceEmployeeForm = document.getElementById('serviceEmployeeForm');

let employees = eval(document.getElementById('employees').innerText.trim());
let initialJobs = eval(document.getElementById('initialJobs').innerText.trim());

let serviceOptions = document.getElementsByClassName('service-option');

let serviceList = document.getElementById('service-list');
let employeeList = document.getElementById('employee-list');


if (typeof initialJobs === 'object' && initialJobs.length != 0) {
    tableBody.innerHTML = '';
    nothingSelected.classList.add('d-none');

    for (let i = 0; i < initialJobs.length; i++) {
        let employeesIIN = [];

        for (employee of initialJobs[i]['Мастера']) {
            employeesIIN.push(employee['ИИН']);
        }

        for (let j = 0; j < serviceOptions.length; j++) {
            if (serviceOptions[j] == serviceOptions[initialJobs[i]['Индекс']]) {
                serviceOptions[j].selected = true;
                serviceOptions[j].dataset['serviceEmployees'] = employeesIIN;
                serviceOptions[j].dataset['serviceGaranty'] = initialJobs[i]['Гарантия'];
            }
        }

        tableBody.innerHTML += `<tr class="service-row" data-service-index="${initialJobs[i]['Индекс']}" data-service-name="${initialJobs[i]['Название услуги']}" data-service-category="${initialJobs[i]['Категория услуги']}" data-service-mark="${initialJobs[i]['Марка услуги']}" data-service-employees="${employeesIIN}" data-service-garanty="${initialJobs[i]['Гарантия']}" data-service-price="${initialJobs[i]['Цена услуги']}">
                                    <td>${initialJobs[i]['Название услуги']}</td>
                                    <td>${service.selectedOptions[i].dataset['tokens']}</td>
                                    <td>${service.selectedOptions[i].dataset['subtext']}</td>
                                    <td>
                                        <select class="form-control selectpicker employee-select" multiple data-live-search="true" title="Выбрать" data-max-options="5" data-selected-text-format="count" required></select>
                                    </td>
                                    <td class="checkedEmployees">
                                        Мастера не выбранны!
                                    </td>
                                    <td>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input garanty" type="checkbox" role="switch">
                                        </div>
                                    </td>
                                    <th><span class="Price">${initialJobs[i]['Цена услуги']}</span><span> ₸</span></th>
                                </tr>`;
    }

    let employeeSelects = document.querySelectorAll('select.employee-select')
    let checkedEmployees = document.getElementsByClassName('checkedEmployees');
    let garantyBtns = document.getElementsByClassName('garanty');
    let price = document.getElementsByClassName('Price');
    let totalPrice = document.getElementById('totalPrice');
    let total = 0;

    for (let j = 0; j < employeeSelects.length; j++) {
        const empSelect = employeeSelects[j];

        empSelect.addEventListener('change', e => {
            let selectedValues = [];
            checkedEmployees[j].innerHTML = ''

            if (empSelect.selectedOptions.length === 0) {
                checkedEmployees[j].innerHTML = 'Мастера не выбранны!'
            }

            for (let i = 0; i < empSelect.selectedOptions.length; i++) {
                selectedValues.push(empSelect.selectedOptions[i].value);
                checkedEmployees[j].innerHTML += `<div>${empSelect.selectedOptions[i].innerText}</div>`
            }


            empSelect.parentElement.parentElement.parentElement.dataset['serviceEmployees'] = selectedValues;
            serviceOptions[eval(empSelect.parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceEmployees'] = selectedValues;
        })
    }

    for (let i = 0; i < price.length; i++) {
        if (!(initialJobs[i]['Гарантия'])) {
            total += eval(price[i].innerText);
        }
    }

    for (let i = 0; i < initialJobs.length; i++) {
        checkedEmployees[i].innerHTML = '';
        let employeesIIN = [];

        for (employee of initialJobs[i]['Мастера']) {
            employeesIIN.push(employee['ИИН']);
        }

        employees.forEach(emp => {
            if (employeesIIN.indexOf(eval(emp.IIN)) != -1) {
                employeeSelects[i].innerHTML += `<option value="${emp.IIN}" selected data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
                checkedEmployees[i].innerHTML += `<div>${emp.name} ${emp.surname}</div>`
            }
            else {
                employeeSelects[i].innerHTML += `<option value="${emp.IIN}" data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
            }
        })

        if (initialJobs[i]['Гарантия']) {
            garantyBtns[i].checked = true;
            price[i].style.cssText = 'text-decoration: line-through;';
        }
        else {
            garantyBtns[i].checked = false;
            price[i].style.cssText = 'text-decoration: none;';
        }

        garantyBtns[i].addEventListener('change', e => {
            if (garantyBtns[i].checked) {
                garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'true';
                serviceOptions[eval(garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'true';
                price[i].style.cssText = 'text-decoration: line-through;';
                total -= eval(price[i].innerHTML);
                totalPrice.innerText = `${total} ₸`;
            }
            else {
                garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'false';
                serviceOptions[eval(garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'false';
                price[i].style.cssText = 'text-decoration: none;';
                total += eval(price[i].innerHTML);
                totalPrice.innerText = `${total} ₸`;
            }
        })
    }

    totalPrice.innerText = `${total} ₸`;

    $('.selectpicker').selectpicker('render');
}


service.addEventListener('change', e => {
    if (service.selectedOptions.length != 0) {
        tableBody.innerHTML = '';
        nothingSelected.classList.add('d-none');

        for (let i = 0; i < service.selectedOptions.length; i++) {
            for (let j = 0; j < serviceOptions.length; j++) {
                if (serviceOptions[j] == service.selectedOptions[i]) {
                    tableBody.innerHTML += `<tr class="service-row" data-service-index="${j}" data-service-name="${service.selectedOptions[i].dataset['serviceName']}" data-service-category="${service.selectedOptions[i].dataset['tokens']}" data-service-mark="${service.selectedOptions[i].dataset['subtext']}" data-service-employees="${serviceOptions[j].dataset['serviceEmployees']}" data-service-garanty="${serviceOptions[j].dataset['serviceGaranty']}" data-service-price="${service.selectedOptions[i].dataset['servicePrice']}">
                                                <td>${service.selectedOptions[i].dataset['serviceName']}</td>
                                                <td>${service.selectedOptions[i].dataset['tokens']}</td>
                                                <td>${service.selectedOptions[i].dataset['subtext']}</td>
                                                <td>
                                                    <select class="form-control selectpicker employee-select" multiple data-live-search="true" title="Выбрать" data-max-options="5" data-selected-text-format="count" required></select>
                                                </td>
                                                <td class="checkedEmployees">
                                                    Мастера не выбранны!
                                                </td>
                                                <td>
                                                    <div class="form-check form-switch">
                                                        <input class="form-check-input garanty" type="checkbox" role="switch">
                                                    </div>
                                                </td>
                                                <th><span class="Price">${service.selectedOptions[i].dataset['servicePrice']}</span><span> ₸</span></th>
                                            </tr>`;
                }
            }
        }

        let employeeSelects = document.querySelectorAll('select.employee-select')
        let checkedEmployees = document.getElementsByClassName('checkedEmployees');

        for (empSelect of employeeSelects) {
            checkedEmployees[Object.values(employeeSelects).indexOf(empSelect)].innerHTML = '';

            employees.forEach(emp => {
                if (empSelect.parentElement.parentElement.dataset['serviceEmployees'] != '[]') {
                    let employeesIIN = empSelect.parentElement.parentElement.dataset['serviceEmployees'].split(',');


                    if (employeesIIN.indexOf(emp.IIN) != -1) {
                        empSelect.innerHTML += `<option value="${emp.IIN}" selected data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
                        checkedEmployees[Object.values(employeeSelects).indexOf(empSelect)].innerHTML += `<div>${emp.name} ${emp.surname}</div>`
                    }
                    else {
                        empSelect.innerHTML += `<option value="${emp.IIN}" data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
                    }
                }
                else {
                    empSelect.innerHTML += `<option value="${emp.IIN}" data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
                    checkedEmployees[Object.values(employeeSelects).indexOf(empSelect)].innerHTML = 'Мастера не выбранны!';
                }
            })
        }

        $('.selectpicker').selectpicker('render');

        for (let j = 0; j < employeeSelects.length; j++) {
            const empSelect = employeeSelects[j];

            empSelect.addEventListener('change', e => {
                let selectedValues = [];
                checkedEmployees[j].innerHTML = ''

                if (empSelect.selectedOptions.length === 0) {
                    checkedEmployees[j].innerHTML = 'Мастера не выбранны!'
                }

                for (let i = 0; i < empSelect.selectedOptions.length; i++) {
                    selectedValues.push(empSelect.selectedOptions[i].value);
                    checkedEmployees[j].innerHTML += `<div>${empSelect.selectedOptions[i].innerText}</div>`
                }


                empSelect.parentElement.parentElement.parentElement.dataset['serviceEmployees'] = selectedValues;
                serviceOptions[eval(empSelect.parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceEmployees'] = selectedValues;
            })
        }

        let garantyBtns = document.getElementsByClassName('garanty');
        let price = document.getElementsByClassName('Price');
        let totalPrice = document.getElementById('totalPrice');
        let total = 0;

        for (let i = 0; i < price.length; i++) {
            total += eval(price[i].innerText);
        }

        for (let i = 0; i < garantyBtns.length; i++) {
            if (garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] === 'false') {
                garantyBtns[i].checked = false;
                price[i].style.cssText = 'text-decoration: none;';
            }
            else {
                garantyBtns[i].checked = true;
                price[i].style.cssText = 'text-decoration: line-through;';
                total -= eval(price[i].innerHTML);
            }

            garantyBtns[i].addEventListener('change', e => {
                if (garantyBtns[i].checked) {
                    garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'true';
                    serviceOptions[eval(garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'true';
                    price[i].style.cssText = 'text-decoration: line-through;';
                    total -= eval(price[i].innerHTML);
                    totalPrice.innerText = `${total} ₸`;
                }
                else {
                    garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'false';
                    serviceOptions[eval(garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'false';
                    price[i].style.cssText = 'text-decoration: none;';
                    total += eval(price[i].innerHTML);
                    totalPrice.innerText = `${total} ₸`;
                }
            })
        }

        totalPrice.innerText = `${total} ₸`;
    }
    else {
        tableBody.innerHTML = '';
        nothingSelected.classList.remove('d-none');
    }
})

serviceEmployeeForm.addEventListener('submit', e => {
    e.preventDefault();

    let resultServices = document.getElementById('resultServices');
    let fullPrice = document.getElementById('fullPrice');
    let priceForPay = document.getElementById('priceForPay');
    let serviceRows = document.getElementsByClassName('service-row');
    let checkedEmployees = document.getElementsByClassName('checkedEmployees');

    let resultJobs = [];
    let resultPriceForPay = 0;
    let resultFullPrice = 0;

    for (let i = 0; i < serviceRows.length; i++) {
        const serviceRow = serviceRows[i];

        let parsed_employees = [];

        for (let j = 0; j < checkedEmployees[i].children.length; j++) {
            const employeeNameSurname = checkedEmployees[i].children[j].innerText;

            parsed_employees.push({
                'Наименование': employeeNameSurname,
                'ИИН': serviceRow.dataset['serviceEmployees'].split(',').map(element => {return eval(element)})[j]
            })
        }

        resultJobs.push({
            'Индекс': eval(serviceRow.dataset['serviceIndex']),
            'Название услуги': serviceRow.dataset['serviceName'],
            'Категория услуги': serviceRow.dataset['serviceCategory'],
            'Марка услуги': serviceRow.dataset['serviceMark'],
            'Цена услуги': eval(serviceRow.dataset['servicePrice']),
            'Гарантия': eval(serviceRow.dataset['serviceGaranty']),
            'Мастера': parsed_employees
        });

        if (eval(serviceRow.dataset['serviceGaranty']) === true) {
            resultFullPrice += eval(serviceRow.dataset['servicePrice']);
        }
        else {
            resultPriceForPay += eval(serviceRow.dataset['servicePrice']);
            resultFullPrice += eval(serviceRow.dataset['servicePrice']);
        }
    }

    resultServices.value = JSON.stringify(resultJobs);
    fullPrice.value = resultFullPrice;
    priceForPay.value = resultPriceForPay;

    serviceEmployeeForm.submit();
})


if (errors != "") {
    alert('Вы не заполнили услуги или мастеров для услуг! Попробуйте еще раз.')
}
