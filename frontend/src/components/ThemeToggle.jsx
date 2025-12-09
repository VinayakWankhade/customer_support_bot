import React, { useEffect, useState } from 'react';
import { Sun, Moon } from 'lucide-react';

const ThemeToggle = () => {
    const [isDark, setIsDark] = useState(() => {
        // Check localStorage or system preference on initial load
        if (typeof window !== 'undefined') {
            return localStorage.getItem('theme') === 'dark' ||
                (!localStorage.getItem('theme') && window.matchMedia('(prefers-color-scheme: dark)').matches);
        }
        return false;
    });

    useEffect(() => {
        const root = window.document.documentElement;
        if (isDark) {
            root.classList.add('dark');
            localStorage.setItem('theme', 'dark');
        } else {
            root.classList.remove('dark');
            localStorage.setItem('theme', 'light');
        }
    }, [isDark]);

    const toggleTheme = () => {
        setIsDark(!isDark);
    };

    return (
        <button
            onClick={toggleTheme}
            className={`
                relative p-2 rounded-full transition-all duration-500 ease-in-out
                focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2
                ${isDark ? 'bg-gray-800 text-yellow-400 hover:bg-gray-700' : 'bg-gray-100 text-orange-500 hover:bg-gray-200'}
            `}
            aria-label="Toggle Theme"
        >
            <div className="relative w-6 h-6">
                <Sun
                    className={`absolute inset-0 w-6 h-6 transition-all duration-500 transform ${isDark ? 'rotate-90 opacity-0 scale-50' : 'rotate-0 opacity-100 scale-100'}`}
                />
                <Moon
                    className={`absolute inset-0 w-6 h-6 transition-all duration-500 transform ${isDark ? 'rotate-0 opacity-100 scale-100' : '-rotate-90 opacity-0 scale-50'}`}
                />
            </div>
            {/* Tooltip for fun */}
            <span className="sr-only">{isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'}</span>
        </button>
    );
};

export default ThemeToggle;
