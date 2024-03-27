let phone = document.querySelector("#phone")
let password = document.querySelector("#password")
let error = document.querySelector(".error")
let error_1 = document.querySelector(".error-1")
let error_2 = document.querySelector(".error-2")
let error_3 = document.querySelector(".error-3")
let email = document.querySelector("#Email")
// let div=document.createElement("div")
// div.innerHTML='<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; "> Error !<button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
let code = document.querySelector("#code")
let form = document.querySelector("#form")
// let btn=document.querySelector(".btn")
// btn.addEventListener("click",function(){
//     console.log(phone.value,password.value,email.value,code.value)
//     console.log(typeof phone.value)

//     console.log(`${phone.value}\n${password.value}\n${email.value}\n${code.value}`)
// })
// email.addEventListener("change",function(){
//  code.value=email.value
// })
// email.addEventListener("input",function(){

//   code.value=email.value;
// })




form.addEventListener('submit', function (eve) {
   if (phone.value == "") {
      // let al=document.querySelector('.error')
      // al.append(div)
      error.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; "> Phone Number Empty </i><button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("nothing")
      eve.preventDefault()

   }
   if (phone.value.length < 10 && phone.value !== "") {
      // let al=document.querySelector('.error')
      // al.append(div)
      error.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; ">Too Short Phone Number<button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("less")
      eve.preventDefault()

   }
   if (phone.value.length > 10) {
      // let al=document.querySelector('.error')
      // al.append(div)
      error.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; ">Too Long Phone Number<button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("greater")
      eve.preventDefault()

   }
   if (isNaN(phone.value)) {
      // let al=document.querySelector('.error')
      // al.append(div)
      error.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; ">Please Enter Number Not Charcters<button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("string")
      eve.preventDefault()

   }



   if (password.value == "") {
      // let al=document.querySelector('.error-2')
      // al.append(div)
      error_1.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; "> Password Empty<button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("nothingPass")
      eve.preventDefault()

   }
   if (password.value.length < 5 && password.value !== "") {
      // let al=document.querySelector('.error-2')
      // al.append(div)
      error_1.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; "> Password Too Short<button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("lesspass")
      eve.preventDefault()

   }
   if (password.value.length > 25) {
      // let al=document.querySelector('.error-2')
      // al.append(div)
      error_1.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; "> Password Too Long<button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("greaterPass")
      eve.preventDefault()

   }

   if (email.value == "") {
      //  let al=document.querySelector('.error-2')
      // al.append(div)
      error_2.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; "> Empty Email <button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("nothingEm")
      eve.preventDefault()

   }
   
   if (code.value == "") {
      //  let al=document.querySelector('.error-3')
      // al.append(div)
      error_3.innerHTML = '<div class="col-sm-10"><div class="alert alert-primary alert alert-danger alert-dismissible fade show p-2" role="alert"  style="height:40px; "> Invite Code Empty<button type="button" class="btn-close  " data-bs-dismiss="alert" aria-label="Close"  style="height:1px; "></button></div></div>'
      console.log("nothingCode")
      eve.preventDefault()

   }








})
