/* global bootstrap: false */
(function () {
  'use strict'
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  tooltipTriggerList.forEach(function (tooltipTriggerEl) {
    new bootstrap.Tooltip(tooltipTriggerEl)
  })
})()


let sidebarBtns = Object.values($('.sidebar-btn'));
let sidebarDivs = Object.values($('.sidebar-ul'));
let sidebarLinks = Object.values($('.sidebar-link'));


let path = window.location.href;


sidebarLinks.forEach((element) => {
  if (element.href == path) {
    let elementParent = element.parentNode.parentNode.parentNode;

    element.style.borderLeft = 'solid 3px rgb(104, 104, 255)'
    element.style.color = 'rgb(104, 104, 255)'

    sidebarDivs.forEach((element) => {
      if (elementParent == element) {
        sidebarBtns[sidebarDivs.indexOf(element)].classList.remove('collapsed')
        element.classList.add('show')
      }
    })
  }
})

// let button = document.getElementById('tradepointChoices');
// let choiceItem = document.getElementById('tradepointItem');
//
// button.addEventListener('click', (data) => {
//           console.log(data);
//           data.forEach(function (item) {
//             console.log(item);
//             choiceItem.value = item.value.name;
//             choiceItem.href = item.value.id;
//           })
// })
