let body = document.getElementById('body');
let emptyBody = document.getElementById('emptyBody');
let next = document.getElementById('next');
let back = document.getElementById('back');
let page = document.getElementById('page');
let search = document.getElementById('ownSearch');
let isPart = document.getElementById('isPart');
let numberTitle = document.getElementById('numberTitle');
let ownEditBTN = document.getElementById('edit3Button');

function update() {
    $('.button_own').click(
        function (e) {
            e.preventDefault()
            var is_part = $(this).attr('data-ownpart');
            console.log(is_part)
            if (is_part === 'true'){
                let numbers = document.getElementById('own_number_label')
                let numbersin = document.getElementById('number')
                numbers.classList.add('d-none')
                numbersin.classList.add('d-none')
                let id = document.getElementById('id')
                let name = document.getElementById('name')
                let comment = document.getElementById('comment')
                let version = document.getElementById('version')
                id.value = $(this).attr('data-ownid');
                name.value = decodeURIComponent($(this).attr('data-ownname'));
                comment.value = decodeURIComponent($(this).attr('data-owncomment'));
                version.value = $(this).attr('data-ownversion')
            }else if(is_part === 'false'){
                console.log('sdssdsdsds')
                let id = document.getElementById('id')
                let name = document.getElementById('name')
                let numbers = document.getElementById('own_number_label')
                numbers.classList.remove('d-none')
                let numbersin = document.getElementById('number')
                numbersin.classList.remove('d-none')
                let number = document.getElementById('number')
                let comment = document.getElementById('comment')
                let version = document.getElementById('version')
                id.value = $(this).attr('data-ownid');
                name.value = decodeURIComponent($(this).attr('data-ownname'));
                number.value = $(this).attr('data-ownnumber');
                comment.value = decodeURIComponent($(this).attr('data-owncomment'));
                version.value = $(this).attr('data-ownversion')
            }else{
                let id = document.getElementById('id')
                let name = document.getElementById('name')
                let number = document.getElementById('number')
                let comment = document.getElementById('comment')
                let version = document.getElementById('version')
                id.value = $(this).attr('data-ownid');
                name.value = decodeURIComponent($(this).attr('data-ownname'));
                number.value = $(this).attr('data-ownnumber');
                comment.value = decodeURIComponent($(this).attr('data-owncomment'));
                version.value = $(this).attr('data-ownversion')
            }
            ownEditBTN.onclick = e => {
                e.preventDefault();
                let id = document.getElementById('id').value
                let name = document.getElementById('name').value;
                let number = document.getElementById('number').value;
                let comment = document.getElementById('comment').value;
                let version = document.getElementById('version').value;
                let closeBtn = document.getElementById('closeBtn');
                let concurrencyBtn = document.getElementById('concurrencyBtn');
                let concurrencyHeader = document.getElementById('concurrencyHeader');
                let oldData = document.getElementById('old');
                let oldData1 = document.getElementById('old1');
                let oldData2 = document.getElementById('old2');
                let newData = document.getElementById('new');
                let newData1 = document.getElementById('new1');
                let newData2 = document.getElementById('new2');

                $.ajax({
                    url: `${locationHost}/org/1/tp/${tpID}/own/${id}/update/`,
                    method: 'patch',
                    headers: {'X-CSRFToken': $.cookie('csrftoken')},
                    data: JSON.stringify({
                        'name': name,
                        'number': number,
                        'comment': comment,
                        'version': version
                    }),
                    dataType: 'json',
                    contentType: 'application/json',
                    success: function (data) {
                        if (data['error'] === undefined) {
                            name.innerText = data['name']
                            number.innerText = data['number']
                            comment.innerText = data['comment']
                            window.location.reload()
                        } else {
                            concurrencyBtn.click();

                            concurrencyHeader.innerText = data['error'];
                            oldData.innerText = data['current_data']['name'];
                            oldData1.innerText = data['current_data']['number'];
                            oldData2.innerText = data['current_data']['comment'];
                            newData.innerText = data['new_data']['name'];
                            newData1.innerText = data['new_data']['number'];
                            newData2.innerText = data['new_data']['comment'];
                            if (oldData.innerText === newData.innerText) {
                                oldData.style.color = 'black';
                                newData.style.color = 'black';
                            } else {
                                oldData.style.color = 'red';
                                newData.style.color = 'green';
                            }
                            if (oldData1.innerText === newData1.innerText) {
                                oldData1.style.color = 'black';
                                newData1.style.color = 'black';
                            } else {
                                oldData1.style.color = 'red';
                                newData1.style.color = 'green';
                            }
                            if (oldData2.innerText === newData2.innerText) {
                                oldData2.style.color = 'black';
                                newData2.style.color = 'black';
                            } else {
                                oldData2.style.color = 'red';
                                newData2.style.color = 'green';
                            }
                            let updateBtn = document.getElementById('updateBtn');
                            let closeBtn = document.getElementById('closeBtn');
                            let closeBtn2 = document.getElementById('closeBtn2');

                            updateBtn.addEventListener('click', e => {
                                $.ajax({
                                    url: `${locationHost}/org/1/tp/${tpID}/own/${id}/update/concurrency/`,
                                    method: 'patch',
                                    headers: {'X-CSRFToken': $.cookie('csrftoken')},
                                    data: JSON.stringify({
                                        'name': data['new_data']['name'],
                                        'number': data['new_data']['number'],
                                        'comment': data['new_data']['comment'],
                                    }),
                                    dataType: 'json',
                                    contentType: 'application/json',
                                    success: (data) => {
                                        name.innerText = data['name']
                                        number.innerText = data['number']
                                        comment.innerText = data['comment']
                                    }
                                })
                            })
                            closeBtn.addEventListener('click', e => {
                                $.ajax({
                                    url: `${locationHost}/org/1/tp/${tpID}/own/${id}/update/`,
                                    method: 'get',
                                    success: (data) => {
                                        let name = document.getElementById('name').value;
                                        let number = document.getElementById('number').value;
                                        let comment = document.getElementById('comment').value;
                                        name.innerText = data['name']
                                        number.innerText = data['number']
                                        comment.innerText = data['comment']
                                        body.innerHtml=''
                                    },
                                    error(data) {
                                        console.log(data)
                                    }
                                })
                            })
                            closeBtn2.addEventListener('click', e => {
                                $.ajax({
                                    url: `${locationHost}/org/1/tp/${tpID}/own/${id}/update/`,
                                    method: 'get',
                                    success: (data) => {
                                        let name = document.getElementById('name').value;
                                        let number = document.getElementById('number').value;
                                        let comment = document.getElementById('comment').value;
                                        name.innerText = data['name']
                                        number.innerText = data['number']
                                        comment.innerText = data['comment']
                                    }
                                })
                            })
                        }
                    },
                    error: function (response) {
                        console.log(response);
                    }
                });

                closeBtn.click();
            }
        })
}

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
            if (item.comment == null) {
                item.comment = '';
            }
            if (item.number == null) {
                item.number = '';
            }
            if (item.is_deleted === false) {
                body.innerHTML += ` <tr>
                                        <td>
                                            <a style="text-decoration: none; color:#566573;" href="/org/1/tp/${tpID}/contractor/${item.contractor}/">${item.name}</a>
                                        </td>
                                        <td>${item.number}</td>
                                        <td>${item.comment}</td>
                                        <td><button id="editOwns" type="button" class="btn btn-primary button_own" 
                                        data-ownid="${item.id}"
                                        data-ownname="${encodeURIComponent(item.name)}"
                                        data-ownnumber="${item.number}"
                                        data-owncomment="${encodeURIComponent(item.comment)}"
                                        data-ownversion="${item.version}"
                                        data-bs-toggle="modal" data-bs-target="#editOwn">Редактировать</button></td>
                                    </tr>`
            }
        })
        update()
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
            if (item.comment == null) {
                item.comment = '';
            }
            if (item.number == null) {
                item.number = '';
            }
            if (item.is_deleted === false) {
                body.innerHTML += ` <tr>
                                        <td>
                                            <a style="text-decoration: none; color:#566573;" href="/org/1/tp/${tpID}/contractor/${item.contractor}/">${item.name}</a>
                                        </td>
                                        <td>${item.number}</td>
                                        <td>${item.comment}</td>
                                        <td><button id="editOwns" type="button" class="btn btn-primary button_own"
                                        data-ownid="${item.id}"
                                        data-ownname="${encodeURIComponent(item.name)}"
                                        data-ownnumber="${item.number}"
                                        data-owncomment="${encodeURIComponent(item.comment)}"
                                        data-ownversion="${item.version}"
                                        data-bs-toggle="modal" data-bs-target="#editOwn">Редактировать</button></td>
                                    </tr>`
            }
            })
        update()
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
            if (item.comment == null) {
                item.comment = '';
            }
            if (item.number == null) {
                item.number = '';
            }
            if (item.is_deleted === false) {
                body.innerHTML += ` <tr>
                                        <td>
                                            <a style="text-decoration: none; color:#566573;" href="/org/1/tp/${tpID}/contractor/${item.contractor}/">${item.name}</a>
                                        </td>
                                        <td>${item.number}</td>
                                        <td>${item.comment}</td>
                                        <td><button id="editOwns" type="button" class="btn btn-primary button_own"
                                        data-ownid="${item.id}"
                                        data-ownname="${encodeURIComponent(item.name)}"
                                        data-ownnumber="${item.number}"
                                        data-owncomment="${encodeURIComponent(item.comment)}"
                                        data-ownversion="${item.version}"
                                        data-bs-toggle="modal" data-bs-target="#editOwn">Редактировать</button></td>
                                    </tr>`
            }
            })
        update()
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
                    if (item.comment == null) {
                        item.comment = '';
                    }
                    if (item.number == null) {
                        item.number = '';
                    }
                    if (item.is_deleted === false) {
                        body.innerHTML += ` <tr>
                                        <td>
                                            <a style="text-decoration: none; color: #566573;" href="/org/1/tp/${tpID}/contractor/${item.contractor}/">${item.name}</a>
                                        </td>
                                        <td>${item.number}</td>
                                        <td>${item.comment}</td>
                                        <td><button id="editOwns" type="button" class="btn btn-primary button_own"
                                        data-ownid="${item.id}"
                                        data-ownname="${encodeURIComponent(item.name)}"
                                        data-ownnumber="${item.number}"
                                        data-owncomment="${encodeURIComponent(item.comment)}"
                                        data-ownversion="${item.version}"
                                        data-bs-toggle="modal" data-bs-target="#editOwn">Редактировать</button></td>
                                    </tr>`
                    }
                    })
                update()
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
                    if (item.comment == null) {
                        item.comment = '';
                    }
                    if (item.number == null) {
                        item.number = '';
                    }
                    if (item.is_part === true) {
                        numberTitle.innerText = '';
                        item.number = ''
                    }
                    if (isPart.value === 'all' || item.is_part === false) {
                        numberTitle.innerText = 'Номер';
                    }
                    if (item.is_deleted === false) {
                        body.innerHTML += ` <tr>
                                        <td>
                                            <a style="text-decoration: none; color: #566573;" href="/org/1/tp/${tpID}/contractor/${item.contractor}/">${item.name}</a>
                                        </td>
                                        <td>${item.number}</td>
                                        <td>${item.comment}</td>
                                        <td><button id="editOwns" type="button" class="btn btn-primary button_own"
                                        data-ownid="${item.id}"
                                        data-ownpart="${item.is_part}"
                                        data-ownname="${encodeURIComponent(item.name)}"
                                        data-ownnumber="${item.number}"
                                        data-owncomment="${encodeURIComponent(item.comment)}"
                                        data-ownversion="${item.version}"
                                        data-bs-toggle="modal" data-bs-target="#editOwn">Редактировать</button></td>
                                    </tr>`
                    }
                    })
                update()
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
