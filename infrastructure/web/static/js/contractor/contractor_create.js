var individualBtn = document.getElementById('individualBtn')
var entityBtn = document.getElementById('entityBtn')
var contractorBankingDetails = document.getElementById('contractor_banking_details')
var contractorIIC = document.getElementById('contractor_IIC')
var contractorBankName = document.getElementById('contractor_bank_name')
var contractorBIC = document.getElementById('contractor_BIC')
var contractorType = document.getElementById('contractor_type')


individualBtn.addEventListener('click', (e) => {
    individualBtn.checked = true;
    entityBtn.checked = false;
    contractorBankingDetails.classList.add('d-none');
    contractorIIC.value = '';
    contractorBankName.value = '';
    contractorBIC.value = '';
    contractorType.value = 'private';
})

entityBtn.addEventListener('click', (e) => {
    entityBtn.checked = true;
    individualBtn.checked = false;
    contractorBankingDetails.classList.remove('d-none');
    contractorType.value = 'entity';
})

function onLoad() {
    if (contractorType.value === 'private') {
        console.log(contractorType.value);
        individualBtn.checked = true;
        entityBtn.checked = false;
        contractorBankingDetails.classList.add('d-none');
    }
    if (contractorType.value === 'entity') {
        entityBtn.checked = true;
        individualBtn.checked = false;
        contractorBankingDetails.classList.remove('d-none');
    }
}

window.addEventListener('load', onLoad);
