function toggleTheme() {
    document.body.classList.toggle('dark-mode');
    const themeButton = document.getElementById('theme-toggle-button');
    const icon = themeButton.querySelector('i');

    if (document.body.classList.contains('dark-mode')) {
        icon.classList.replace('fa-moon', 'fa-sun');
        themeButton.innerHTML = `<i class="fas fa-sun"></i> Light Mode`;
        localStorage.setItem('theme', 'dark'); // Save dark theme preference
    } else {
        icon.classList.replace('fa-sun', 'fa-moon');
        themeButton.innerHTML = `<i class="fas fa-moon"></i> Dark Mode`;
        localStorage.setItem('theme', 'light'); // Save light theme preference
    }
}

function loadThemePreference() {
    const theme = localStorage.getItem('theme');
    if (theme === 'dark') {
        document.body.classList.add('dark-mode');
        const themeButton = document.getElementById('theme-toggle-button');
        themeButton.innerHTML = `<i class="fas fa-sun"></i> Light Mode`;
    } else {
        document.body.classList.remove('dark-mode');
        const themeButton = document.getElementById('theme-toggle-button');
        themeButton.innerHTML = `<i class="fas fa-moon"></i> Dark Mode`;
    }
}
