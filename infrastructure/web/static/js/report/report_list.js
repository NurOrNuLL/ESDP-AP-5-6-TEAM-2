let body = document.getElementById('body');

$.ajax({
    url: `${locationHost}/org/1/tp/${tpID}/report/save/`,
    method: 'GET',
    success: (data) => {
        if (data.items.length != 0) {
            data.items.forEach(function (item) {
                var fromDate = new Date(item.from_date);
                var dd = String(fromDate.getDate()).padStart(2, '0');
                var mm = String(fromDate.getMonth() + 1).padStart(2, '0');
                var yyyy = fromDate.getFullYear();
                fromDate = dd + '.' + mm + '.' + yyyy;

                var toDate = new Date(item.to_date);
                var dd = String(toDate.getDate()).padStart(2, '0');
                var mm = String(toDate.getMonth() + 1).padStart(2, '0');
                var yyyy = toDate.getFullYear();
                toDate = dd + '.' + mm + '.' + yyyy;

                if (item.report.report_type === 1) {
                    item.report.report_type = 'Общий'
                } else if (item.report.report_type === 2) {
                    item.report.report_type = 'Заказ-наряды'
                } else if (item.report.report_type === 3) {
                    item.report.report_type = 'Зарплаты'
                }
                if (item.report.report_type === 'Общий') {
                    body.innerHTML += `<tr><td>${item.created_at}</td><td>${fromDate} - ${toDate}</td><td><span class="badge rounded-pill text-bg-primary">${item.report.report_type}</span></td></tr>`
                } else if (item.report.report_type === 'Заказ-наряды') {
                    body.innerHTML += `<tr><td>${item.created_at}</td><td>${fromDate} - ${toDate}</td><td><span class="badge rounded-pill text-bg-success">${item.report.report_type}</span></td></tr>`
                } else if (item.report.report_type === 'Зарплаты') {
                    body.innerHTML += `<tr><td>${item.created_at}</td><td>${fromDate} - ${toDate}</td><td><span class="badge rounded-pill text-bg-danger">${item.report.report_type}</span></td></tr>`
                }
            })
        } else {
            body.innerHTML = '<h4 style="position: absolute; top: 50%; left: 50%" class="text-center">Ничего не найдено!</h4>'
        }
    },
    error: (err) => {
        console.log(err)
    }
})
