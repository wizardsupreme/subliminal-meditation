// Theme Switcher
class ThemeSwitcher {
    constructor() {
        this.theme = localStorage.getItem('theme') || 'light';
        this.systemPrefersDark = window.matchMedia('(prefers-color-scheme: dark)');
        this.initialize();
    }

    initialize() {
        // Apply initial theme
        this.applyTheme(this.theme);
        
        // Listen for system theme changes
        this.systemPrefersDark.addListener((e) => {
            if (this.theme === 'system') {
                this.applyTheme(e.matches ? 'dark' : 'light');
            }
        });

        // Set up auto switch if enabled
        this.setupAutoSwitch();
    }

    setupAutoSwitch() {
        const now = new Date();
        const hours = now.getHours();
        
        // Auto switch based on time if enabled
        if (this.theme === 'system') {
            const startDark = 18; // 6 PM
            const endDark = 6;    // 6 AM
            
            if ((hours >= startDark) || (hours < endDark)) {
                this.applyTheme('dark');
            } else {
                this.applyTheme('light');
            }
        }
    }

    toggleTheme() {
        const newTheme = document.documentElement.classList.contains('dark-mode') ? 'light' : 'dark';
        this.theme = newTheme;
        localStorage.setItem('theme', newTheme);
        this.applyTheme(newTheme);
        this.updateButtonIcon(newTheme);
    }

    applyTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.classList.add('dark-mode');
        } else {
            document.documentElement.classList.remove('dark-mode');
        }
        this.updateButtonIcon(theme);
    }

    updateButtonIcon(theme) {
        const button = document.getElementById('theme-toggle');
        if (button) {
            // Update button icon and aria-label
            button.innerHTML = theme === 'dark' 
                ? '☀️' 
                : '🌙';
            button.setAttribute('aria-label', 
                theme === 'dark' 
                    ? 'Switch to light mode' 
                    : 'Switch to dark mode'
            );
        }
    }
}

// Initialize theme switcher
const themeSwitcher = new ThemeSwitcher();

// Export for use in other files
window.themeSwitcher = themeSwitcher; 