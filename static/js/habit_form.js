document.getElementById('habit-form').addEventListener('submit', function(e){
    const title = document.querySelector('input[name="title"]').value;
    if(!title.trim()){
        alert('عنوان عادت نمی‌تواند خالی باشد');
        e.preventDefault();
    }
});