// $(document).ready(function(){
//     $('.toast').toast('show')
// })

var toastElList = [].slice.call(document.querySelectorAll('.toast'))
var toastList = toastElList.map(function (toastEl) {
  return new bootstrap.Toast(toastEl, option)
})
var count =0
