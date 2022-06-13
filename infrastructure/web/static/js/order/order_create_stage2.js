let service = document.getElementById('service');
let serviceName = document.getElementById('service_name');
let servicePrice = document.getElementById('service_name');

let employee = document.getElementById('employee');

let tableBody = document.getElementById('selectedServicesTable');
let nothingSelected = document.getElementById('nothingSelected');

let serviceEmployeeForm = document.getElementById('serviceEmployeeForm');

let employees = eval(document.getElementById('employees').innerText.trim());
let sessionJobs = eval(document.getElementById('session_jobs').innerText.trim());

let serviceOptions = document.getElementsByClassName('service-option');


if (typeof sessionJobs === 'object' && sessionJobs.length != 0) {
    tableBody.innerHTML = '';
    nothingSelected.classList.add('d-none');

    for (let i = 0; i < sessionJobs.length; i++) {
        for (let j = 0; j < serviceOptions.length; j++) {
            if (serviceOptions[j] == serviceOptions[sessionJobs[i]['Индекс']]) {
                serviceOptions[j].selected = true;
                serviceOptions[j].dataset['serviceEmployees'] = sessionJobs[i]['Мастера'];
                serviceOptions[j].dataset['serviceGaranty'] = sessionJobs[i]['Гарантия'];
            }
        }

        tableBody.innerHTML += `<tr class="service-row" data-service-index="${sessionJobs[i]['Индекс']}" data-service-name="${sessionJobs[i]['Название услуги']}" data-service-employees="${sessionJobs[i]['Мастера']}" data-service-garanty="${sessionJobs[i]['Гарантия']}" data-service-price="${sessionJobs[i]['Цена услуги']}">
                                    <td>${sessionJobs[i]['Название услуги']}</td>
                                    <td>
                                        <select class="form-control selectpicker employee-select" multiple data-live-search="true" title="Выберите мастеров" data-max-options="5" data-selected-text-format="count" required></select>
                                    </td>
                                    <td>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input garanty" type="checkbox" role="switch">
                                        </div>
                                    </td>
                                    <th>${sessionJobs[i]['Цена услуги']}</th>
                                </tr>`;
    }

    let employeeSelects = document.querySelectorAll('select.employee-select')
    let garantyBtns = document.getElementsByClassName('garanty');

    for (let i = 0; i < sessionJobs.length; i++) {
        employees.forEach(emp => {
            if (sessionJobs[i]['Мастера'].indexOf(eval(emp.IIN)) != -1) {
                employeeSelects[i].innerHTML += `<option value="${emp.IIN}" selected data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
            }
            else {
                employeeSelects[i].innerHTML += `<option value="${emp.IIN}" data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
            }
        })

        if (sessionJobs[i]['Гарантия']) {
            garantyBtns[i].checked = true;
        }
        else {
            garantyBtns[i].checked = false;
        }
    }

    $('.selectpicker').selectpicker('render');
}


service.addEventListener('change', e => {
    if (service.selectedOptions.length != 0) {
        tableBody.innerHTML = '';
        nothingSelected.classList.add('d-none');

        for (let i = 0; i < service.selectedOptions.length; i++) {
            for (let j = 0; j < serviceOptions.length; j++) {
                if (serviceOptions[j] == service.selectedOptions[i]) {
                    tableBody.innerHTML += `<tr class="service-row" data-service-index="${j}" data-service-name="${service.selectedOptions[i].dataset['serviceName']}" data-service-employees="${serviceOptions[j].dataset['serviceEmployees']}" data-service-garanty="${serviceOptions[j].dataset['serviceGaranty']}" data-service-price="${service.selectedOptions[i].dataset['servicePrice']}">
                                                <td>${service.selectedOptions[i].dataset['serviceName']}</td>
                                                <td>
                                                    <select class="form-control selectpicker employee-select" multiple data-live-search="true" title="Выберите мастеров" data-max-options="5" data-selected-text-format="count" required></select>
                                                </td>
                                                <td>
                                                    <div class="form-check form-switch">
                                                        <input class="form-check-input garanty" type="checkbox" role="switch">
                                                    </div>
                                                </td>
                                                <th>${service.selectedOptions[i].dataset['servicePrice']}</th>
                                            </tr>`;
                }
            }
        }

        let employeeSelects = document.querySelectorAll('select.employee-select')

        for (empSelect of employeeSelects) {
            employees.forEach(emp => {
                if (empSelect.parentElement.parentElement.dataset['serviceEmployees'] != '[]') {
                    let employeesIIN = empSelect.parentElement.parentElement.dataset['serviceEmployees'].split(',');

                    if (employeesIIN.indexOf(emp.IIN) != -1) {
                        empSelect.innerHTML += `<option value="${emp.IIN}" selected data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
                    }
                    else {
                        empSelect.innerHTML += `<option value="${emp.IIN}" data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
                    }
                }
                else {
                    empSelect.innerHTML += `<option value="${emp.IIN}" data-subtext="${emp.IIN}">${emp.name} ${emp.surname}</option>`
                }
            })
        }

        $('.selectpicker').selectpicker('render');

        Object.values(employeeSelects).forEach(empSelect => {
            empSelect.addEventListener('change', e => {
                let selectedValues = [];

                for (let i = 0; i < empSelect.selectedOptions.length; i++) {
                    selectedValues.push(empSelect.selectedOptions[i].value)
                }

                empSelect.parentElement.parentElement.parentElement.dataset['serviceEmployees'] = selectedValues;
                serviceOptions[eval(empSelect.parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceEmployees'] = selectedValues;
            })
        })

        let garantyBtns = document.getElementsByClassName('garanty');

        for (let i = 0; i < garantyBtns.length; i++) {
            if (garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] === 'false') {
                garantyBtns[i].checked = false
            }
            else {
                garantyBtns[i].checked = true
            }

            garantyBtns[i].addEventListener('change', e => {
                if (garantyBtns[i].checked) {
                    garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'true';
                    serviceOptions[eval(garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'true';
                }
                else {
                    garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'false';
                    serviceOptions[eval(garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'false';
                }
            })
        }
    }
    else {
        tableBody.innerHTML = '';
        nothingSelected.classList.remove('d-none');
    }
})

serviceEmployeeForm.addEventListener('submit', e => {
    e.preventDefault();

    let resultServices = document.getElementById('resultServices');
    let serviceRows = document.getElementsByClassName('service-row');

    let result = [];

    for (let i = 0; i < serviceRows.length; i++) {
        const element = serviceRows[i];

        result.push({
            'Индекс': eval(element.dataset['serviceIndex']),
            'Название услуги': element.dataset['serviceName'],
            'Цена услуги': eval(element.dataset['servicePrice']),
            'Гарантия': eval(element.dataset['serviceGaranty']),
            'Мастера': element.dataset['serviceEmployees'].split(',').map(element => {return eval(element)})
        });
    }

    resultServices.value = JSON.stringify(result);

    serviceEmployeeForm.submit();
})


if (errors != "") {
    alert('Вы не заполнили услуги или мастеров для услуг! Попробуйте еще раз.')
}
