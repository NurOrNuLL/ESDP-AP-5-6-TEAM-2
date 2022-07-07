let reportForm = document.getElementById('reportForm');
let resetReport = document.getElementById('resetReport');
let downloadReport = document.getElementById('downloadReport');
let reportFormat = document.getElementById('file_format');
let bodyBlock = document.getElementById('bodyBlock');
let downloadData = document.getElementById('downloadData');
let errorAlert = document.getElementById('errorAlert');
let error = document.getElementById('error');
let reportInput = document.getElementById('reportInput');
let reportSave = document.getElementById('reportSave');
let fromDate = document.getElementById('from_date');
let toDate = document.getElementById('to_date');


function renderReportType1(paidOrders, unpaidOrders, report) {
    if (paidOrders === true) {
        if (unpaidOrders === true) {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-success">Оплаченные заказ наряды</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-success border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th scope="col">Дата создания</th>
                                                <th scope="col">Дата завершения</th>
                                                <th scope="col">Контрагент</th>
                                                <th scope="col">Номер авто/Запчасть</th>
                                                <th scope="col">Гарантия</th>
                                                <th scope="col">Сумма</th>
                                            </tr>
                                        </thead>
                                        <tbody id="paidOrdersBody"></tbody>
                                    </table>
                                    <span class="badge fs-5 mb-2 bg-danger">Неоплаченные заказ наряды</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-danger border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th scope="col">Дата создания</th>
                                                <th scope="col">Дата завершения</th>
                                                <th scope="col">Контрагент</th>
                                                <th scope="col">Номер авто/Запчасть</th>
                                                <th scope="col">Гарантия</th>
                                                <th scope="col">Сумма</th>
                                            </tr>
                                        </thead>
                                        <tbody id="unpaidOrdersBody"></tbody>
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
                                                        <th>Оплаченные заказ наряды</th>
                                                        <th>${report['totalPaid']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">4</th>
                                                        <th>Неоплаченные заказ наряды</th>
                                                        <th>${report['totalUnpaid']}</th>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>`
        }
        else {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-success">Оплаченные заказ наряды</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-success border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th scope="col">Дата создания</th>
                                                <th scope="col">Дата завершения</th>
                                                <th scope="col">Контрагент</th>
                                                <th scope="col">Номер авто/Запчасть</th>
                                                <th scope="col">Гарантия</th>
                                                <th scope="col">Сумма</th>
                                            </tr>
                                        </thead>
                                        <tbody id="paidOrdersBody"></tbody>
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
                                                        <th>Оплаченные заказ наряды</th>
                                                        <th>${report['totalPaid']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">4</th>
                                                        <th>Неоплаченные заказ наряды</th>
                                                        <th>${report['totalUnpaid']}</th>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>`
        }
    }
    else {
        if (unpaidOrders === true) {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-success">Неоплаченные заказ наряды</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-success border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th scope="col">Дата создания</th>
                                                <th scope="col">Дата завершения</th>
                                                <th scope="col">Контрагент</th>
                                                <th scope="col">Номер авто/Запчасть</th>
                                                <th scope="col">Гарантия</th>
                                                <th scope="col">Сумма</th>
                                            </tr>
                                        </thead>
                                        <tbody id="paidOrdersBody"></tbody>
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
                                                        <th>Оплаченные заказ наряды</th>
                                                        <th>${report['totalPaid']}</th>
                                                    </tr>
                                                    <tr>
                                                        <th class="text-center">4</th>
                                                        <th>Неоплаченные заказ наряды</th>
                                                        <th>${report['totalUnpaid']}</th>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>`
        }
        else {
            bodyBlock.innerHTML = '<h4 class="text-center text-danger" style="position: absolute; bottom: 50%; left: 37%;">Недостаточно данных для отчета!</h4>'
            reportSave.disabled = true;
            resetReport.disabled = true;
            downloadReport.disabled = true;
            reportFormat.disabled = true;
        }
    }

    let paidOrdersBody = document.getElementById('paidOrdersBody');
    let unpaidOrdersBody = document.getElementById('unpaidOrdersBody');
    let employeeSalaryBody = document.getElementById('employeeSalaryBody');

    if (paidOrdersBody !== undefined) {
        for (let i = 0; i < report['paidOrders'].length; i++) {
            const order = report['paidOrders'][i];

            paidOrdersBody.innerHTML += `<tr>
                                            <th class="text-center">
                                                <a class="link-primary" href="/org/1/tp/${tpID}/order/${order.order_id}/">
                                                    ${order.order_id}
                                                </a>
                                            </th>
                                            <td>${order.created_at}</td>
                                            <td>${order.finished_at}</td>
                                            <td>
                                                <a class="link-primary" href="/org/1/tp/${tpID}/order/${order.contractor_id}/">
                                                    ${order.contractor}
                                                </a>
                                            </td>
                                            <td>${order.own}</td>
                                            <th>${order.garanty}</th>
                                            <th>${order.total}</th>
                                        </tr>`
        }
    }

    if (unpaidOrdersBody !== undefined) {
        for (let i = 0; i < report['unpaidOrders'].length; i++) {
            const order = report['unpaidOrders'][i];

            unpaidOrdersBody.innerHTML += `<tr>
                                            <th class="text-center">
                                                <a class="link-primary" href="/org/1/tp/${tpID}/order/${order.order_id}/">
                                                    ${order.order_id}
                                                </a>
                                            </th>
                                            <td>${order.created_at}</td>
                                            <td>${order.finished_at}</td>
                                            <td>
                                                <a class="link-primary" href="/org/1/tp/${tpID}/order/${order.contractor_id}/">
                                                    ${order.contractor}
                                                </a>
                                            </td>
                                            <td>${order.own}</td>
                                            <th>${order.garanty}</th>
                                            <th>${order.total}</th>
                                        </tr>`
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


function renderReportType2(paidOrders, unpaidOrders, report) {
    if (paidOrders === true) {
        if (unpaidOrders === true) {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-success">Оплаченные заказ наряды</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-success border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th scope="col">Дата создания</th>
                                                <th scope="col">Дата завершения</th>
                                                <th scope="col">Контрагент</th>
                                                <th scope="col">Номер авто/Запчасть</th>
                                                <th scope="col">Гарантия</th>
                                                <th scope="col">Сумма</th>
                                            </tr>
                                        </thead>
                                        <tbody id="paidOrdersBody"></tbody>
                                    </table>
                                    <span class="badge fs-5 mb-2 bg-danger">Неоплаченные заказ наряды</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-danger border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th scope="col">Дата создания</th>
                                                <th scope="col">Дата завершения</th>
                                                <th scope="col">Контрагент</th>
                                                <th scope="col">Номер авто/Запчасть</th>
                                                <th scope="col">Гарантия</th>
                                                <th scope="col">Сумма</th>
                                            </tr>
                                        </thead>
                                        <tbody id="unpaidOrdersBody"></tbody>
                                    </table>
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
                                                    <th>Оплаченные заказ наряды</th>
                                                    <th>${report['totalPaid']}</th>
                                                </tr>
                                                <tr>
                                                    <th class="text-center">4</th>
                                                    <th>Неоплаченные заказ наряды</th>
                                                    <th>${report['totalUnpaid']}</th>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>`
        }
        else {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-success">Оплаченные заказ наряды</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-success border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th scope="col">Дата создания</th>
                                                <th scope="col">Дата завершения</th>
                                                <th scope="col">Контрагент</th>
                                                <th scope="col">Номер авто/Запчасть</th>
                                                <th scope="col">Гарантия</th>
                                                <th scope="col">Сумма</th>
                                            </tr>
                                        </thead>
                                        <tbody id="paidOrdersBody"></tbody>
                                    </table>
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
                                                    <th>Оплаченные заказ наряды</th>
                                                    <th>${report['totalPaid']}</th>
                                                </tr>
                                                <tr>
                                                    <th class="text-center">4</th>
                                                    <th>Неоплаченные заказ наряды</th>
                                                    <th>${report['totalUnpaid']}</th>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>`
        }
    }
    else {
        if (unpaidOrders === true) {
            bodyBlock.innerHTML = ` <span class="badge fs-5 mb-2 bg-success">Неоплаченные заказ наряды</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-success border-secondary">
                                                <th class="text-center" scope="col" style="width: 40px">№</th>
                                                <th scope="col">Дата создания</th>
                                                <th scope="col">Дата завершения</th>
                                                <th scope="col">Контрагент</th>
                                                <th scope="col">Номер авто/Запчасть</th>
                                                <th scope="col">Гарантия</th>
                                                <th scope="col">Сумма</th>
                                            </tr>
                                        </thead>
                                        <tbody id="paidOrdersBody"></tbody>
                                    </table>
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
                                                    <th>Оплаченные заказ наряды</th>
                                                    <th>${report['totalPaid']}</th>
                                                </tr>
                                                <tr>
                                                    <th class="text-center">4</th>
                                                    <th>Неоплаченные заказ наряды</th>
                                                    <th>${report['totalUnpaid']}</th>
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>`
        }
        else {
            bodyBlock.innerHTML = '<h4 class="text-center text-danger" style="position: absolute; bottom: 50%; left: 37%;">Недостаточно данных для отчета!</h4>'
            reportSave.disabled = true;
            resetReport.disabled = true;
            downloadReport.disabled = true;
            reportFormat.disabled = true;
        }
    }

    let paidOrdersBody = document.getElementById('paidOrdersBody');
    let unpaidOrdersBody = document.getElementById('unpaidOrdersBody');

    if (paidOrdersBody !== undefined) {
        for (let i = 0; i < report['paidOrders'].length; i++) {
            const order = report['paidOrders'][i];

            paidOrdersBody.innerHTML += `<tr>
                                            <th class="text-center">
                                                <a class="link-primary" href="/org/1/tp/${tpID}/order/${order.order_id}/">
                                                    ${order.order_id}
                                                </a>
                                            </th>
                                            <td>${order.created_at}</td>
                                            <td>${order.finished_at}</td>
                                            <td>
                                                <a class="link-primary" href="/org/1/tp/${tpID}/order/${order.contractor_id}/">
                                                    ${order.contractor}
                                                </a>
                                            </td>
                                            <td>${order.own}</td>
                                            <th>${order.garanty}</th>
                                            <th>${order.total}</th>
                                        </tr>`
        }
    }

    if (unpaidOrdersBody !== undefined) {
        for (let i = 0; i < report['unpaidOrders'].length; i++) {
            const order = report['unpaidOrders'][i];

            unpaidOrdersBody.innerHTML += `<tr>
                                            <th class="text-center">
                                                <a class="link-primary" href="/org/1/tp/${tpID}/order/${order.order_id}/">
                                                    ${order.order_id}
                                                </a>
                                            </th>
                                            <td>${order.created_at}</td>
                                            <td>${order.finished_at}</td>
                                            <td>
                                                <a class="link-primary" href="/org/1/tp/${tpID}/order/${order.contractor_id}/">
                                                    ${order.contractor}
                                                </a>
                                            </td>
                                            <td>${order.own}</td>
                                            <th>${order.garanty}</th>
                                            <th>${order.total}</th>
                                        </tr>`
        }
    }
}


function renderReportType3(report) {
    if (report['employeeSalary'].length !== 0) {
        bodyBlock.innerHTML = ` <div>
                                    <span class="badge fs-5 mb-2 bg-primary">Зарплаты мастерам</span>
                                    <table class="table table-sm table-bordered border-secondary align-middle">
                                        <thead>
                                            <tr class="table-primary border-secondary">
                                                <th scope="col" class="text-center" style="width: 20px">№</th>
                                                <th scope="col" style="width: 250px">Мастер</th>
                                                <th scope="col" style="width: 100px">ИИН</th>
                                                <th scope="col" style="width: 100px">Телефон</th>
                                                <th scope="col" style="width: 150px">Зарплата</th>
                                            </tr>
                                        </thead>
                                        <tbody id="employeeSalaryBody"></tbody>
                                    </table>
                                </div>`
    }
    else {
        bodyBlock.innerHTML = '<h4 class="text-center text-danger" style="position: absolute; bottom: 50%; left: 37%;">Недостаточно данных для отчета!</h4>'
        reportSave.disabled = true;
        resetReport.disabled = true;
        downloadReport.disabled = true;
        reportFormat.disabled = true;
    }

    let employeeSalaryBody = document.getElementById('employeeSalaryBody');

    for (let i = 0; i < report['employeeSalary'].length; i++) {
        const employeeSalary = report['employeeSalary'][i];

        employeeSalaryBody.innerHTML += `<tr>
                                            <th class="text-center">${i + 1}</th>
                                            <td>${employeeSalary['Наименование']}</td>
                                            <td>${employeeSalary['ИИН']}</td>
                                            <td>${employeeSalary['Телефон']}</td>
                                            <th>${employeeSalary['Зарплата']}</th>
                                        </tr>`
    }
}


resetReport.onclick = e => {
    bodyBlock.innerHTML = '<h4 class="text-center" style="position: absolute; bottom: 50%; left: 40%;">Отчет еще не сформирован!</h4>'
    reportInput.value = '';

    reportSave.disabled = true;
    resetReport.disabled = true;
    downloadReport.disabled = true;
    reportFormat.disabled = true;
}


reportForm.addEventListener('submit', e => {
    e.preventDefault();

    if (DEBUG === true) {
        reportSocket = new WebSocket(`ws://${window.location.host}/report/create/`);
    }
    else {
        reportSocket = new WebSocket(`wss://${window.location.host}/report/create/`);
    }

    reportSocket.onopen = e => {
        reportSocket.send(JSON.stringify({
            'from_date': document.getElementById('from_date').value,
            'to_date': document.getElementById('to_date').value,
            'tpID': document.getElementById('tpID').value,
            'report_type': document.getElementById('report_type').value
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

        if (report['error'] === undefined) {
            if (!(errorAlert.classList.contains('d-none'))) {
                errorAlert.classList.add('d-none')
            }

            reportInput.value = JSON.stringify(report);

            downloadData.value = JSON.stringify(report);
            downloadData.innerText = JSON.stringify(report);

            reportSave.disabled = false;
            resetReport.disabled = false;
            downloadReport.disabled = false;
            reportFormat.disabled = false;

            if (report['report_type'] === 1) {
                if (report['paidOrders'].length !== 0) {
                    if (report['unpaidOrders'].length !== 0) {
                        renderReportType1(true, true, report)
                    }
                    else {
                        renderReportType1(true, false, report)
                    }
                }
                else {
                    if (report['unpaidOrders'].length !== 0) {
                        renderReportType1(false, true, report)
                    }
                    else {
                        renderReportType1(false, false, report)
                    }
                }
            }
            else if (report['report_type'] === 2) {
                if (report['paidOrders'].length !== 0) {
                    if (report['unpaidOrders'].length !== 0) {
                        renderReportType2(true, true, report)
                    }
                    else {
                        renderReportType2(true, false, report);
                    }
                }
                else {
                    if (report['unpaidOrders'].length !== 0) {
                        renderReportType2(false, true, report);
                    }
                    else {
                        renderReportType2(false, false, report);
                    }
                }
            }
            else if (report['report_type'] === 3) {
                renderReportType3(report);
            }
        }
        else {
            errorAlert.classList.remove('d-none');
            error.innerText = report.error;

            bodyBlock.innerHTML = '<h4 class="text-center" style="position: absolute; bottom: 50%; left: 40%;">Отчет еще не сформирован!</h4>'

            reportSave.disabled = true;
            resetReport.disabled = true;
            downloadReport.disabled = true;
            reportFormat.disabled = true;
        }

        reportSocket.close();
    }
})

reportSave.onclick = e => {
    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/report/save/`,
        method: 'post',
        data: JSON.stringify({
            'report': reportInput.value,
            'from_date': fromDate.value,
            'to_date': toDate.value
        }),
        contentType: 'application/json',
        headers: {'X-CSRFToken': $.cookie('csrftoken')},
        success: (data) => {
            console.log(data);
        },
        errors: (err) => {
            console.log(err);
        }
    })
}
