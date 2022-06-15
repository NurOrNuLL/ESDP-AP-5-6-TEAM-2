var btnPartForm = document.getElementById('part_form');
var btnAutoForm = document.getElementById('auto_form');
var labelOwnName = document.getElementById('own_name_label');
var inputOwnType = document.getElementById('own_is_part');
var FieldOwnNumber = document.getElementById('number_field');


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
        FieldOwnNumber.style.display = "none";
        inputOwnType.value = 'True';
        localStorage.setItem('picked_part', 'btn-secondary');
        localStorage.removeItem('picked_auto');
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
        FieldOwnNumber.style.display = "block";
        inputOwnType.value = 'False';
        localStorage.setItem('picked_auto', 'btn-secondary');
        localStorage.removeItem('picked_part');
    }
})

function onLoad() {
    if (localStorage.getItem('picked_auto')) {
        FieldOwnNumber.style.display = "block";
    }
    else {
        FieldOwnNumber.style.display = "none";
    }
    if(localStorage.getItem('picked_part') === 'btn-secondary') {
            btnPartForm.classList.remove('btn-light');
            btnPartForm.classList.add('btn-secondary');
        }
    else if(localStorage.getItem('picked_auto') === 'btn-secondary') {
        btnAutoForm.classList.remove('btn-light');
        btnAutoForm.classList.add('btn-secondary');
    }
}

window.addEventListener('load', onLoad);