var btnIndividualForm = document.getElementById('individual_form')
var btnEntityForm = document.getElementById('entity_form')
var contractorBankingDetails = document.getElementById('contractor_banking_details')
var contractorIIC = document.getElementById('contractor_IIC')
var contractorBankName = document.getElementById('contractor_bank_name')
var contractorBIC = document.getElementById('contractor_BIC')


btnIndividualForm.addEventListener('click', (e) => {
    e.preventDefault();
    if (
        btnIndividualForm.classList.contains('btn-light')
    ) {
        btnIndividualForm.classList.remove('btn-light');
        btnIndividualForm.classList.add('btn-secondary');
        btnEntityForm.classList.remove('btn-secondary');
        btnEntityForm.classList.add('btn-light');
        localStorage.setItem('picked_individual', 'btn-secondary');
        localStorage.removeItem('picked_entity');
          }

    contractorBankingDetails.style.display = "none";
    contractorIIC.value = '';
    contractorBankName.value = '';
    contractorBIC.value = '';
})

btnEntityForm.addEventListener('click', (e) => {
    e.preventDefault();
        if (
        btnEntityForm.classList.contains('btn-light')
    ) {
        btnEntityForm.classList.remove('btn-light');
        btnEntityForm.classList.add('btn-secondary');
        btnIndividualForm.classList.remove('btn-secondary');
        btnIndividualForm.classList.add('btn-light');
        localStorage.setItem('picked_entity', 'btn-secondary');
        localStorage.removeItem('picked_individual');
    }
    contractorBankingDetails.style.display = "block";
})

function onLoad() {
    if (localStorage.getItem('picked_entity')) {
        contractorBankingDetails.style.display = "block";
    }
    else {
        contractorBankingDetails.style.display = "none";
    }
    if(localStorage.getItem('picked_individual') === 'btn-secondary') {
            btnIndividualForm.classList.remove('btn-light');
            btnIndividualForm.classList.add('btn-secondary');
        }
    else if(localStorage.getItem('picked_entity') === 'btn-secondary') {
        btnEntityForm.classList.remove('btn-light');
        btnEntityForm.classList.add('btn-secondary');
    }
}

window.addEventListener('load', onLoad);
