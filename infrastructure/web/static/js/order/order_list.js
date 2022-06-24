let beforeTableBlock = document.getElementById('beforeTable');

function render(search, date, status, payment_status, page, limit) {
    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/order/list/filter?search=${search}&date=${date}&status=${status}&payment_status=${payment_status}&page=${page}&limit=${limit}`,
        method: 'get',
        success: (data) => {
            body.innerHTML = '';
            if (data.length != 0) {
                beforeTableBlock.innerHTML = '';
                data.results.forEach(function (item) {
                    var today = new Date(item.created_at);
                    var dd = String(today.getDate()).padStart(2, '0');
                    var mm = String(today.getMonth() + 1).padStart(2, '0');
                    var yyyy = today.getFullYear();
                    var hh = String(today.getHours())
                    var min = String(today.getMinutes())
                    today = dd + '.' + mm + '.' + yyyy + ' ' + hh + ':' + min;

                    if (item.status.trim() === 'В работе'.trim() && item.payment.payment_status.trim() === 'Не оплачено'.trim()) {
                        body.innerHTML += '<tr><td>' + item.id + '</td><td>' + today + '</td><td>' + '<span class="badge rounded-pill text-bg-primary">'
                        + item.status + '</span>' + '</td><td>' + '<span class="badge rounded-pill text-bg-danger">' + item.payment.payment_status + '</span>' + '</td>' +
                        '<td>' + item.contractor.name + '</td><td>' + item.own.number + '</td>' +
                        '<td class="d-flex justify-content-end"><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/order/' + item.id + '/">Детали</a></td></tr>'
                    }
                    else if (item.status.trim() === 'В работе'.trim() && item.payment.payment_status.trim() != 'Не оплачено'.trim()) {
                        body.innerHTML += '<tr><td>' + item.id + '</td><td>' + today + '</td><td>' + '<span class="badge rounded-pill text-bg-primary">'
                        + item.status + '</span>' + '</td><td>' + '<span class="badge rounded-pill text-bg-success">' + item.payment.payment_status + '</span>' + '</td>' +
                        '<td>' + item.contractor.name + '</td><td>' + item.own.number + '</td>' +
                        '<td class="d-flex justify-content-end"><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/order/' + item.id + '/">Детали</a></td></tr>'
                    }
                    else if (item.status.trim() != 'В работе'.trim() && item.payment.payment_status.trim() === 'Не оплачено'.trim()) {
                        body.innerHTML += '<tr><td>' + item.id + '</td><td>' + today + '</td><td>' + '<span class="badge rounded-pill text-bg-success">'
                        + item.status + '</span>' + '</td><td>' + '<span class="badge rounded-pill text-bg-danger">' + item.payment.payment_status + '</span>' + '</td>' +
                        '<td>' + item.contractor.name + '</td><td>' + item.own.number + '</td>' +
                        '<td class="d-flex justify-content-end"><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/order/' + item.id + '/">Детали</a></td></tr>'
                    }
                    else {
                        body.innerHTML += '<tr><td>' + item.id + '</td><td>' + today + '</td><td>' + '<span class="badge rounded-pill text-bg-success">'
                        + item.status + '</span>' + '</td><td>' + '<span class="badge rounded-pill text-bg-success">' + item.payment.payment_status + '</span>' + '</td>' +
                        '<td>' + item.contractor.name + '</td><td>' + item.own.number + '</td>' +
                        '<td class="d-flex justify-content-end"><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/order/' + item.id + '/">Детали</a></td></tr>'
                    }
                })

                if (data.previous === null && data.next === null) {
                    next.classList.add('disabled')
                    back.classList.add('disabled')
                } else if (data.next === null && data.previous != null) {
                    next.classList.add('disabled')
                    back.classList.remove('disabled')
                } else if (data.next != null && data.previous === null) {
                    back.classList.add('disabled')
                    next.classList.remove('disabled')
                } else {
                    next.classList.remove('disabled')
                    back.classList.remove('disabled')
                }
            } else {
                beforeTableBlock.innerHTML = '';
                beforeTableBlock.innerHTML += '<h4 class="text-center">Ничего не найдено!</h4>';
            }
        },
        error: (response) => {
            console.log(response)
            body.innerHTML = '';
            beforeTableBlock.innerHTML = '';
            beforeTableBlock.innerHTML += '<h4 class="text-center">Ничего не найдено!</h4>';
        }
    })
}
let orderDate = document.getElementById('order_date')
let orderStatus = document.getElementById('order_status')
let orderPaymentStatus = document.getElementById('payment_status')
let search = document.getElementById('search')

let page = document.getElementById('page');
let limit = document.getElementById('limit');
let back = document.getElementById('back');
let next = document.getElementById('next');

render('', '', '', '', 1, 999999)

limit.addEventListener('input', (e) => {
    if (limit.value === '' || limit.value === 0) {
        render(search.value, orderDate.value, orderStatus.value, orderPaymentStatus.value, page.value, 999999)
    }
    render(search.value, orderDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})

next.addEventListener('click', (e) => {
    page.value = parseInt(page.value) + 1
    render(search.value, orderDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})

back.addEventListener('click', (e) => {
    page.value = parseInt(page.value) - 1
    render(search.value, orderDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})

search.addEventListener('input', (e) => {
    render(search.value, orderDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})
orderDate.addEventListener('change', (e) => {
    render(search.value, orderDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})
orderStatus.addEventListener('change', (e) => {
    render(search.value, orderDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})

orderPaymentStatus.addEventListener('change', (e) => {
    render(search.value, orderDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})
