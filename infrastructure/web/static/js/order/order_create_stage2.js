let service = document.getElementById('service')
let serviceName = document.getElementById('service_name')
let servicePrice = document.getElementById('service_name')

let employee = document.getElementById('employee')

let tableBody = document.getElementById('selectedServicesTable')
let nothingSelected = document.getElementById('nothingSelected')

let serviceEmployeeForm = document.getElementById('serviceEmployeeForm')


service.addEventListener('change', e => {
    if (service.selectedOptions.length != 0) {
        tableBody.innerHTML = '';
        nothingSelected.classList.add('d-none');

        for (let i = 0; i < service.selectedOptions.length; i++) {
            tableBody.innerHTML += `<tr class="service-row" data-service-name="${service.selectedOptions[i].dataset['serviceName']}" data-service-garanty="false" data-service-price="${service.selectedOptions[i].dataset['servicePrice']}">
                                        <td>${service.selectedOptions[i].dataset['serviceName']}</td>
                                        <td>
                                            <div class="form-check form-switch">
                                                <input class="form-check-input garanty" type="checkbox" role="switch">
                                            </div>
                                        </td>
                                        <th>${service.selectedOptions[i].dataset['servicePrice']}</th>
                                    </tr>`;
        }

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
            'Цена услуги': element.dataset['servicePrice'],
            'Гарантия': element.dataset['serviceGaranty'],
        });
    }

    resultServices.value = JSON.stringify(result);

    serviceEmployeeForm.submit();
})
