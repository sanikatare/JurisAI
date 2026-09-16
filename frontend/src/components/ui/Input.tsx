import React from 'react';
import { clsx } from 'clsx';

export interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  icon?: React.ReactNode;
  error?: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(({
  className,
  icon,
  error,
  ...props
}, ref) => {
  return (
    <div className="w-full relative">
      {icon && (
        <div className="absolute left-3 top-1/2 -translate-y-1/2 text-juris-textSubtle pointer-events-none">
          {icon}
        </div>
      )}
      <input
        ref={ref}
        className={clsx(
          'w-full bg-white text-juris-textPrimary placeholder:text-juris-textSubtle border border-juris-border rounded-md py-2 text-sm transition-all duration-150 focus:outline-none focus:border-juris-textPrimary focus:ring-1 focus:ring-juris-textPrimary',
          icon ? 'pl-9 pr-3' : 'px-3',
          error && 'border-juris-riskHigh focus:border-juris-riskHigh focus:ring-juris-riskHigh',
          className
        )}
        {...props}
      />
      {error && <p className="mt-1 text-xs text-juris-riskHigh">{error}</p>}
    </div>
  );
});

Input.displayName = 'Input';
