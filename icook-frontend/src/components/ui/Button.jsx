import React from 'react';

export const Button = ({ children, onClick, className = '', type = 'button' }) => (
    <button
        type={type}
        onClick={onClick}
        className={`bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-xl transition ${className}`}
    >
        {children}
    </button>
);
