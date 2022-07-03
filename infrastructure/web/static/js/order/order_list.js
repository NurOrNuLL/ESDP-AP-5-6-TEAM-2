let beforeTableBlock = document.getElementById('beforeTable');

function render(search, date, status, payment_status, page, limit) {
    $.ajax({
        url: `${locationHost}/org/1/tp/${tpID}/order/list/filter?search=${search}&date=${date}&status=${status}&payment_status=${payment_status}&page=${page}&limit=${limit}`,
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
                    var min = String(today.getMinutes())
                    today = dd + '.' + mm + '.' + yyyy + ' ' + hh + ':' + min;

                    if (item.status.trim() === 'В работе'.trim() && item.payment.payment_status.trim() === 'Не оплачено'.trim()) {
                        body.innerHTML += `<tr data-id="${item.id}"><td><a class="btn rounded-pill btn-secondary" href="/org/1/tp/${tpID}/order/${item.id}/">${item.id}</a></td><td>${today}</td>
                        <td><span class="badge rounded-pill text-bg-primary">${item.status}</span></td>
                        <td><a  class="modalbtn" type="button" data-bs-toggle="modal"
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)}  data-bs-target="#exampleModal"><span class="badge rounded-pill text-bg-danger">${item.payment.payment_status}</span></a></td>
                        <td><a class="" href="/org/1/tp/${tpID}/contractor/${item.contractor.id}/">${item.contractor.name}</a></td><td>${item.own.number}</td></tr>`
                    } else if (item.status.trim() === 'В работе'.trim() && item.payment.payment_status.trim() != 'Не оплачено'.trim()) {
                        body.innerHTML += `<tr><td><a class="btn rounded-pill btn-secondary" href="/org/1/tp/${tpID}/order/${item.id}/">${item.id}</a></td><td>${today}</td>
                        <td><span class="badge rounded-pill text-bg-primary">${item.status}</span></td>
                        <td><a  class="modalbtn" type="button"
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)}  data-bs-target="#exampleModal">
                        <span class="badge rounded-pill text-bg-success">${item.payment.payment_status}</span></a></td>
                        <td><a class="" href="/org/1/tp/${tpID}/contractor/${item.contractor.id}/">${item.contractor.name}</a></td><td>${item.own.number}</td>
                        <td class="d-flex justify-content-end"></tr>`
                    } else if (item.status.trim() != 'В работе'.trim() && item.payment.payment_status.trim() === 'Не оплачено'.trim()) {
                        body.innerHTML += `<tr><td><a class="btn rounded-pill btn-secondary" href="/org/1/tp/${tpID}/order/${item.id}/">${item.id}</a></td><td>${today}</td>
                        <td><span class="badge rounded-pill text-bg-success">${item.status}</span></td>
                        <td><a  class="modalbtn" type="button" data-bs-toggle="modal"  
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)}  data-bs-target="#exampleModal">
                        <span class="badge rounded-pill text-bg-danger">${item.payment.payment_status}</span></a></td>
                        <td><a class="" href="/org/1/tp/${tpID}/contractor/${item.contractor.id}/">${item.contractor.name}</a></td><td>${item.own.number}</td>
                        <td class="d-flex justify-content-end"></tr>`
                    } else {
                        body.innerHTML += `<tr><td><a class="btn rounded-pill btn-secondary" href="/org/1/tp/${tpID}/order/${item.id}/">${item.id}</a>
                        </td><td>${today}</td>
                        <td><span class="badge rounded-pill text-bg-success">${item.status}</span></td>
                        <td><a  class="modalbtn" type="button"  
                        data-idorderclass=${encodeURIComponent(item.id)}
                        data-dayorder=${encodeURIComponent(today)}
                        data-statusorder=${encodeURIComponent(item.status)}
                        data-paymentstatusorder=${encodeURIComponent(item.payment.payment_status)}
                        data-contractororder=${encodeURIComponent(item.contractor.name)}
                        data-ownorder=${encodeURIComponent(item.own.number)}  data-bs-target="#exampleModal">
                        <span class="badge rounded-pill text-bg-success">${item.payment.payment_status}</span></a></td>
                        <td><a class="" href="/org/1/tp/${tpID}/contractor/${item.contractor.id}/">${item.contractor.name}</a></td><td>${item.own.number}</td>
                        <td class="d-flex justify-content-end"></tr>`
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
            $(".idorderclass").html(`<p><strong>ID</strong>: ${idorderclass} </p>`);
            $(".dayorder").html(`<p><strong>Дата</strong>: ${dayorder}</p>`);
            $(".contractororder").html(`<p><strong>Заказ-наряд</strong>: ${contractororder}</p>`);
            $(".ownorder").html(`<p><strong>Контрактор</strong>:  ${ownorder}</p>`);
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
                },
                error: (response) => {
                    console.log(response)
                }
            })

        })
    })

});


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
