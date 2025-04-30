document.getElementById('signup-form').addEventListener('submit',function(e){
    const password1 = document.querySelector('input[name="password1"]').value;
    const password2 = document.querySelector('input[name="password2"]').value;
    if(password1.length<8){
        alert('رمز عبور باید حداقل ۸ کاراکتر باشد.');
        e.preventDefault();
    }else if(password1 != password2){
        alert('رمزهای عبور مطابقت ندارند.');
        e.preventDefault();
    }
    console.log("signup.js loaded!");
});