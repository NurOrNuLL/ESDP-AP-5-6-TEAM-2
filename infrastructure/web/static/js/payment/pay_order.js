// При выборе метода оплаты выводятся поля соответствующих данных для заполнения
const selectElement = document.querySelector('.method');

selectElement.addEventListener('change', (event) => {
    if (parseInt(event.target.value) == 1) {
        const cash = document.querySelector('.pay_method')
        cash.innerHTML = ''
        cash.innerHTML = `<textarea cols=5 rows=3 type="text" class="form-control border-secondary details_cash" id="details_cash" name='details_cash' hidden></textarea>`

    } else if (parseInt(event.target.value) == 2) {
        const cash = document.querySelector('.pay_method')

        cash.innerHTML = ''
        cash.innerHTML = `
                        <input type="text" class="form-control border-secondary" id="details_cashless" name='details_cashless' hidden>
                        <label for="consignment" class="form-label">Накладное</label><br>
                        <textarea cols=3 rows=2 type="text" class="form-control border-secondary" id="consignment" name='consignment'></textarea>
                        <div id="the-count">
                        <span id="current">0</span>
                        <span id="maximum">/ 100</span>
                        </div>
                        <label for="invoice" class="form-label">Счет фактура</label><br>
                        <textarea cols=3 rows=2  type="text" class="form-control border-secondary" id="invoice" name='invoice' ></textarea>
                        <div id="the-count2">
                        <span id="current2">0</span>
                        <span id="maximum2">/ 100</span>
                        </div>`
        $('#consignment').keyup(function () {

            var characterCount = $(this).val().length,
                current = $('#current'),
                maximum = $('#maximum'),
                theCount = $('#the-count');

            current.text(characterCount);

        });
        $('#invoice').keyup(function () {

            var characterCount2 = $(this).val().length,
                current = $('#current2'),
                maximum = $('#maximum2'),
                theCount = $('#the-count2');

            current.text(characterCount2);

        });


    } else if (parseInt(event.target.value) == 3) {
        const cash = document.querySelector('.pay_method')
        cash.innerHTML = ''
        cash.innerHTML = `
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
                        </div>`

    } else if (event.target.value == '') {
        const cash = document.querySelector('.pay_method')
        const btn = document.querySelector('.submit_button_form')
        btn.innerHTML = ''
        cash.innerHTML = ''
        cash.innerHTML = `
                        <input type="text" class="form-control border-secondary" id="details_cash" name='details_cash' value="" hidden>
                        <input type="text" class="form-control border-secondary" id="details_cashless" name='details_cashless' hidden>
                        <textarea cols=3 rows=2 type="text" class="form-control border-secondary" id="details_kaspi" name='details_kaspi' hidden></textarea>
                        <input type="text" class="form-control border-secondary" id="consignment" name='consignment' hidden>
                        <input type="text" class="form-control border-secondary" id="invoice" name='invoice' hidden>`
    }
});


// Закрытие модального окна кнопкой X и обновление страницы с актуальными данными после изменения

let submit = document.querySelector('.close_modal')

submit.addEventListener('click', (event) => {
    submit.dataset.dismiss = 'modal'
    window.location.replace(`${locationHost}/org/1/tp/${tpID}/`)
})