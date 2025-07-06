import React, { useState, useCallback } from 'react';
import './Button.css';

interface ButtonProps {
  text: string;
  onClick?: () => void;
  disabled?: boolean;
  variant?: 'primary' | 'secondary' | 'danger';
  size?: 'small' | 'medium' | 'large';
  loading?: boolean;
}

export const Button: React.FC<ButtonProps> = ({
  text,
  onClick,
  disabled = false,
  variant = 'primary',
  size = 'medium',
  loading = false
}) => {
  const [isHovered, setIsHovered] = useState(false);
  
  const handleClick = useCallback(() => {
    if (!disabled && !loading && onClick) {
      onClick();
    }
  }, [disabled, loading, onClick]);
  
  const getClassName = () => {
    const classes = ['button'];
    classes.push(`button--${variant}`);
    classes.push(`button--${size}`);
    
    if (disabled) classes.push('button--disabled');
    if (loading) classes.push('button--loading');
    if (isHovered) classes.push('button--hovered');
    
    return classes.join(' ');
  };
  
  return (
    <button
      className={getClassName()}
      onClick={handleClick}
      disabled={disabled || loading}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      {loading ? (
        <span className="button__spinner">Loading...</span>
      ) : (
        text
      )}
    </button>
  );
};

export default Button;