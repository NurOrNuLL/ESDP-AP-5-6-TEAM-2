var btnIndividualForm = document.getElementById('individual_form')
var btnEntityForm = document.getElementById('entity_form')
var contractorBankingDetails = document.getElementById('contractor_banking_details')
var contractorIIC = document.getElementById('contractor_IIC')
var contractorBankName = document.getElementById('contractor_bank_name')
var contractorBIC = document.getElementById('contractor_BIC')


btnIndividualForm.addEventListener('click', (e) => {
    e.preventDefault();
    contractorBankingDetails.style.display = "none";
    contractorIIC.value = '';
    contractorBankName.value = '';
    contractorBIC.value = '';
})

btnEntityForm.addEventListener('click', (e) => {
    e.preventDefault();
    contractorBankingDetails.style.display = "block";
})

function onLoad() {
    if (contractorIIC.value || contractorBankName.value || contractorBIC.value) {
        contractorBankingDetails.style.display = "block";
    }
    else {
        contractorBankingDetails.style.display = "none";
    }
}

window.addEventListener('load', onLoad);
