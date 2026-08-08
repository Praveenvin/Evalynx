import { useRef, useState, type DragEvent } from "react";
import { UploadCloud } from "lucide-react";

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
  multiple?: boolean;
  accept?: string;
  label?: string;
}

export default function FileUpload({
  onFilesSelected,
  multiple = true,
  accept = ".pdf",
  label = "resumes",
}: FileUploadProps) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    onFilesSelected(Array.from(fileList));
  };

  const handleDrop = (event: DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    setIsDragging(false);
    handleFiles(event.dataTransfer.files);
  };

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragging(true);
      }}
      onDragLeave={() => setIsDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === "Enter" || e.key === " ") inputRef.current?.click();
      }}
      className={`flex cursor-pointer flex-col items-center justify-center rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors duration-150 ${
        isDragging
          ? "border-accent bg-accent-soft"
          : "border-border-strong bg-canvas hover:border-accent-ring hover:bg-accent-soft/40"
      }`}
    >
      <div className="flex h-11 w-11 items-center justify-center rounded-full bg-accent-soft text-accent">
        <UploadCloud size={20} />
      </div>
      <p className="mt-3 text-sm font-medium text-ink">
        Drop {label} here
      </p>
      <p className="mt-1 text-xs text-ink-faint">
        or <span className="font-medium text-accent">Browse files</span>
      </p>
      <p className="mt-3 text-xs text-ink-faint">
        {multiple ? "Multiple PDF files supported" : "PDF file"}
      </p>
      <input
        ref={inputRef}
        type="file"
        multiple={multiple}
        accept={accept}
        className="hidden"
        onChange={(e) => handleFiles(e.target.files)}
      />
    </div>
  );
}
