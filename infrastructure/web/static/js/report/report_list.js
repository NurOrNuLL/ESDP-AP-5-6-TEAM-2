let body = document.getElementById('body');
let reportSocket;


if (DEBUG === true) {
    reportSocket = new WebSocket(`ws://${window.location.host}/wss/report/list/`);
}
else {
    reportSocket = new WebSocket(`wss://${window.location.host}/wss/report/list/`);
}

reportSocket.onopen = (e) => {
    reportSocket.send(JSON.stringify({
        'tpID': tpID,
    }));

    body.innerHTML = '<div style="position: absolute; bottom: 50%; left: 56%;"> \
                            <div class="spinner-border" role="status"> \
                                <span class="visually-hidden">Loading...</span> \
                            </div> \
                            <h5 style="position: relative; right: 87px;">Список загружается</h5> \
                        </div>';
}

reportSocket.onmessage = (e) => {
    let reports = JSON.parse(e.data);

    body.innerHTML = '';

    for (report of reports) {
        let fromDate = new Date(report.from_date);
        let dd = String(fromDate.getDate()).padStart(2, '0');
        let mm = String(fromDate.getMonth() + 1).padStart(2, '0');
        let yyyy = fromDate.getFullYear();
        fromDate = dd + '.' + mm + '.' + yyyy;

        let toDate = new Date(report.to_date);
        dd = String(toDate.getDate()).padStart(2, '0');
        mm = String(toDate.getMonth() + 1).padStart(2, '0');
        yyyy = toDate.getFullYear();
        toDate = dd + '.' + mm + '.' + yyyy;
        if (report.report.report_type === 1) {
            report.report.report_type = 'Общий'
        } else if (report.report.report_type === 2) {
            report.report.report_type = 'Заказ-наряды'
        } else if (report.report.report_type === 3) {
            report.report.report_type = 'Зарплаты'
        }
        if (report.report.report_type === 'Общий') {
            body.innerHTML += `<tr><td><a href="/org/1/tp/${tpID}/report/${report.uuid}/">${report.created_at}</a></td><td>${fromDate} - ${toDate}</td><td><span class="badge rounded-pill text-bg-primary">${report.report.report_type}</span></td></tr>`
        } else if (report.report.report_type === 'Заказ-наряды') {
            body.innerHTML += `<tr><td><a href="/org/1/tp/${tpID}/report/${report.uuid}/">${report.created_at}</a></td><td>${fromDate} - ${toDate}</td><td><span class="badge rounded-pill text-bg-success">${report.report.report_type}</span></td></tr>`
        } else if (report.report.report_type === 'Зарплаты') {
            body.innerHTML += `<tr><td><a href="/org/1/tp/${tpID}/report/${report.uuid}/">${report.created_at}</a></td><td>${fromDate} - ${toDate}</td><td><span class="badge rounded-pill text-bg-danger">${report.report.report_type}</span></td></tr>`
        }
    }

    reportSocket.close();
}
