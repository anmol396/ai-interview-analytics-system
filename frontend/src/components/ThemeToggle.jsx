import React, { useState, useEffect } from 'react';
import { Sun, Moon } from 'lucide-react';

const ThemeToggle = () => {
  const [isDark, setIsDark] = useState(false);

  useEffect(() => {
    // Initial sync with document class (already set in index.html script)
    const checkTheme = () => {
      setIsDark(document.documentElement.classList.contains('dark'));
    };
    checkTheme();
  }, []);

  const toggleTheme = () => {
    const isDarkNow = document.documentElement.classList.toggle('dark');
    localStorage.setItem('theme', isDarkNow ? 'dark' : 'light');
    setIsDark(isDarkNow);
  };

  return (
    <button
      onClick={toggleTheme}
      className="p-2.5 rounded-xl bg-[var(--bg-secondary)] border border-[var(--border-color)] text-[var(--accent-color)] hover:bg-[var(--bg-primary)] transition-all shadow-sm group active:scale-95"
      aria-label="Toggle theme"
    >
      {isDark ? (
        <Sun className="w-5 h-5 transition-transform duration-500 hover:rotate-90" />
      ) : (
        <Moon className="w-5 h-5 transition-transform duration-500 hover:-rotate-12" />
      )}
    </button>
  );
};

export default ThemeToggle;