import React from 'react';

export const Card = ({ children, className = '', ...props }) => {
  return (
    <div className={`bg-white rounded-xl shadow-md overflow-hidden ${className}`} {...props}>
      {children}
    </div>
  );
};

export const CardHeader = ({ children, className = '' }) => {
  return <div className={`px-6 py-4 border-b border-gray-100 ${className}`}>{children}</div>;
};

export const CardBody = ({ children, className = '' }) => {
  return <div className={`px-6 py-4 ${className}`}>{children}</div>;
};

export const CardFooter = ({ children, className = '' }) => {
  return <div className={`px-6 py-4 bg-gray-50 ${className}`}>{children}</div>;
};
