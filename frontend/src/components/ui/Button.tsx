import React from 'react';
import { clsx } from 'clsx';

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'dark' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  icon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  icon,
  className,
  disabled,
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center font-medium rounded transition-all duration-150 focus:outline-none focus:ring-2 focus:ring-offset-1 disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer';

  const variantClasses = {
    primary: 'bg-juris-textPrimary text-white hover:bg-juris-surface hover:shadow-subtle focus:ring-juris-textPrimary',
    secondary: 'bg-juris-bgMuted text-juris-textPrimary hover:bg-juris-border/60 border border-juris-border focus:ring-juris-textPrimary',
    outline: 'bg-transparent text-juris-textPrimary border border-juris-border hover:bg-juris-bgMuted hover:border-juris-borderDark focus:ring-juris-textPrimary',
    ghost: 'bg-transparent text-juris-textMuted hover:text-juris-textPrimary hover:bg-juris-bgMuted focus:ring-juris-textPrimary',
    dark: 'bg-juris-card text-white hover:bg-juris-surfaceLight border border-juris-surfaceBorder focus:ring-white',
    danger: 'bg-juris-riskHigh text-white hover:bg-red-700 focus:ring-red-600',
  };

  const sizeClasses = {
    sm: 'text-xs px-2.5 py-1.5 gap-1.5',
    md: 'text-sm px-4 py-2 gap-2',
    lg: 'text-base px-5 py-2.5 gap-2.5',
  };

  return (
    <button
      className={clsx(baseClasses, variantClasses[variant], sizeClasses[size], className)}
      disabled={disabled}
      {...props}
    >
      {icon && <span className="shrink-0">{icon}</span>}
      {children}
    </button>
  );
};
