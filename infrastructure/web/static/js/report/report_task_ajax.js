let reportForm = document.getElementById('reportForm');
let bodyBlock = document.getElementById('bodyBlock');


function renderReport(paidJobs, unpaidJobs, report) {
    if (paidJobs === true) {
        if (unpaidJobs === true) {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-success">Оплаченные работы</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-success border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th style="width: 500px;" scope="col">Название услуги</th>
                                                <th scope="col">Категория</th>
                                                <th scope="col">Марка</th>
                                                <th scope="col">Мастера</th>
                                                <th style="width: 150px;" scope="col">Гарантия</th>
                                                <th scope="col">Цена</th>
                                            </tr>
                                        </thead>
                                        <tbody id="paidJobsBody"></tbody>
                                    </table>
                                    <span class="badge fs-5 mb-2 bg-danger">Неоплаченные работы</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-danger border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th style="width: 500px;" scope="col">Название услуги</th>
                                                <th scope="col">Категория</th>
                                                <th scope="col">Марка</th>
                                                <th scope="col">Мастера</th>
                                                <th style="width: 150px;" scope="col">Гарантия</th>
                                                <th scope="col">Цена</th>
                                            </tr>
                                        </thead>
                                        <tbody id="unpaidJobsBody"></tbody>
                                    </table>
                                    <div class="d-flex justify-content-between">
                                        <div class="w-50">
                                            <span class="badge fs-5 mb-2 bg-primary">Зарплаты мастерам</span>
                                            <table class="table table-sm table-bordered border-secondary align-middle">
                                                <thead>
                                                    <tr class="table-primary border-secondary">
                                                        <th scope="col" class="text-center" style="width: 20px">№</th>
                                                        <th scope="col" style="width: 250px">Мастер</th>
                                                        <th scope="col" style="width: 100px">ИИН</th>
                                                        <th scope="col" style="width: 150px">Зарплата</th>
                                                    </tr>
                                                </thead>
                                                <tbody id="employeeSalaryBody"></tbody>
                                            </table>
                                        </div>
                                        <div style="width: 600px">
                                            <span class="badge fs-5 mb-2 bg-info">Итог</span>
                                            <table class="table table-sm table-bordered border-secondary align-middle">
                                                <thead>
                                                    <tr class="table-info border-secondary">
                                                        <th scope="col" class="text-center" style="width: 20px">№</th>
                                                        <th scope="col">Критерий</th>
                                                        <th scope="col">Сумма</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr>
                                                        <th class="text-center">1</th>
                                                        <th>Общая реализация</th>
                                                        <th>${report['total']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">2</th>
                                                        <th>Гарантия</th>
                                                        <th>${report['garanty']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">3</th>
                                                        <th>Оплаченные работы</th>
                                                        <th>${report['totalPaid']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">4</th>
                                                        <th>Неоплаченные работы</th>
                                                        <th>${report['totalUnpaid']}</th>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>`
        }
        else {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-success">Оплаченные работы</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-success border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th style="width: 500px;" scope="col">Название услуги</th>
                                                <th scope="col">Категория</th>
                                                <th scope="col">Марка</th>
                                                <th scope="col">Мастера</th>
                                                <th style="width: 150px;" scope="col">Гарантия</th>
                                                <th scope="col">Цена</th>
                                            </tr>
                                        </thead>
                                        <tbody id="paidJobsBody"></tbody>
                                    </table>
                                    <div class="d-flex justify-content-between">
                                        <div class="w-50">
                                            <span class="badge fs-5 mb-2 bg-primary">Зарплаты мастерам</span>
                                            <table class="table table-sm table-bordered border-secondary align-middle">
                                                <thead>
                                                    <tr class="table-primary border-secondary">
                                                        <th scope="col" class="text-center" style="width: 20px">№</th>
                                                        <th scope="col" style="width: 250px">Мастер</th>
                                                        <th scope="col" style="width: 100px">ИИН</th>
                                                        <th scope="col" style="width: 150px">Зарплата</th>
                                                    </tr>
                                                </thead>
                                                <tbody id="employeeSalaryBody"></tbody>
                                            </table>
                                        </div>
                                        <div style="width: 600px">
                                            <span class="badge fs-5 mb-2 bg-info">Итог</span>
                                            <table class="table table-sm table-bordered border-secondary align-middle">
                                                <thead>
                                                    <tr class="table-info border-secondary">
                                                        <th scope="col" class="text-center" style="width: 20px">№</th>
                                                        <th scope="col">Критерий</th>
                                                        <th scope="col">Сумма</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr>
                                                        <th class="text-center">1</th>
                                                        <th>Общая реализация</th>
                                                        <th>${report['total']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">2</th>
                                                        <th>Гарантия</th>
                                                        <th>${report['garanty']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">3</th>
                                                        <th>Оплаченные работы</th>
                                                        <th>${report['totalPaid']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">4</th>
                                                        <th>Неоплаченные работы</th>
                                                        <th>${report['totalUnpaid']}</th>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>`
        }
    }
    else {
        if (unpaidJobs === true) {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-danger">Неоплаченные работы</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-danger border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th style="width: 500px;" scope="col">Название услуги</th>
                                                <th scope="col">Категория</th>
                                                <th scope="col">Марка</th>
                                                <th scope="col">Мастера</th>
                                                <th style="width: 150px;" scope="col">Гарантия</th>
                                                <th scope="col">Цена</th>
                                            </tr>
                                        </thead>
                                        <tbody id="unpaidJobsBody"></tbody>
                                    </table>
                                    <div class="d-flex justify-content-between">
                                        <div class="w-50">
                                            <span class="badge fs-5 mb-2 bg-primary">Зарплаты мастерам</span>
                                            <table class="table table-sm table-bordered border-secondary align-middle">
                                                <thead>
                                                    <tr class="table-primary border-secondary">
                                                        <th scope="col" class="text-center" style="width: 20px">№</th>
                                                        <th scope="col" style="width: 250px">Мастер</th>
                                                        <th scope="col" style="width: 100px">ИИН</th>
                                                        <th scope="col" style="width: 150px">Зарплата</th>
                                                    </tr>
                                                </thead>
                                                <tbody id="employeeSalaryBody"></tbody>
                                            </table>
                                        </div>
                                        <div style="width: 600px">
                                            <span class="badge fs-5 mb-2 bg-info">Итог</span>
                                            <table class="table table-sm table-bordered border-secondary align-middle">
                                                <thead>
                                                    <tr class="table-info border-secondary">
                                                        <th scope="col" class="text-center" style="width: 20px">№</th>
                                                        <th scope="col">Критерий</th>
                                                        <th scope="col">Сумма</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr>
                                                        <th class="text-center">1</th>
                                                        <th>Общая реализация</th>
                                                        <th>${report['total']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">2</th>
                                                        <th>Гарантия</th>
                                                        <th>${report['garanty']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">3</th>
                                                        <th>Оплаченные работы</th>
                                                        <th>${report['totalPaid']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">4</th>
                                                        <th>Неоплаченные работы</th>
                                                        <th>${report['totalUnpaid']}</th>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>`
        }
        else {
            bodyBlock.innerHTML = ` <div class="d-flex justify-content-between">
                                        <div class="w-50">
                                            <span class="badge fs-5 mb-2 bg-primary">Зарплаты мастерам</span>
                                            <table class="table table-sm table-bordered border-secondary align-middle">
                                                <thead>
                                                    <tr class="table-primary border-secondary">
                                                        <th scope="col" class="text-center" style="width: 20px">№</th>
                                                        <th scope="col" style="width: 250px">Мастер</th>
                                                        <th scope="col" style="width: 100px">ИИН</th>
                                                        <th scope="col" style="width: 150px">Зарплата</th>
                                                    </tr>
                                                </thead>
                                                <tbody id="employeeSalaryBody"></tbody>
                                            </table>
                                        </div>
                                        <div style="width: 600px">
                                            <span class="badge fs-5 mb-2 bg-info">Итог</span>
                                            <table class="table table-sm table-bordered border-secondary align-middle">
                                                <thead>
                                                    <tr class="table-info border-secondary">
                                                        <th scope="col" class="text-center" style="width: 20px">№</th>
                                                        <th scope="col">Критерий</th>
                                                        <th scope="col">Сумма</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    <tr>
                                                        <th class="text-center">1</th>
                                                        <th>Общая реализация</th>
                                                        <th>${report['total']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">2</th>
                                                        <th>Гарантия</th>
                                                        <th>${report['garanty']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">3</th>
                                                        <th>Оплаченные работы</th>
                                                        <th>${report['totalPaid']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">4</th>
                                                        <th>Неоплаченные работы</th>
                                                        <th>${report['totalUnpaid']}</th>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>`
        }
    }

    let paidJobsBody = document.getElementById('paidJobsBody');
    let unpaidJobsBody = document.getElementById('unpaidJobsBody');
    let employeeSalaryBody = document.getElementById('employeeSalaryBody');

    if (paidJobsBody != undefined) {
        for (let i = 0; i < report['paidJobs'].length; i++) {
            const job = report['paidJobs'][i];

            if (job['Гарантия'] === true) {
                paidJobsBody.innerHTML += `<tr>
                                    <th class="text-center">${i + 1}</th>
                                    <td>${job['Название услуги']}</td>
                                    <td>${job['Категория услуги']}</td>
                                    <td>${job['Марка услуги']}</td>
                                    <td class="employeeBody"></td>
                                    <td>На гарантии</td>
                                    <th>${job['Цена услуги']}</th>
                                </tr>`
            }
            else {
                paidJobsBody.innerHTML += `<tr>
                                    <th class="text-center">${i + 1}</th>
                                    <td>${job['Название услуги']}</td>
                                    <td>${job['Категория услуги']}</td>
                                    <td>${job['Марка услуги']}</td>
                                    <td class="employeeBody"></td>
                                    <td></td>
                                    <th>${job['Цена услуги']}</th>
                                </tr>`
            }

            for (j = 0; j < job['Мастера'].length; j++) {
                const employee = job['Мастера'][j];
                let employeeBodies = document.getElementsByClassName('employeeBody');

                employeeBodies[employeeBodies.length - 1].innerHTML += `<div>${employee['Наименование']}</div>`
            }
        }
    }

    if (unpaidJobsBody != undefined) {
        for (let i = 0; i < report['unpaidJobs'].length; i++) {
            const job = report['unpaidJobs'][i];

            if (job['Гарантия'] === true) {
                unpaidJobsBody.innerHTML += `<tr>
                                                <th class="text-center">${i + 1}</th>
                                                <td>${job['Название услуги']}</td>
                                                <td>${job['Категория услуги']}</td>
                                                <td>${job['Марка услуги']}</td>
                                                <td class="employeeBody"></td>
                                                <td>На гарантии</td>
                                                <th>${job['Цена услуги']}</th>
                                            </tr>`
            }
            else {
                unpaidJobsBody.innerHTML += `<tr>
                                                <th class="text-center">${i + 1}</th>
                                                <td>${job['Название услуги']}</td>
                                                <td>${job['Категория услуги']}</td>
                                                <td>${job['Марка услуги']}</td>
                                                <td class="employeeBody"></td>
                                                <td></td>
                                                <th>${job['Цена услуги']}</th>
                                            </tr>`
            }

            for (j = 0; j < job['Мастера'].length; j++) {
                const employee = job['Мастера'][j];
                let employeeBodies = document.getElementsByClassName('employeeBody');

                employeeBodies[employeeBodies.length - 1].innerHTML += `<div>${employee['Наименование']}</div>`
            }
        }
    }

    for (let i = 0; i < report['employeeSalary'].length; i++) {
        const employeeSalary = report['employeeSalary'][i];

        employeeSalaryBody.innerHTML += `<tr>
                                            <th class="text-center">${i + 1}</th>
                                            <td>${employeeSalary['Наименование']}</td>
                                            <td>${employeeSalary['ИИН']}</td>
                                            <th>${employeeSalary['Зарплата']}</th>
                                        </tr>`
    }
}


reportForm.addEventListener('submit', e => {
    e.preventDefault();

    reportSocket = new WebSocket(`ws://${window.location.host}/report/create`);

    reportSocket.onopen = e => {
        reportSocket.send(JSON.stringify({
            'from_date': document.getElementById('from_date').value,
            'to_date': document.getElementById('to_date').value,
            'tpID': document.getElementById('tpID').value
        }));

        bodyBlock.innerHTML = '<div style="position: absolute; bottom: 50%; left: 50%;"> \
                                    <div class="spinner-border" role="status"> \
                                        <span class="visually-hidden">Loading...</span> \
                                    </div> \
                                    <h5 style="position: relative; right: 75px;">Отчет составляется</h5> \
                                </div>';
    };

    reportSocket.onmessage = e => {
        let report = JSON.parse(e.data);

        if (report['paidJobs'].length != 0) {
            if (report['unpaidJobs'].length != 0) {
                renderReport(true, true, report)
            }
            else {
                renderReport(true, false, report)
            }
        }
        else {
            if (report['unpaidJobs'].length != 0) {
                renderReport(false, true, report)
            }
            else {
                renderReport(false, false, report)
            }
        }

        reportSocket.close();
    };
});
