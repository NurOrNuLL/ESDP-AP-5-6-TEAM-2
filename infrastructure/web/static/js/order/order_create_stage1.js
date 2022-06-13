let contractor = document.getElementById('contractor');
let own = document.getElementById('own')

contractor.addEventListener('change', (e) => {
    own.innerHTML = ''

    $.ajax({
        url: `http://127.0.0.1:8000/org/1/tp/${tpID}/contractor/${contractor.value}/own/?contrID=${contractor.value}`,
        method: 'get',
        success: (data) => {
            if (own.attributes.getNamedItem('disabled')) {
                own.attributes.removeNamedItem('disabled')
            }
            data.forEach(element => {
                own.innerHTML += `<option value="${element.id}">${element.name}</option>`
            });
        },
        error: (response) => {
            console.log(response)
        }
    })
})
