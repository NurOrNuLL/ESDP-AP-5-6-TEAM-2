let service = document.getElementById('service');
let serviceName = document.getElementById('service_name');
let servicePrice = document.getElementById('service_name');
let employee = document.getElementById('employee');
let tableBody = document.getElementById('selectedServicesTable');
let nothingSelected = document.getElementById('nothingSelected');
let serviceEmployeeForm = document.getElementById('serviceEmployeeForm');
let employees = eval(document.getElementById('employees').innerText.trim());
let sessionJobs = eval(document.getElementById('initialJobs').innerText.trim());
let serviceOptions = document.getElementsByClassName('service-option');
let serviceList = document.getElementById('service-list');
let employeeList = document.getElementById('employee-list');
let fullPrice = document.getElementById('fullPrice');
let priceForPay = document.getElementById('priceForPay');


if (typeof sessionJobs === 'object' && sessionJobs.length != 0) {
    tableBody.innerHTML = '';
    nothingSelected.classList.add('d-none');

    // Основной цикл для отрисовки session_data или form.cleaned_data
    for (let i = 0; i < sessionJobs.length; i++) {
        const initialJob = sessionJobs[i];

        let employeesIINs = [];
        for (employee of initialJob['Мастера']) {
            employeesIINs.push(employee['ИИН']);
        }

        // Индексирование и отслеживание выбранных услуг
        for (serviceOption of serviceOptions) {
            if (serviceOption == serviceOptions[initialJob['Индекс']]) {
                serviceOption.selected = true;
                serviceOption.dataset['serviceEmployees'] = employeesIINs;
                serviceOption.dataset['serviceGaranty'] = initialJob['Гарантия'];
                serviceOption.dataset['serviceCount'] = initialJob['Количество услуг'];
                serviceOption.dataset['total'] = initialJob['Сумма услуг'];
            }
        }

        // Начальная отрисовка строчек таблицы
        tableBody.innerHTML += `<tr class="service-row"
                                    data-service-index="${initialJob['Индекс']}"
                                    data-service-name="${initialJob['Название услуги']}"
                                    data-service-category="${initialJob['Категория услуги']}"
                                    data-service-mark="${initialJob['Марка услуги']}"
                                    data-service-employees="${employeesIINs}"
                                    data-service-count="${initialJob['Количество услуг']}"
                                    data-service-garanty="${initialJob['Гарантия']}"
                                    data-service-price="${initialJob['Цена услуги']}"
                                    data-total="${initialJob['Сумма услуг']}">

                                    <td>
                                        <div class="d-flex justify-content-center align-items-center">
                                            <button type="button" class="btn-close removeService"></button>
                                        </div>
                                    </td>
                                    <td>${initialJob['Название услуги']}</td>
                                    <td>${initialJob['Категория услуги']}</td>
                                    <td>${initialJob['Марка услуги']}</td>
                                    <td>
                                        <select multiple required
                                            class="form-control selectpicker employee-select"
                                            title="Выбрать"
                                            data-live-search="true"
                                            data-max-options="5"
                                            data-selected-text-format="count"></select>
                                    </td>
                                    <td class="checkedEmployees" style="width: 100px">
                                        Мастера не выбраны!
                                    </td>
                                    <td style="width: 100px">
                                        <div class="d-flex align-items-center justify-content-center">
                                            <button type="button" class="btn btn-danger btn-sm minusCount" disabled>
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-lg" viewBox="0 0 16 16">
                                                    <path fill-rule="evenodd" d="M2 8a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11A.5.5 0 0 1 2 8Z"/>
                                                </svg>
                                            </button>
                                            <span class="mx-3 count">${initialJob['Количество услуг']}</span>
                                            <button type="button" class="btn btn-success btn-sm plusCount">
                                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                                                    <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
                                                </svg>
                                            </button>
                                        </div>
                                    </td>
                                    <td>
                                        <div class="form-check form-switch">
                                            <input class="form-check-input garanty" type="checkbox" role="switch">
                                        </div>
                                    </td>
                                    <th><span class="Price">${initialJob['Сумма услуг']}</span></th>
                                </tr>`;
    }

    let serviceRows = document.getElementsByClassName('service-row');
    let employeeSelects = document.querySelectorAll('select.employee-select');
    let checkedEmployees = document.getElementsByClassName('checkedEmployees');
    let garantyBtns = document.getElementsByClassName('garanty');
    let prices = document.getElementsByClassName('Price');
    let minusCounts = document.getElementsByClassName('minusCount');
    let counts = document.getElementsByClassName('count')
    let plusCounts = document.getElementsByClassName('plusCount');
    let totalPrice = document.getElementById('totalPrice');
    let removeServices = document.getElementsByClassName('removeService');
    let total = 0;
    let totalWithoutGaranty = 0;

    for (let i = 0; i < serviceRows.length; i++) {
        const serviceRow = serviceRows[i];
        const sessionJob = sessionJobs[i];
        const employeeSelect = employeeSelects[i];
        const checkedEmployee = checkedEmployees[i];
        const garantyBtn = garantyBtns[i];
        const minusCount = minusCounts[i];
        const count = counts[i];
        const plusCount = plusCounts[i];
        const price = prices[i];
        const removeService = removeServices[i];
        let employeesIINs = [];

        totalWithoutGaranty += eval(price.innerText);

        for (employee of sessionJob['Мастера']) {
            employeesIINs.push(employee['ИИН']);
        }

        if (sessionJob['Мастера'].length != 0) {
            checkedEmployee.innerHTML = '';
        }

        if (eval(sessionJob['Количество услуг']) != 1) {
            minusCount.disabled = false;
        }

        // Отрисовка селектов мастеров
        employees.forEach(employee => {
            if (employeesIINs.indexOf(employee.IIN) != -1) {
                employeeSelect.innerHTML += `<option value="${employee.IIN}" data-emp-name="${employee.name[0]}." data-emp-surname="${employee.surname}" data-subtext="${employee.IIN}" selected>${employee.name} ${employee.surname}</option>`
                checkedEmployee.innerHTML += `<span class="badge rounded-pill text-bg-warning text-truncate" style="max-width: 150px;">${employee.name[0].toUpperCase()}. ${employee.surname}</span>`
            }
            else {
                employeeSelect.innerHTML += `<option value="${employee.IIN}" data-emp-name="${employee.name[0]}." data-emp-surname="${employee.surname}" data-subtext="${employee.IIN}">${employee.name} ${employee.surname}</option>`
            }
        })

        // Событие для выбора мастеров
        employeeSelect.onchange = e => {
            let selectedValues = [];

            checkedEmployee.innerHTML = '';

            if (employeeSelect.selectedOptions.length === 0) {
                checkedEmployee.innerHTML = 'Мастера не выбраны!'
            }

            for (let j = 0; j < employeeSelect.selectedOptions.length; j++) {
                const selectedOption = employeeSelect.selectedOptions[j];

                selectedValues.push(selectedOption.value);
                checkedEmployee.innerHTML += `<span class="badge rounded-pill text-bg-warning text-truncate" style="max-width: 150px;">${selectedOption.dataset['empName'].toUpperCase()} ${selectedOption.dataset['empSurname']}</span>`
            }

            serviceRow.dataset['serviceEmployees'] = selectedValues;
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceEmployees'] = selectedValues;
        };

        // Событие на удаление строчки кнопкой
        removeService.onclick = e => {
            if (eval(serviceRow.dataset['serviceGaranty']) != true) {
                total -= eval(serviceRow.dataset['total']);
            }
            totalWithoutGaranty -= eval(serviceRow.dataset['total']);
            totalPrice.innerText = total;
            priceForPay.value = total;
            fullPrice.value = totalWithoutGaranty;
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].selected = false;
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceGaranty'] = false;
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceEmployees'] = '[]';
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceCount'] = 1;
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['total'] = serviceRow.dataset['servicePrice'];
            serviceRow.remove();

            if (serviceRows.length === 0) {
                nothingSelected.classList.remove('d-none');
            }

            $('.service').selectpicker('destroy');
            $('.service').selectpicker('render');
        };

        // Событие на уменьшение количества услуг
        minusCount.onclick = e => {
            count.innerText = eval(count.innerText) - 1;
            price.innerText = eval(price.innerText) - eval(serviceRow.dataset['servicePrice']);
            serviceRow.dataset['serviceCount'] = count.innerText;
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceCount'] = count.innerText
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['total'] = price.innerText

            if (eval(serviceRow.dataset['serviceGaranty']) === false) {
                serviceRow.dataset['total'] = price.innerText;
                total -= eval(serviceRow.dataset['servicePrice']);
                totalPrice.innerText = total;
                priceForPay.innerText = total;
            }
            totalWithoutGaranty -= eval(serviceRow.dataset['servicePrice']);
            fullPrice.value = totalWithoutGaranty;

            if (eval(count.innerText) === 1) {
                minusCount.disabled = true;
            }
        };

        // Событие на увеличение количества услуг
        plusCount.onclick = e => {
            count.innerText = eval(count.innerText) + 1;
            price.innerText = eval(price.innerText) + eval(serviceRow.dataset['servicePrice']);
            serviceRow.dataset['serviceCount'] = count.innerText;
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceCount'] = count.innerText
            serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['total'] = price.innerText

            if (eval(serviceRow.dataset['serviceGaranty']) === false) {
                serviceRow.dataset['total'] = price.innerText;
                total += eval(serviceRow.dataset['servicePrice']);
                totalPrice.innerText = total;
                priceForPay.value = total;
            }
            totalWithoutGaranty += eval(serviceRow.dataset['servicePrice']);
            fullPrice.value = totalWithoutGaranty;

            minusCount.disabled = false;
        };

        // Отрисовка чекбоксов гарантии
        if (sessionJob['Гарантия']) {
            garantyBtn.checked = true;
            price.style.cssText = 'text-decoration: line-through;';
        }
        else {
            garantyBtn.checked = false;
            price.style.cssText = 'text-decoration: none;';
        }

        // Событие для чекбокса гарантии
        garantyBtn.addEventListener('change', e => {
            if (garantyBtn.checked) {
                serviceRow.dataset['serviceGaranty'] = 'true';
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'true';
                price.style.cssText = 'text-decoration: line-through;';
                total -= eval(price.innerHTML);
                totalPrice.innerText = total;
                priceForPay.value = total;
            }
            else {
                serviceRow.dataset['serviceGaranty'] = 'false';
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'false';
                price.style.cssText = 'text-decoration: none;';
                total += eval(price.innerHTML);
                totalPrice.innerText = total;
                priceForPay.value = total;
            }
        })

        // Добавление цены к общей сумме
        if (!(sessionJobs[i]['Гарантия'])) {
            total += eval(prices[i].innerText);
        }
    }

    totalPrice.innerText = total;
    priceForPay.value = total;
    fullPrice.value = totalWithoutGaranty;

    $('.selectpicker').selectpicker('render');
}


