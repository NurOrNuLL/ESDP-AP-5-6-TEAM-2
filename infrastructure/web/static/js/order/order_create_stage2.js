let service = document.getElementById('service')
let serviceName = document.getElementById('service_name')
let servicePrice = document.getElementById('service_name')

let employee = document.getElementById('employee')

let tableBody = document.getElementById('selectedServicesTable')
let nothingSelected = document.getElementById('nothingSelected')

let serviceEmployeeForm = document.getElementById('serviceEmployeeForm')

let employees = eval(document.getElementById('employees').innerText.trim())


service.addEventListener('change', e => {
    if (service.selectedOptions.length != 0) {
        tableBody.innerHTML = '';
        nothingSelected.classList.add('d-none');

        for (let i = 0; i < service.selectedOptions.length; i++) {
            tableBody.innerHTML += `<tr class="service-row" data-service-name="${service.selectedOptions[i].dataset['serviceName']}" data-service-employees="[]" data-service-garanty="false" data-service-price="${service.selectedOptions[i].dataset['servicePrice']}">
                                        <td>${service.selectedOptions[i].dataset['serviceName']}</td>
                                        <td>
                                            <select class="form-control selectpicker employee-select" multiple data-live-search="true" title="Выберите мастеров" data-max-options="5" data-selected-text-format="count"></select>
                                        </td>
                                        <td>
                                            <div class="form-check form-switch">
                                                <input class="form-check-input garanty" type="checkbox" role="switch">
                                            </div>
                                        </td>
                                        <th>${service.selectedOptions[i].dataset['servicePrice']}</th>
                                    </tr>`;
        }

        let employeeSelects = document.querySelectorAll('select.employee-select')

        for (empSelect of employeeSelects) {
            employees.forEach(emp => {
                empSelect.innerHTML += `<option value="${emp.IIN}" data-subtext="${emp.IIN} ">${emp.name} ${emp.surname}</option>`
            })
        }

        $('.selectpicker').selectpicker('render');

        console.log(employeeSelects);

        Object.values(employeeSelects).forEach(empSelect => {
            empSelect.addEventListener('change', e => {
                let selectedValues = [];

                for (let i = 0; i < empSelect.selectedOptions.length; i++) {
                    selectedValues.push(empSelect.selectedOptions[i].value)
                }

                empSelect.parentElement.parentElement.parentElement.dataset['serviceEmployees'] = selectedValues;
            })
        })

        let garantyBtns = document.getElementsByClassName('garanty');

        for (let i = 0; i < garantyBtns.length; i++) {
            garantyBtns[i].addEventListener('change', e => {
                if (garantyBtns[i].checked) {
                    garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'true';
                }
                else {
                    garantyBtns[i].parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'false';
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
            'Название услуги': element.dataset['serviceName'],
            'Цена услуги': eval(element.dataset['servicePrice']),
            'Гарантия': eval(element.dataset['serviceGaranty']),
            'Мастера': element.dataset['serviceEmployees'].split(',').map(element => {return eval(element)})
        });
    }

    resultServices.value = JSON.stringify(result);

    serviceEmployeeForm.submit();
})
