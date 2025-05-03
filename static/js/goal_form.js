document.getElementById('goal_form').addEventListener('submit',function(e){
    const title = document.querySelector('input[name="title"]').value;
    const progress = document.querySelector('input[name="progress"]').value;
    const startDate = document.querySelector('input[name="start_date"]').value;
    const endDate = document.querySelector('input[name="end_date"]').value;

    if(!title.trim()){
        alert('عنوان هدف نمی‌تواند خالی باشد');
        e.preventDefault();
    }else if(progress < 0 || progress > 100){
        alert('پیشرفت باید بین ۰ تا ۱۰۰ باشد');
        e.preventDefault();
    }else if(startDate && endDate && new Date(startDate) > new Date(endDate)){
        alert('تاریخ شروع نمی‌تواند بعد از تاریخ پایان باشد');
        e.preventDefault();
    }
})