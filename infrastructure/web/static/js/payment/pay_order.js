// При выборе метода оплаты выводятся поля соответствующих данных для заполнения
const selectElement = document.querySelector('.method');

selectElement.addEventListener('change', (event) => {
    if (parseInt(event.target.value) == 1) {
        const cash = document.querySelector('.pay_method')
        const btn = document.querySelector('.submit_button_form')
        btn.innerHTML = ''
        btn.innerHTML = `<input type="submit" value="Оплатить" id="submitIfOk" class="btn btn-primary submitValues"
                               onclick="stringLengthCheck(document.payment.details_cash, 0, 100)">`
        cash.innerHTML = ''
        cash.innerHTML = `
                                    <textarea cols=5 rows=3 type="text" class="form-control border-secondary details_cash" id="details_cash" name='details_cash' hidden></textarea>
                                    <input type="text" class="form-control border-secondary" id="details_cashless" name='details_cashless' value="" hidden>
                                    <input type="text" class="form-control border-secondary" id="details_kaspi" name='details_kaspi' value="" hidden>
                                    <input type="text" class="form-control border-secondary" id="consignment" name='consignment' value="" hidden>
                                    <input type="text" class="form-control border-secondary" id="invoice" name='invoice' value="" hidden>`


    } else if (parseInt(event.target.value) == 2) {
        const cash = document.querySelector('.pay_method')
        const btn = document.querySelector('.submit_button_form')
        btn.innerHTML = ''
        btn.innerHTML = `<input type="submit" value="Оплатить" id="submitIfOk" class="btn btn-primary submitValues" onclick="stringLengthCheckSecond(document.payment.consignment, document.payment.invoice, 0, 100)">`

        cash.innerHTML = ''
        cash.innerHTML = `
                                    <input type="text" class="form-control border-secondary" id="details_cash" name='details_cash' value="" hidden>
                                    <input type="text" class="form-control border-secondary" id="details_cashless" name='details_cashless' value="" hidden>

                                    <input type="text" class="form-control border-secondary" id="details_kaspi" name='details_kaspi' value="" hidden>
                                    <label for="consignment" class="form-label">Накладное</label><br>
                                    <textarea cols=5 rows=3  type="text" class="form-control border-secondary" id="consignment" name='consignment'></textarea>
                                    <label for="invoice" class="form-label">Счет фактура</label><br>
                                    <textarea cols=5 rows=3  type="text" class="form-control border-secondary" id="invoice" name='invoice' ></textarea>`

    } else if (parseInt(event.target.value) == 3) {
        const cash = document.querySelector('.pay_method')
        const btn = document.querySelector('.submit_button_form')
        btn.innerHTML = ''
        btn.innerHTML = `<input type="submit" value="Оплатить" id="submitIfOk" class="btn btn-primary submitValues"
                               onclick="stringLengthCheck(document.payment.details_kaspi, 0, 50)">`
        cash.innerHTML = ''
        cash.innerHTML = `
                                    <input type="text" class="form-control border-secondary" id="details_cash" name='details_cash' value="" hidden>
                                    <input type="text" class="form-control border-secondary" id="details_cashless" name='details_cashless' value="" hidden>

                                    <div class="form-check">
                                    <input class="form-check-input" type="radio" name="details_kaspi" id="details_kaspiQR" value="Kaspi QR">
                                    <label class="form-check-label" for="details_kaspiQR">
                                    Kaspi QR
                                    </label>
                                    </div>
                                    <div class="form-check">
                                    <input class="form-check-input" type="radio" name="details_kaspi" id="details_kaspiTransfer" value="Kaspi Перевод">
                                    <label class="form-check-label" for="details_kaspiTransfer">
                                    Kaspi Перевод
                                    </label>
                                    </div>
                                    <div class="form-check">
                                    <input class="form-check-input" type="radio" name="details_kaspi" id="details_kaspiRed" value="Kaspi RED">
                                    <label class="form-check-label" for="details_kaspiRed">
                                    Kaspi RED
                                    </label>
                                    </div>

                                    <input type="text" class="form-control border-secondary" id="consignment" name='consignment' value="" hidden>
                                    <input type="text" class="form-control border-secondary" id="invoice" name='invoice' value="" hidden>`

    } else if (event.target.value == '') {
        const cash = document.querySelector('.pay_method')
        const btn = document.querySelector('.submit_button_form')
        btn.innerHTML = ''
        cash.innerHTML = ''
        cash.innerHTML = `
                                    <input type="text" class="form-control border-secondary" id="details_cash" name='details_cash' value="" hidden>
                                    <input type="text" class="form-control border-secondary" id="details_cashless" name='details_cashless' value="" hidden>

                                    <textarea cols=5 rows=3 type="text" class="form-control border-secondary" id="details_kaspi" name='details_kaspi' hidden></textarea>
                                    <input type="text" class="form-control border-secondary" id="consignment" name='consignment' value="" hidden>
                                    <input type="text" class="form-control border-secondary" id="invoice" name='invoice' value="" hidden>`
    }
});


