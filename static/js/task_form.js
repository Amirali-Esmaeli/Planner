document.getElementById('task-form').addEventListener('submit', function(e){
    const title = document.querySelector('input[name="title"]').value;
    const dueDate = document.querySelector('input[name="due_date"]').value;
    const today = new Date().toISOString().split('T')[0];

    if (!title.trim()) {
        alert('عنوان وظیفه نمی‌تواند خالی باشد');
        e.preventDefault();
    }else if (!dueDate) {
        alert('تاریخ سررسید نمی‌تواند خالی باشد');
        e.preventDefault();
    }else if (dueDate < today) {
        alert('تاریخ سررسید نمی‌تواند در گذشته باشد');
        e.preventDefault();
    }else if (!goal) {
        alert('هدف مرتبط را انتخاب کنید');
        e.preventDefault();
    }
});