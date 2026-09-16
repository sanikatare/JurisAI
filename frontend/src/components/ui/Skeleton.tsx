import React from 'react';
import { clsx } from 'clsx';

export interface SkeletonProps {
  className?: string;
  height?: string;
  width?: string;
}

export const Skeleton: React.FC<SkeletonProps> = ({ className, height = 'h-4', width = 'w-full' }) => {
  return (
    <div
      className={clsx('skeleton-shimmer rounded bg-juris-bgMuted', height, width, className)}
    />
  );
};
