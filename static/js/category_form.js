document.getElementById('category-form').addEventListener('submit', function(e){
    const name = document.querySelector('input[name="name"]').value;
    if (!name.trim()) {
        alert('نام دسته‌بندی نمی‌تواند خالی باشد');
        e.preventDefault();
    }
});