service.addEventListener('change', e => {
    if (service.selectedOptions.length != 0) {
        tableBody.innerHTML = '';
        nothingSelected.classList.add('d-none');

        // Начальная отрисовка строчек таблицы
        for (let i = 0; i < service.selectedOptions.length; i++) {
            const selectedOption = service.selectedOptions[i];

            for (let j = 0; j < serviceOptions.length; j++) {
                const serviceOption = serviceOptions[j];

                if (serviceOption == selectedOption) {
                    tableBody.innerHTML += `<tr class="service-row"
                                                data-service-index="${j}"
                                                data-service-name="${selectedOption.dataset['serviceName']}"
                                                data-service-category="${selectedOption.dataset['tokens']}"
                                                data-service-mark="${selectedOption.dataset['subtext']}"
                                                data-service-employees="${serviceOption.dataset['serviceEmployees']}"
                                                data-service-count="${selectedOption.dataset['serviceCount']}"
                                                data-service-garanty="${serviceOption.dataset['serviceGaranty']}"
                                                data-service-price="${selectedOption.dataset['servicePrice']}"
                                                data-total="${selectedOption.dataset['total']}">

                                                <td>
                                                    <div class="d-flex justify-content-center align-items-center">
                                                        <button type="button" class="btn-close removeService"></button>
                                                    </div>
                                                </td>
                                                <td>${selectedOption.dataset['serviceName']}</td>
                                                <td>${selectedOption.dataset['tokens']}</td>
                                                <td>${selectedOption.dataset['subtext']}</td>
                                                <td>
                                                    <select multiple required
                                                        class="form-control selectpicker employee-select"
                                                        title="Выбрать"
                                                        data-live-search="true"
                                                        data-max-options="5"
                                                        data-selected-text-format="count"></select>
                                                </td>
                                                <td class="checkedEmployees" style="width: 100px">
                                                    Мастера не выбраны!
                                                </td>
                                                <td style="width: 100px">
                                                    <div class="d-flex align-items-center justify-content-center">
                                                        <button type="button" class="btn btn-danger btn-sm minusCount" disabled>
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-dash-lg" viewBox="0 0 16 16">
                                                                <path fill-rule="evenodd" d="M2 8a.5.5 0 0 1 .5-.5h11a.5.5 0 0 1 0 1h-11A.5.5 0 0 1 2 8Z"/>
                                                            </svg>
                                                        </button>
                                                        <span class="mx-3 count">${service.selectedOptions[i].dataset['serviceCount']}</span>
                                                        <button type="button" class="btn btn-success btn-sm plusCount">
                                                            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-plus-lg" viewBox="0 0 16 16">
                                                                <path fill-rule="evenodd" d="M8 2a.5.5 0 0 1 .5.5v5h5a.5.5 0 0 1 0 1h-5v5a.5.5 0 0 1-1 0v-5h-5a.5.5 0 0 1 0-1h5v-5A.5.5 0 0 1 8 2Z"/>
                                                            </svg>
                                                        </button>
                                                    </div>
                                                </td>
                                                <td>
                                                    <div class="form-check form-switch">
                                                        <input class="form-check-input garanty" type="checkbox" role="switch">
                                                    </div>
                                                </td>
                                                <th><span class="Price">${service.selectedOptions[i].dataset['total']}</span></th>
                                            </tr>`;
                }
            }
        }

        let employeeSelects = document.querySelectorAll('select.employee-select')
        let checkedEmployees = document.getElementsByClassName('checkedEmployees');
        let serviceRows = document.getElementsByClassName('service-row');
        let garantyBtns = document.getElementsByClassName('garanty');
        let prices = document.getElementsByClassName('Price');
        let minusCounts = document.getElementsByClassName('minusCount');
        let counts = document.getElementsByClassName('count')
        let plusCounts = document.getElementsByClassName('plusCount');
        let totalPrice = document.getElementById('totalPrice');
        let removeServices = document.getElementsByClassName('removeService');
        let total = 0;
        let totalWithoutGaranty = 0;

        // Основной цикл для заполнения данными строчек таблицы
        for (let i = 0; i < serviceRows.length; i++) {
            const serviceRow = serviceRows[i];
            const employeeSelect = employeeSelects[i];
            const checkedEmployee = checkedEmployees[i]
            const removeService = removeServices[i];
            const minusCount = minusCounts[i];
            const plusCount = plusCounts[i];
            const count = counts[i];
            const garantyBtn = garantyBtns[i];
            const price = prices[i];

            totalWithoutGaranty += eval(price.innerText);

            checkedEmployee.innerHTML = '';

            if (eval(count.innerText) != 1) {
                minusCount.disabled = false;
            };

            // Отрисовка селектов мастеров
            employees.forEach(employee => {
                if (serviceRow.dataset['serviceEmployees'] != '[]') {
                    if (serviceRow.dataset['serviceEmployees'] != '') {
                        let employeesIINs = serviceRow.dataset['serviceEmployees'].split(',');

                        if (employeesIINs.indexOf(employee.IIN) != -1) {
                            employeeSelect.innerHTML += `<option value="${employee.IIN}" data-emp-name="${employee.name[0]}." data-emp-surname="${employee.surname}" selected data-subtext="${employee.IIN}">${employee.name} ${employee.surname}</option>`
                            checkedEmployee.innerHTML += `<span class="badge rounded-pill text-bg-warning text-truncate" style="max-width: 150px;">${employee.name[0]}. ${employee.surname}</span>`
                        }
                        else {
                            employeeSelect.innerHTML += `<option value="${employee.IIN}" data-emp-name="${employee.name[0]}." data-emp-surname="${employee.surname}" data-subtext="${employee.IIN}">${employee.name} ${employee.surname}</option>`
                        }
                    }
                    else {
                        employeeSelect.innerHTML += `<option value="${employee.IIN}" data-emp-name="${employee.name[0]}." data-emp-surname="${employee.surname}" data-subtext="${employee.IIN}">${employee.name} ${employee.surname}</option>`
                        checkedEmployee.innerHTML = 'Мастера не выбраны!';
                    }
                }
                else {
                    employeeSelect.innerHTML += `<option value="${employee.IIN}" data-emp-name="${employee.name[0]}." data-emp-surname="${employee.surname}" data-subtext="${employee.IIN}">${employee.name} ${employee.surname}</option>`
                    checkedEmployee.innerHTML = 'Мастера не выбраны!';
                }
            });

            // Событие на изменение селекта мастеров
            employeeSelect.onchange = e => {
                let selectedValues = [];

                checkedEmployee.innerHTML = '';

                if (employeeSelect.selectedOptions.length === 0) {
                    checkedEmployee.innerHTML = 'Мастера не выбраны!'
                }

                for (let j = 0; j < employeeSelect.selectedOptions.length; j++) {
                    const selectedOption = employeeSelect.selectedOptions[j];

                    selectedValues.push(selectedOption.value);
                    checkedEmployee.innerHTML += `<span class="badge rounded-pill text-bg-warning text-truncate" style="max-width: 150px;">${selectedOption.dataset['empName'].toUpperCase()} ${selectedOption.dataset['empSurname']}</span>`
                }

                serviceRow.dataset['serviceEmployees'] = selectedValues;
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceEmployees'] = selectedValues;
            };

            // Событие на удаление строчки кнопкой
            removeService.onclick = e => {
                if (eval(serviceRow.dataset['serviceGaranty']) != true) {
                    total -= eval(serviceRow.dataset['total']);
                }
                totalWithoutGaranty -= eval(serviceRow.dataset['total']);
                totalPrice.innerText = total;
                priceForPay.value = total;
                fullPrice.value = totalWithoutGaranty;
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].selected = false;
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceGaranty'] = false;
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceEmployees'] = '[]';
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceCount'] = 1;
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['total'] = serviceRow.dataset['servicePrice'];
                serviceRow.remove();

                if (serviceRows.length === 0) {
                    nothingSelected.classList.remove('d-none');
                }

                $('.service').selectpicker('destroy');
                $('.service').selectpicker('render');
            };

            // Событие на уменьшение количества услуг
            minusCount.onclick = e => {
                count.innerText = eval(count.innerText) - 1;
                price.innerText = eval(price.innerText) - eval(serviceRow.dataset['servicePrice']);
                serviceRow.dataset['serviceCount'] = count.innerText;
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceCount'] = count.innerText
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['total'] = price.innerText

                if (eval(serviceRow.dataset['serviceGaranty']) === false) {
                    serviceRow.dataset['total'] = price.innerText;
                    total -= eval(serviceRow.dataset['servicePrice']);
                    totalPrice.innerText = total;
                    priceForPay.value = total;
                }
                totalWithoutGaranty -= eval(serviceRow.dataset['servicePrice']);
                fullPrice.value = totalWithoutGaranty

                if (eval(count.innerText) === 1) {
                    minusCount.disabled = true;
                }
            };

            // Событие на увеличение количества услуг
            plusCount.onclick = e => {
                count.innerText = eval(count.innerText) + 1;
                price.innerText = eval(price.innerText) + eval(serviceRow.dataset['servicePrice']);
                serviceRow.dataset['serviceCount'] = count.innerText;
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceCount'] = count.innerText
                serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['total'] = price.innerText

                if (eval(serviceRow.dataset['serviceGaranty']) === false) {
                    serviceRow.dataset['total'] = price.innerText;
                    total += eval(serviceRow.dataset['servicePrice']);
                    totalPrice.innerText = total;
                    priceForPay.value = total;
                }
                totalWithoutGaranty += eval(serviceRow.dataset['servicePrice']);
                fullPrice.value = totalWithoutGaranty;

                minusCount.disabled = false;
            };

            // Проверка на гарантию в датасетах сервисов
            if (serviceRow.dataset['serviceGaranty'] === 'false') {
                garantyBtn.checked = false;
                price.style.cssText = 'text-decoration: none;';
            }
            else {
                garantyBtn.checked = true;
                price.style.cssText = 'text-decoration: line-through;';
                total -= eval(price.innerHTML);
            };

            // Событие на чекбокс гарантии
            garantyBtn.addEventListener('change', e => {
                if (garantyBtn.checked) {
                    garantyBtn.parentElement.parentElement.parentElement.dataset['serviceGaranty'] = 'true';
                    serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'true';
                    price.style.cssText = 'text-decoration: line-through;';
                    total -= eval(price.innerHTML);
                    totalPrice.innerText = total;
                    priceForPay.value = total;
                }
                else {
                    serviceRow.dataset['serviceGaranty'] = 'false';
                    serviceOptions[eval(serviceRow.dataset['serviceIndex'])].dataset['serviceGaranty'] = 'false';
                    price.style.cssText = 'text-decoration: none;';
                    total += eval(price.innerHTML);
                    totalPrice.innerText = total;
                    priceForPay.value = total;
                }
            });

            total += eval(price.innerText);
        }

        totalPrice.innerText = total;
        priceForPay.value = total;
        fullPrice.value = totalWithoutGaranty;

        $('.selectpicker').selectpicker('render');
    }
    else {
        let totalPrice = document.getElementById('totalPrice');

        tableBody.innerHTML = '';
        nothingSelected.classList.remove('d-none');
        totalPrice.innerText = 0;
    }
})