// Функция для валидации данных при наличным и каспи способом
function stringLengthCheck(name, minlength, maxlength) {
    var mnlen = minlength;
    var mxlen = maxlength;

    if (name.value.length < mnlen || name.value.length > mxlen) {
        let error_text = document.querySelector('.error_text')
        error_text.innerHTML = `<div class="alert alert-danger d-flex align-items-center pt-1 pb-1 pe-4 ps-4 m-0"
                                     role="alert">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor"
                                         class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2" viewBox="0 0 16 16"
                                         role="img"
                                         aria-label="Warning:">
                                        <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                                    </svg>
                                    <div>
                                        Описание ${name.value} не должно превышать ${mxlen} символов
                                    </div>
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"
                                            aria-label="Close"></button>
                                </div>`
        name.value = ''
        return false;

    } else {
        name.value
        let error_text = document.querySelector('.error_text')
        error_text.innerHTML = ''
        error_text.innerHTML = `<div class="alert alert-success" role="alert">
                                                                Описание ${name.value} принято, нажмите отправить повторно
                                                            </div>`
        let submit = document.querySelector('#submitIfOk')
        console.log(submit)

        submit.addEventListener('click', (event) => {
            submit.dataset.dismiss = 'modal'
            window.location.replace(`${locationHost}/org/1/tp/${tpID}/`)
        })
        return true

    }
}

// Функция для валидации данных при безналичным способом
function stringLengthCheckSecond(name1, name2, minlength, maxlength) {
    var mnlen = minlength;
    var mxlen = maxlength;

    if (name1.value.length < mnlen || name1.value.length > mxlen || name2.value.length < mnlen || name2.value.length > mxlen) {
        let error_text = document.querySelector('.error_text')
        error_text.innerHTML = `<div class="alert alert-danger d-flex align-items-center pt-1 pb-1 pe-4 ps-4 m-0"
                                     role="alert">
                                    <svg xmlns="http://www.w3.org/2000/svg" width="15" height="15" fill="currentColor"
                                         class="bi bi-exclamation-triangle-fill flex-shrink-0 me-2" viewBox="0 0 16 16"
                                         role="img"
                                         aria-label="Warning:">
                                        <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                                    </svg>
                                    <div>
                                        <p>Проверьте описание Накладное: ${name1.value}</p>

                                        <p>Проверьте описание Счет Фактура: ${name2.value}</p>
                                        <p>Описание не должно превышать ${mxlen} символов</p>


                                    </div>
                                    <button type="button" class="btn-close" data-bs-dismiss="alert"
                                            aria-label="Close"></button>
                                </div>`
        name1.value = ''
        name2.value = ''
        return false;

    } else {
        name1.value
        name2.value
        let error_text = document.querySelector('.error_text')
        error_text.innerHTML = ''
        error_text.innerHTML = `<div class="alert alert-success" role="alert">
                                                                Описание ${name1.value}, ${name2.value} принято, нажмите отправить повторно
                                                            </div>`
        let submit = document.querySelector('#submitIfOk')


        submit.addEventListener('click', (event) => {
            submit.dataset.dismiss = 'modal'
            window.location.replace(`${locationHost}/org/1/tp/${tpID}/`)
        })
        return true

    }
}

// Закрытие модального окна кнопкой X и обновление страницы с актуальными данными после изменения

let submit = document.querySelector('.close_modal')

submit.addEventListener('click', (event) => {
    submit.dataset.dismiss = 'modal'
    window.location.replace(`${locationHost}/org/1/tp/${tpID}/`)
})

// Закрытие модального окна Оплаты при нажатии кнопки Закрыть
let second_submit = document.querySelector('.close_modal_second')
second_submit.addEventListener('click', (event) => {
    window.location.replace(`${locationHost}/org/1/tp/${tpID}/`)
})