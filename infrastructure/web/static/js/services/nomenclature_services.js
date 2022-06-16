let select = document.getElementById('nomenclature');
let beforeTableBlock = document.getElementById('beforeTable');

function render(nomenclature, search, category, mark, page, limit) {
    $.ajax({
        url: `http://127.0.0.1:8000/org/1/tp/${tpID}/nomenclature/${nomenclature}/services/filter?search=${search}&category=${category}&mark=${mark}&page=${page}&limit=${limit}`,
        method: 'get',
        success: (data) => {
            body.innerHTML = '';
            if (data.services.length != 0) {
                beforeTableBlock.innerHTML = '';
                data.services.forEach(function (item, i, arr) {
                    if (item.Примечание) {
                        body.innerHTML += '<tr><td>' + item.Название + '</td><td>'
                        + item.Категория + '</td><td>' + item.Примечание + '</td><td>'
                        + item.Марка + '</td><td><b>' + item.Цена + '</b></td></tr>'
                    }
                    else {
                        body.innerHTML += '<tr><td>' + item.Название + '</td><td>'
                        + item.Категория + '</td><td>' + '-' + '</td><td>'
                        + item.Марка + '</td><td><b>' + item.Цена + '</b></td></tr>'
                    }
                })

                if (data.page_number === 1) {
                    next.classList.add('disabled')
                    back.classList.add('disabled')
                } else if (parseInt(page) === data.page_number) {
                    next.classList.add('disabled')
                    back.classList.remove('disabled')
                } else if (parseInt(page) === 1) {
                    back.classList.add('disabled')
                    next.classList.remove('disabled')
                } else {
                    next.classList.remove('disabled')
                    back.classList.remove('disabled')
                }
            }
            else {
                beforeTableBlock.innerHTML = '';
                beforeTableBlock.innerHTML += '<h4 class="text-center">Ничего не найдено!</h4>';
            }
        },
        error: (response) => {
            console.log(response)
            body.innerHTML = '';
            beforeTableBlock.innerHTML = '';
            beforeTableBlock.innerHTML += '<h4 class="text-center">Ничего не найдено!</h4>';
        }
    })
}

let value = select.value
let category = document.getElementById('category')
let mark = document.getElementById('mark')
let search = document.getElementById('search')

let page = document.getElementById('page');
let limit = document.getElementById('limit');
let back = document.getElementById('back');
let next = document.getElementById('next');

limit.addEventListener('input', (e) => {
    if (limit.value === '' || limit.value === 0) {
        render(value, search.value, category.value, mark.value, page.value, 999999)
    }
    render(value, search.value, category.value, mark.value, page.value, limit.value)
})

next.addEventListener('click', (e) => {
    page.value = parseInt(page.value) + 1
    render(value, search.value, category.value, mark.value, page.value, limit.value)
})

back.addEventListener('click', (e) => {
    page.value = parseInt(page.value) - 1
    render(value, search.value, category.value, mark.value, page.value, limit.value)
})

render(value, '', '', '', 1, 999999)

search.addEventListener('input', (e) => {
    render(value, search.value, category.value, mark.value, page.value, limit.value)
})

category.addEventListener('change', (e) => {
    render(value, search.value, category.value, mark.value, page.value, limit.value)
})

mark.addEventListener('change', (e) => {
    render(value, search.value, category.value, mark.value, page.value, limit.value)
})

select.addEventListener('change', function () {
    value = select.value
    if (limit.value === '' || limit.value === 0) {
        render(value, search.value, category.value, mark.value, page.value, 999999)
    }
    render(value, search.value, category.value, mark.value, page.value, limit.value)
})
