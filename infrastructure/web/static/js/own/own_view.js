let body = document.getElementById('body');
let emptyBody = document.getElementById('emptyBody');
let next = document.getElementById('next');
let back = document.getElementById('back');
let page = document.getElementById('page');
let search = document.getElementById('ownSearch');
let isPart = document.getElementById('isPart');

$.ajax({
    url: `http://127.0.0.1:8000/org/1/tp/${tpID}/own/list/filter/?search=&is_part=${isPart.value}`,
    method: 'GET',
    success: (data) => {
        if (data.next && data.previous === null) {
            next.classList.remove('disabled')
            back.classList.add('disabled')
        }
        else if (data.previous && data.next === null) {
            next.classList.add('disabled')
            back.classList.remove('disabled')
        }
        else if (data.next === null && data.previous === null) {
            next.classList.add('disabled')
            back.classList.add('disabled')
        }
        else {
            next.classList.remove('disabled')
            back.classList.remove('disabled')
        }

        data.results.forEach(function (item) {
            console.log(item);
            if (item.comment == null) {
                item.comment = '';
            }
            body.innerHTML += '<tr><td>' + item.name + '</td><td>' + item.number + '</td><td>' + item.comment + '</td><td><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/contractor/' + item.contractor + '/">Детали</a></td></tr>'
        })
    },
    error: (response) => {
        console.log(response)
    }
})


back.addEventListener('click', (e) => {
    page.value = parseInt(page.value) - 1
  $.ajax({
    url: `http://127.0.0.1:8000/org/1/own/list/filter/?page=${page.value}&search=${search.value}&is_part=${isPart.value}`,
    method: 'GET',
    success: (data) => {
        body.innerText = ""

        if (data.next && data.previous === null) {
            next.classList.remove('disabled')
            back.classList.add('disabled')
        }
        else if (data.previous && data.next === null) {
            next.classList.add('disabled')
            back.classList.remove('disabled')
        }
        else if (data.next === null && data.previous === null) {
            next.classList.add('disabled')
            back.classList.add('disabled')
        }
        else {
            next.classList.remove('disabled')
            back.classList.remove('disabled')
        }

        data.results.forEach(function (item) {
            body.innerHTML += '<tr><td>' + item.name + '</td><td>' + item.number + '</td><td>' + item.comment + '</td><td><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/contractor/' + item.contractor + '/">Детали контрагента</a></td></tr>'
        })
    },
    error: (response) => {
        console.log(response)
    }
})
})


next.addEventListener('click', (e) => {
    page.value = parseInt(page.value) + 1
  $.ajax({
    url: `http://127.0.0.1:8000/org/1/tp/${tpID}/own/list/filter/?page=${page.value}&search=${search.value}&is_part=${isPart.value}`,
    method: 'GET',
    success: (data) => {
        body.innerText = ""

        if (data.next && data.previous === null) {
            next.classList.remove('disabled')
            back.classList.add('disabled')
        }
        else if (data.previous && data.next === null) {
            next.classList.add('disabled')
            back.classList.remove('disabled')
        }
        else if (data.next === null && data.previous === null) {
            next.classList.add('disabled')
            back.classList.add('disabled')
        }
        else {
            next.classList.remove('disabled')
            back.classList.remove('disabled')
        }

        data.results.forEach(function (item) {
            body.innerHTML += '<tr><td>' + item.name + '</td><td>' + item.number + '</td><td>' + item.comment + '</td><td><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/contractor/' + item.contractor + '/">Детали контрагента</a></td></tr>'
        })
    },
    error: (response) => {
        console.log(response)
    }
})
})

search.addEventListener('input', (e) => {
      $.ajax({
        url: `http://127.0.0.1:8000/org/1/tp/${tpID}/own/list/filter/?search=${search.value}&is_part=${isPart.value}`,
        method: 'GET',
        success: (data) => {
            body.innerHTML = '';
            emptyBody.innerHTML = '';
            if (data.next && data.previous === null) {
                next.classList.remove('disabled')
                back.classList.add('disabled')
            }
            else if (data.previous && data.next === null) {
                next.classList.add('disabled')
                back.classList.remove('disabled')
            }
            else if (data.next === null && data.previous === null) {
                next.classList.add('disabled')
                back.classList.add('disabled')
            }
            else {
                next.classList.remove('disabled')
                back.classList.remove('disabled')
            }

            if(data.results.length) {
                data.results.forEach(function (item) {
                    body.innerHTML += '<tr><td>' + item.name + '</td><td>' + item.number + '</td><td>' + item.comment + '</td><td><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/contractor/' + item.contractor + '/">Детали контрагента</a></td></tr>'
                })
            }
            else {
                body.innerHTML = '';
                emptyBody.innerHTML = '';
                emptyBody.innerHTML += '<h4 class="text-center" >Ничего не найдено!</h4>';
            }
        },
        error: (response) => {
            console.log(response);
        }
        })
})

isPart.addEventListener('change', () => {
    $.ajax({
        url: `http://127.0.0.1:8000/org/1/tp/${tpID}/own/list/filter/?search=${search.value}&is_part=${isPart.value}`,
        method: 'GET',
        success: (data) => {
            body.innerHTML = '';
            emptyBody.innerHTML = '';
            if (data.next && data.previous === null) {
                next.classList.remove('disabled')
                back.classList.add('disabled')
            }
            else if (data.previous && data.next === null) {
                next.classList.add('disabled')
                back.classList.remove('disabled')
            }
            else if (data.next === null && data.previous === null) {
                next.classList.add('disabled')
                back.classList.add('disabled')
            }
            else {
                next.classList.remove('disabled')
                back.classList.remove('disabled')
            }

            if(data.results.length) {
                data.results.forEach(function (item) {
                    body.innerHTML += '<tr><td>' + item.name + '</td><td>' + item.number + '</td><td>' + item.comment + '</td><td><a class="btn btn-secondary" href="/org/1/tp/' + tpID + '/contractor/' + item.contractor + '/">Детали контрагента</a></td></tr>'
                })
            }
            else {
                body.innerHTML = '';
                emptyBody.innerHTML = '';
                emptyBody.innerHTML += '<h4 class="text-center" >Ничего не найдено!</h4>';
            }
        },
        error: (response) => {
            console.log(response);
        }
        })
})
