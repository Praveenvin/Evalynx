import { CheckCircle2, FileText, X } from "lucide-react";

interface FileListProps {
  files: File[];
  onRemove: (index: number) => void;
}

export default function FileList({ files, onRemove }: FileListProps) {
  if (files.length === 0) return null;

  return (
    <ul className="mt-4 flex flex-col gap-2">
      {files.map((file, index) => (
        <li
          key={`${file.name}-${index}`}
          className="flex items-center justify-between rounded-lg border border-border bg-surface px-3 py-2"
        >
          <div className="flex min-w-0 items-center gap-2.5">
            <FileText size={16} className="shrink-0 text-ink-faint" />
            <span className="truncate text-sm text-ink">{file.name}</span>
            <CheckCircle2 size={15} className="shrink-0 text-good" />
          </div>
          <button
            type="button"
            onClick={() => onRemove(index)}
            aria-label={`Remove ${file.name}`}
            className="ml-3 shrink-0 rounded-md p-1 text-ink-faint transition-colors hover:bg-canvas hover:text-weak"
          >
            <X size={15} />
          </button>
        </li>
      ))}
    </ul>
  );
}
