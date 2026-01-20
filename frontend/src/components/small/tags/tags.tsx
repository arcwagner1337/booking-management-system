type TagVariant = "primary" | "secondary" | "success" | "danger";

type TagSize = "xs" | "sm" | "md";

interface TagButtonProps {
  label: string;
  active?: boolean;
  onClick?: () => void;
  variant?: TagVariant;
  size?: TagSize;
  disabled?: boolean;
}

const TagButton = ({
  label,
  active = false,
  onClick = () => {},
  variant = "primary",
  size = "xs",
  disabled = false,
}: TagButtonProps): React.ReactElement => {
  const baseStyles =
    "inline-flex items-center rounded-full font-medium transition-all duration-200 select-none";

  const variants: Record<TagVariant, string> = {
    primary: "tag-primary",
    secondary: "tag-secondary",
    success: "tag-success",
    danger: "tag-danger",
  };

  const sizes: Record<TagSize, string> = {
    xs: "tag-xs",
    sm: "tag-sm",
    md: "tag-md",
  };

  const activeStyles = active ? "opacity-100" : "opacity-60 hover:opacity-90";

  return (
    <button
      type="button"
      disabled={disabled}
      onClick={onClick}
      className={`tag ${baseStyles} ${variants[variant]} ${sizes[size]} ${activeStyles}`}
    >
      {label}
    </button>
  );
};

export default TagButton;
