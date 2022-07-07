$(function () {
    $('.modalbtn2').click(
        function (e) {
            e.preventDefault()
            var idorderclass = $(this).attr('data-idorderclass');
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
            $(".priceforpay").html(`<p class="alert alert-warning" role="alert" style="width: 730px;"><strong>Общая сумма</strong>:  ${priceforpay} тенге</p>`);
            let senId = document.getElementsByClassName('chosenID')
            $('.sendId').html(`<input type="text" value="${idorderclass}" id="chosenID" class="chosenID" name="order_id" hidden >`)
            idClicked = parseInt(idorderclass)
            senId.value = idClicked
        })


    $(function () {
        $('#paymentForm2').submit(function (e) {
            e.preventDefault();
            e.stopPropagation();
            var data = $(this).serialize();
            var payd_data = $(this).serializeArray()

            $.ajax({
                url: `${locationHost}/org/1/tp/${tpID}/order/${idClicked}/payment/`,
                method: 'post',
                data: data,
                success: (response) => {
                    let error_text = document.querySelector('.error_text')
                    if (response.error) {
                        error_text.innerHTML = `<p style="color: red">${response.error}</p>`
                    } else {
                        error_text.innerHTML = ''
                        let submit = document.querySelector('.close_modal')
                        let detail_status = document.querySelector('#detail_status');
                        let detail_button = document.querySelector('#detail_button');
                        let id_method = document.querySelector('#id_method');
                        let detail_method = document.querySelector('#detail_method');
                        let details = document.querySelector('#details');

                        if (id_method.value === '1') {
                            detail_method.innerHTML = ''
                            detail_method.innerHTML = 'Наличный'
                            details.innerHTML = ''
                        } else if (id_method.value === '2') {
                            detail_method.innerHTML = ''
                            detail_method.innerHTML = 'Безналичный'
                            details.innerHTML = ''
                            details.innerHTML = `<br> Накладная # ${payd_data[4].value} <br>\
                                                                 Счет фактура # ${payd_data[5].value}`
                        } else if (id_method.value === '3') {
                            detail_method.innerHTML = ''
                            detail_method.innerHTML = 'Kaspi'
                            details.innerHTML = ''
                            details.innerHTML = `${payd_data[3].value}`
                        }
                        console.log(id_method.value)
                        detail_status.innerHTML = ''
                        detail_status.innerHTML = 'Оплачено'
                        detail_button.remove()
                        submit.click();
                    }
                },
                error: (response) => {
                    console.log(response)
                }
            })

        })
    })
});