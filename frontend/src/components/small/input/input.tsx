import React, { useState } from "react";

type InputVariant = "default" | "success" | "error";

type InputSize = "xs" | "sm" | "md" | "lg" | "xl";
interface InputProps {
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  variant?: InputVariant;
  size?: InputSize;
  disabled?: boolean;
  type?: React.HTMLInputTypeAttribute;
  label?: string;
  id?: string;
  isFloating?: boolean;
  span?: string;
}
const Input = ({
  label,
  id,
  placeholder,
  variant = "default",
  size = "md",
  disabled = false,
  isFloating = false,
  span,
}: InputProps): React.ReactElement => {
  const [text, setText] = useState("");
  const handleChange = (event: {
    target: { value: React.SetStateAction<string> };
  }) => {
    setText(event.target.value);
  };
  const baseStyles =
    "input font-medium transition-all duration-200 focus:outline-none";
  const variants: Record<InputVariant, string> = {
    default: "",
    success: "is-valid",
    error: "is-invalid",
  };
  const sizes: Record<InputSize, string> = {
    xs: "input-xs",
    sm: "input-sm",
    md: "", //default
    lg: "input-lg",
    xl: "input-xl",
  };
  if (isFloating) {
    return (
      <>
        <div className="input-floating max-w-sm">
          <input
            id={id}
            value={text}
            className={`${baseStyles} ${variants[variant]} ${sizes[size]}`}
            placeholder={`${placeholder}`}
            disabled={disabled}
            onChange={handleChange}
          />
          <label className="input-floating-label" htmlFor={`${id}`}>
            {label}
          </label>
          <span className="helper-text ps-3">{span}</span>
        </div>
      </>
    );
  }
  return (
    <>
      <div className="max-w-sm">
        <label className="label-text" htmlFor={`${id}`}>
          {label}
        </label>
        <input
          id={id}
          value={text}
          type="text"
          className={`${baseStyles} ${variants[variant]} ${sizes[size]}`}
          placeholder={`${placeholder}`}
          disabled={disabled}
          onChange={handleChange}
        />
        <span className="helper-text">{span}</span>
      </div>
    </>
  );
};

export default Input;
