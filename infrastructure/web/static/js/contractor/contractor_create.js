var btnIndividualForm = document.getElementById('individual_form')
var btnEntityForm = document.getElementById('entity_form')
var contractorBankingDetails = document.getElementById('contractor_banking_details')


btnIndividualForm.addEventListener('click', (e) => {
    e.preventDefault();
    contractorBankingDetails.style.display = "none";
})

btnEntityForm.addEventListener('click', (e) => {
    e.preventDefault();
    contractorBankingDetails.style.display = "block";
})
