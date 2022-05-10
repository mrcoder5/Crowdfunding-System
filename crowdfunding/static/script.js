// $(document).ready(function(){
//     $('.toast').toast('show')
// })

$('.toast').toast('show')
var count =0


const toastElement = document.getElementById("toast")
const toastBody = document.getElementById("toast-body")

const toast = new bootstrap.Toast(toastElement, { delay: 2000 })

htmx.on("showMessage", (e) => {
  toastBody.innerText = e.detail.value
  toast.show()
})