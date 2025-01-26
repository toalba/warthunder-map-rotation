function toggleColorMode() {
    (() => {
        const setPreferredTheme = () => {
            if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
                document.documentElement.setAttribute('data-bs-theme', 'dark');
            } else {
                document.documentElement.setAttribute('data-bs-theme', 'light');
            }
        };
        window.addEventListener('DOMContentLoaded', () => {
            setPreferredTheme();
        });
    })();
}

document.addEventListener('DOMContentLoaded', function(event) {
    toggleColorMode();
});