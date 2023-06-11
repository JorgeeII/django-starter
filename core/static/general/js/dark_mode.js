const userPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

function setTheme(theme) {
    document.body.setAttribute('data-bs-theme', theme);
}

document.addEventListener('DOMContentLoaded', () => {
    const storedTheme = localStorage.getItem('theme');
    const theme = (storedTheme == 'auto' ? (userPrefersDark ? 'dark' : 'light') : storedTheme);
    setTheme(theme);
});

function toggleTheme() {
    let currentTheme = localStorage.getItem('theme');
    if (currentTheme == 'auto') {
        currentTheme = (userPrefersDark ? 'dark' : 'light')
    }
    console.log(currentTheme)
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
};