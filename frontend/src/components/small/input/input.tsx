type InputVariant =
  | "primary"
  | "secondary"
  | "success"
  | "danger"
  | "warning";

type InputSize = "xs" | "sm" | "md" | "lg" | "xl";

interface InputProps {
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  variant?: InputVariant;
  size?: InputSize;
  disabled?: boolean;
  type?: React.HTMLInputTypeAttribute;
}

const Input = ({
  value,
  onChange,
  placeholder = "",
  variant = "primary",
  size = "xs",
  disabled = false,
  type = "text",
}: InputProps): React.ReactElement => {
  const baseStyles =
    "input font-medium rounded transition-all duration-200 focus:outline-none";

  const variants: Record<InputVariant, string> = {
    primary: "input-primary",
    secondary: "input-secondary",
    success: "input-success",
    danger: "input-error",
    warning: "input-warning",
  };

  const sizes: Record<InputSize, string> = {
    xs: "input-xs",
    sm: "input-sm",
    md: "", //default
    lg: "input-lg",
    xl: "input-xl",
  };

  return (
    <input
      type={type}
      value={value}
      onChange={onChange}
      placeholder={placeholder}
      disabled={disabled}
      className={`${baseStyles} ${variants[variant]} ${sizes[size]}`}
    />
  );
};

export default Input;
