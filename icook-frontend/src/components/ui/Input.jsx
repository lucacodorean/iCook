import React from 'react';

export const Input = ({ className = '', ...props }) => (
    <input
        className={`border border-gray-300 rounded-xl px-4 py-2 focus:outline-none  ${className}`}
        {...props}
    />
);
