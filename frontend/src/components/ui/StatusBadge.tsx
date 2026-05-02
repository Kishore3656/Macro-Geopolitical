interface StatusBadgeProps {
  label: string;
  status: 'success' | 'warning' | 'danger' | 'neutral';
  value?: string | number;
}

const statusColors = {
  success: 'bg-success bg-opacity-20 text-success',
  warning: 'bg-amber bg-opacity-20 text-amber',
  danger: 'bg-danger bg-opacity-20 text-danger',
  neutral: 'bg-slate-800 text-slate-300',
};

export default function StatusBadge({ label, status, value }: StatusBadgeProps) {
  return (
    <div className={`px-3 py-2 rounded-lg text-sm font-medium ${statusColors[status]}`}>
      {label} {value !== undefined && <span className="ml-1">{value}</span>}
    </div>
  );
}
