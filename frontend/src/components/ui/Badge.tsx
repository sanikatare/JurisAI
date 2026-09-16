import React from 'react';
import { clsx } from 'clsx';

export interface BadgeProps {
  children: React.ReactNode;
  variant?: 'low' | 'mod' | 'high' | 'neutral' | 'dark' | 'outline';
  size?: 'sm' | 'md';
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({
  children,
  variant = 'neutral',
  size = 'md',
  className,
}) => {
  const baseClasses = 'inline-flex items-center font-medium rounded-full tracking-tight transition-colors';

  const variantClasses = {
    low: 'bg-juris-riskLowBg text-juris-riskLow border border-juris-riskLowBorder',
    mod: 'bg-juris-riskModBg text-juris-riskMod border border-juris-riskModBorder',
    high: 'bg-juris-riskHighBg text-juris-riskHigh border border-juris-riskHighBorder',
    neutral: 'bg-juris-bgMuted text-juris-textMuted border border-juris-border',
    dark: 'bg-juris-surface text-white border border-juris-surfaceBorder',
    outline: 'bg-transparent text-juris-textBody border border-juris-border',
  };

  const sizeClasses = {
    sm: 'text-[11px] px-2 py-0.5',
    md: 'text-xs px-2.5 py-1',
  };

  return (
    <span className={clsx(baseClasses, variantClasses[variant], sizeClasses[size], className)}>
      {children}
    </span>
  );
};
