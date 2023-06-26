setTimeout(() => {
    console.log('running script...')
    preventForm()
    // alertAnimation()
}, 2000);

function preventForm() {
    form1 = document.querySelector('#login-form')
    form1.addEventListener("submit", (event)=>{
        event.preventDefault()
        console.log('okkokoko');
    }, false)
    form = document.querySelector('#register-form')
    form.addEventListener("submit", (event)=>{
        event.preventDefault()
    }, false)
}
