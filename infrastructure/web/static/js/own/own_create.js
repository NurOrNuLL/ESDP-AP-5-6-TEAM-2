var btnPartForm = document.getElementById('part_form');
var btnAutoForm = document.getElementById('auto_form');
var labelOwnName = document.getElementById('own_name_label');
var labelOwnNumber = document.getElementById('own_number_label');
var selectAuto = document.getElementById('type_auto');
var selectPart = document.getElementById('type_part');
var inputOwnType = document.getElementById('own_is_part');

btnPartForm.addEventListener('click', (e) => {
    e.preventDefault();
    if (
        btnPartForm.classList.contains('btn-light')
    ) {
        btnPartForm.classList.remove('btn-light');
        btnPartForm.classList.add('btn-secondary');
        btnAutoForm.classList.remove('btn-secondary');
        btnAutoForm.classList.add('btn-light');
        labelOwnName.innerText = 'Наименование детали:';
        labelOwnNumber.innerText = 'Дополнительная информация::';
        inputOwnType.value = 'True';
          }
})

btnAutoForm.addEventListener('click', (e) => {
    e.preventDefault();
        if (
        btnAutoForm.classList.contains('btn-light')
    ) {
        btnAutoForm.classList.remove('btn-light');
        btnAutoForm.classList.add('btn-secondary');
        btnPartForm.classList.remove('btn-secondary');
        btnPartForm.classList.add('btn-light');
        labelOwnName.innerText = 'Модель автомобиля:';
        labelOwnNumber.innerText = 'Гос. номер:';
        inputOwnType.value = 'False';
    }
})
