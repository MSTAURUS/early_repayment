$(function(){
    $('.decimal').on('input', function(){
         this.value = this.value.replace(/^\.|[^\d\.]|\.(?=.*\.)|^0+(?=\d)/g, '');
     });
});

document.addEventListener('DOMContentLoaded', function() {
const themeToggle = document.getElementById('theme-toggle');
const currentTheme = localStorage.getItem('theme') || 'light';

// Устанавливаем текущую тему
document.documentElement.setAttribute('data-theme', currentTheme);
updateButtonText(currentTheme);

themeToggle.addEventListener('click', function() {
    const currentTheme = localStorage.getItem('theme') || 'light';

    const newTheme = currentTheme === 'light' ? 'dark' : 'light';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateButtonText(newTheme);
});

function updateButtonText(theme) {
    if (theme === 'light'){
        document.getElementById('icon-btn').className = 'bi-lightbulb-fill';
    } else {
        document.getElementById('icon-btn').className = 'bi-lightbulb';
    }
    document.cookie = "theme="+theme;

}

});