serviceEmployeeForm.addEventListener('submit', e => {
    e.preventDefault();

    let resultJobs = document.getElementById('resultServices');
    let serviceRows = document.getElementsByClassName('service-row');
    let checkedEmployees = document.getElementsByClassName('checkedEmployees');

    let result = [];

    for (let i = 0; i < serviceRows.length; i++) {
        const serviceRow = serviceRows[i];

        let parsed_employees = [];

        for (let j = 0; j < checkedEmployees[i].children.length; j++) {
            const employeeNameSurname = checkedEmployees[i].children[j].innerText;

            parsed_employees.push({
                'Наименование': employeeNameSurname,
                'ИИН': serviceRow.dataset['serviceEmployees'].split(',')[j]
            })
        }

        result.push({
            'Индекс': eval(serviceRow.dataset['serviceIndex']),
            'Название услуги': serviceRow.dataset['serviceName'],
            'Категория услуги': serviceRow.dataset['serviceCategory'],
            'Марка услуги': serviceRow.dataset['serviceMark'],
            'Количество услуг': eval(serviceRow.dataset['serviceCount']),
            'Цена услуги': eval(serviceRow.dataset['servicePrice']),
            'Сумма услуг': eval(serviceRow.dataset['total']),
            'Гарантия': eval(serviceRow.dataset['serviceGaranty']),
            'Мастера': parsed_employees
        });
    }

    resultJobs.value = JSON.stringify(result);

    serviceEmployeeForm.submit();
})
