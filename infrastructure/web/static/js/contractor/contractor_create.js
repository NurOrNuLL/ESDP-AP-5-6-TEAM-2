var individualBtn = document.getElementById('individualBtn')
var entityBtn = document.getElementById('entityBtn')
var contractorBankingDetails = document.getElementById('contractor_banking_details')
var contractorIIC = document.getElementById('contractor_IIC')
var contractorBankName = document.getElementById('contractor_bank_name')
var contractorBIC = document.getElementById('contractor_BIC')


individualBtn.addEventListener('click', (e) => {
    individualBtn.checked = true;
    entityBtn.checked = false;

    contractorBankingDetails.classList.add('d-none');
    contractorIIC.value = '';
    contractorBankName.value = '';
    contractorBIC.value = '';
})

entityBtn.addEventListener('click', (e) => {
    entityBtn.checked = true;
    individualBtn.checked = false;

    contractorBankingDetails.classList.remove('d-none');
})
