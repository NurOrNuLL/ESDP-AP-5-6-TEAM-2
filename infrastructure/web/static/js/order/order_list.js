let beforeTableBlock = document.getElementById('beforeTable');

function render(search, from_date, to_date, status, payment_status, page, limit) {
    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/order/list/filter?search=${search}&from_date=${from_date}&to_date=${to_date}&status=${status}&payment_status=${payment_status}&page=${page}&limit=${limit}`,
        method: 'get',
        async: false,
        success: (data) => {
            body.innerHTML = '';
            if (data.results.length != 0) {
                beforeTableBlock.innerHTML = '';
                data.results.forEach(function (item) {
                    var today = new Date(item.created_at);
                    var dd = String(today.getDate()).padStart(2, '0');
                    var mm = String(today.getMonth() + 1).padStart(2, '0');
                    var yyyy = today.getFullYear();
                    var hh = String(today.getHours())
                    var min
                    if (today.getMinutes() < 10) {
                        min = '0' + String(today.getMinutes())
                    } else {
                        min = String(today.getMinutes())
                    }

                    today = dd + '.' + mm + '.' + yyyy + ' ' + hh + ':' + min;

                    var finish_day = new Date(item.finished_at);
                    var dd = String(finish_day.getDate()).padStart(2, '0');
                    var mm = String(finish_day.getMonth() + 1).padStart(2, '0');
                    var yyyy = finish_day.getFullYear();
                    var hh = String(finish_day.getHours())
                    var min
                    if (finish_day.getMinutes() < 10) {
                        min = '0' + String(finish_day.getMinutes())
                    } else {
                        min = String(finish_day.getMinutes())
                    }
                    finish_day = dd + '.' + mm + '.' + yyyy + ' ' + hh + ':' + min;

                    if (item.status.trim() === 'В работе'.trim() && item.payment.payment_status.trim() === 'Не оплачено'.trim()) {
                        body.innerHTML += `<tr class="orderRow"><td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${item.id}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${today}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/"></a></td>
                        <td><span class="badge rounded-pill text-bg-primary">${item.status}</span></td>
                        <td><a class="modalbtn" type="button" data-bs-toggle="modal"
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)} data-priceforpay="${encodeURIComponent(item.price_for_pay)}"  data-bs-target="#exampleModal"><span class="badge rounded-pill text-bg-danger">${item.payment.payment_status}</span></a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  class="" href="/org/1/tp/${tpID}/contractor/${item.contractor.id}/">${item.contractor.name}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${item.own.number}</a></td>
                        <td><a  class="modalbtn btn btn-primary" type="button" data-bs-toggle="modal"
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)} data-priceforpay="${encodeURIComponent(item.price_for_pay)}"  data-bs-target="#exampleModal">Оплатить</a></td></tr>`
                    } else if (item.status.trim() === 'В работе'.trim() && item.payment.payment_status.trim() != 'Не оплачено'.trim()) {
                        body.innerHTML += `<tr class="orderRow"><td><a style="text-decoration: none; color: #696d74;"   href="/org/1/tp/${tpID}/order/${item.id}/">${item.id}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${today}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/"></a></td>
                        <td><span class="badge rounded-pill text-bg-primary">${item.status}</span></td>
                        <td><a  class="modalbtn" type="button"
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)}  data-bs-target="#exampleModal">
                        <span class="badge rounded-pill text-bg-success">${item.payment.payment_status}</span></a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  class="" href="/org/1/tp/${tpID}/contractor/${item.contractor.id}/">${item.contractor.name}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${item.own.number}</a></td>
                        <td><a  class="modalbtn btn btn-primary" type="button" 
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)}  data-bs-target="#exampleModal">Оплатить</a></td>

                        </tr>`
                    } else if (item.status.trim() != 'В работе'.trim() && item.payment.payment_status.trim() === 'Не оплачено'.trim()) {
                        body.innerHTML += `<tr class="orderRow"><td><a style="text-decoration: none; color: #696d74;"   href="/org/1/tp/${tpID}/order/${item.id}/">${item.id}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${today}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${finish_day}</a></td>
                        <td><span class="badge rounded-pill text-bg-success">${item.status}</span></td>
                        <td><a  class="modalbtn" type="button" data-bs-toggle="modal"
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)} data-priceforpay="${encodeURIComponent(item.price_for_pay)}"  data-bs-target="#exampleModal">
                        <span class="badge rounded-pill text-bg-danger">${item.payment.payment_status}</span></a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  class="" href="/org/1/tp/${tpID}/contractor/${item.contractor.id}/">${item.contractor.name}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${item.own.number}</a></td>
                        <td><a  class="modalbtn btn btn-primary" type="button" data-bs-toggle="modal"
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)} data-priceforpay="${encodeURIComponent(item.price_for_pay)}"  data-bs-target="#exampleModal">Оплатить</a></td>
                        </tr>`
                    } else {
                        body.innerHTML += `<tr class="orderRow"><td><a style="text-decoration: none; color: #696d74;"   href="/org/1/tp/${tpID}/order/${item.id}/">${item.id}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${today}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${finish_day}</a></td>
                        <td><span class="badge rounded-pill text-bg-success">${item.status}</span></td>
                        <td><a  class="modalbtn" type="button"
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)}  data-bs-target="#exampleModal">
                        <span class="badge rounded-pill text-bg-success">${item.payment.payment_status}</span></a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  class="" href="/org/1/tp/${tpID}/contractor/${item.contractor.id}/">${item.contractor.name}</a></td>
                        <td><a style="text-decoration: none; color: #696d74;"  href="/org/1/tp/${tpID}/order/${item.id}/">${item.own.number}</a></td>
                        <td><a  class="modalbtn btn btn-primary" type="button" 
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)}  data-bs-target="#exampleModal">Оплатить</a></td>
                        </tr>`
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
                console.log(data);
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


$(function () {
    var idClicked
    $('.modalbtn').click(
        function (e) {
            e.preventDefault()
            var idorderclass = decodeURIComponent($(this).attr('data-idorderclass'));
            var dayorder = decodeURIComponent($(this).attr('data-dayorder'));
            var statusorder = decodeURIComponent($(this).attr('data-statusorder'));
            var priceforpay = decodeURIComponent($(this).attr('data-priceforpay'));
            if (statusorder == 'Завершен') {
                $(".statusorder").html(`<p><strong>Статус</strong>: <span class="badge rounded-pill text-bg-success">${statusorder}</span>`);
            } else if (statusorder == 'В работе') {
                $(".statusorder").html(`<p><strong>Статус</strong>: <span class="badge rounded-pill text-bg-primary">${statusorder}</span>`);
            }
            var paymentstatusorder = decodeURIComponent($(this).attr('data-paymentstatusorder'));
            if (paymentstatusorder == 'Оплачено') {
                $(".paymentstatusorder").html(`<p><strong>Статус оплаты</strong>: <span class="badge rounded-pill text-bg-success paystatus" data-paystatus="${paymentstatusorder}"> ${paymentstatusorder}</span></p>`);
                $('.showForm').html(`<div class="alert alert-danger" role="alert">
                Внимание заказ ОПЛАЧЕН, убедитесь что действительно хотите внести изменения!!!
                </div>`)
            } else if (paymentstatusorder == 'Не оплачено') {
                $(".paymentstatusorder").html(`<p><strong>Статус оплаты</strong>: <span class="badge rounded-pill text-bg-danger paystatus" data-paystatus="${paymentstatusorder}"> ${paymentstatusorder}</span> </p>`);
                $('.showForm').html(``)
            }
            var contractororder = decodeURIComponent($(this).attr('data-contractororder'));
            var ownorder = decodeURIComponent($(this).attr('data-ownorder'));
            $(".idorderclass").html(`<p><strong>№</strong>: ${idorderclass} </p>`);
            $(".dayorder").html(`<p><strong>Дата</strong>: ${dayorder}</p>`);
            $(".contractororder").html(`<p><strong>Заказ-наряд</strong>: ${contractororder}</p>`);
            $(".ownorder").html(`<p><strong>Контрактор</strong>:  ${ownorder}</p>`);
            $(".priceforpay").html(`<p class="alert alert-danger" role="alert"><strong>Общая сумма</strong>:  ${priceforpay} тенге</p>`);
            let senId = document.getElementsByClassName('chosenID')
            $('.sendId').html(`<input type="text" value="${idorderclass}" id="chosenID" class="chosenID" name="order_id" hidden >`)
            idClicked = parseInt(idorderclass)
            senId.value = idClicked
            let formAction = document.getElementById('paymentForm')
            formAction.action = `${tpID}/order/${idClicked}/payment/`
            document.payment.action
        })


    $(function () {
        $('#paymentForm').submit(function (e) {
            e.preventDefault();
            e.stopPropagation();
            var data = $(this).serialize();

            $.ajax({
                url: `${locationHost}/org/1/tp/${tpID}/order/${idClicked}/payment/`,
                method: 'post',
                data: data,
                success: (response) => {
                    let error_text = document.querySelector('.error_text')
                    if(response.error){
                        error_text.innerHTML = `<p style="color: red">${response.error}</p>`
                    } else {
                        error_text.innerHTML = ''
                    }
                },
                error: (response) => {
                    console.log(response)
                }
            })

        })
    })

});


let fromDate = document.getElementById('from_date')
let toDate = document.getElementById('to_date')
let orderStatus = document.getElementById('order_status')
let orderPaymentStatus = document.getElementById('payment_status')
let search = document.getElementById('search')

let page = document.getElementById('page');
let limit = document.getElementById('limit');
let back = document.getElementById('back');
let next = document.getElementById('next');

render('', '', '', '', '', 1, 999999)

limit.addEventListener('input', (e) => {
    if (limit.value === '' || limit.value === 0) {
        render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, 999999)
    }
    render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})

next.addEventListener('click', (e) => {
    page.value = parseInt(page.value) + 1
    render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})

back.addEventListener('click', (e) => {
    page.value = parseInt(page.value) - 1
    render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})

search.addEventListener('input', (e) => {
    render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})
fromDate.addEventListener('change', (e) => {
    if (fromDate.value != '' && toDate.value != '') {
        render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
    }
})

toDate.addEventListener('change', (e) => {
    if (fromDate.value != '' && toDate.value != '') {
        render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
    }
})

orderStatus.addEventListener('change', (e) => {
    render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})

orderPaymentStatus.addEventListener('change', (e) => {
    render(search.value, fromDate.value, toDate.value, orderStatus.value, orderPaymentStatus.value, page.value, limit.value)
})


window.onload = e => {
    let orderStatusSocket;

    if (DEBUG === true) {
        orderStatusSocket = new WebSocket(`ws://${window.location.host}/order/status/update/tracking/`);
    }
    else {
        orderStatusSocket = new WebSocket(`wss://${window.location.host}/order/status/update/tracking/`);
    }

    orderStatusSocket.onmessage = e => {
        let data = JSON.parse(e.data);
        let orderRows = document.getElementsByClassName('orderRow');

        for (orderRow of orderRows) {
            if (data['payment_status'] !== undefined && data['status'] === undefined) {
                if (eval(orderRow.children[0].innerText) === data['id']) {
                    if (data['payment_status'] === 'Оплачено') {
                        orderRow.children[4].firstChild.firstChild.innerText = 'Оплачено';
                        orderRow.children[4].firstChild.firstChild.classList.remove('text-bg-danger');
                        orderRow.children[4].firstChild.firstChild.classList.add('text-bg-success');
                        orderRow.children[4].firstChild.removeAttribute('data-bs-toggle');
                        orderRow.children[7].firstChild.removeAttribute('data-bs-toggle');
                    }
                }
            }
            else {
                if (eval(orderRow.children[0].innerText) === data['id']) {
                    if (data['status'] === 'Завершен') {
                        orderRow.children[3].firstChild.innerText = 'Завершен';
                        orderRow.children[3].firstChild.firstChild.classList.remove('text-bg-primary');
                        orderRow.children[3].firstChild.firstChild.classList.add('text-bg-success');
                    }
                }
            }
        }
    }
}
