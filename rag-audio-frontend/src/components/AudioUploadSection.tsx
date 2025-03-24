import { useRef } from "react";
import FileCard from "./FileCard";
import { toast } from "react-toastify";

interface Props {
  files: File[];
  setFiles: (files: File[]) => void;
}

export default function AudioUploadSection({ files, setFiles }: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    const incoming = Array.from(fileList);

    const SUPPORTED_FORMATS = [
      "mp3",
      "mp4",
      "mpeg",
      "mpga",
      "m4a",
      "wav",
      "webm",
    ];

    const newFiles: File[] = [];

    incoming.forEach((file) => {
      const isDuplicate = files.some(
        (f) => f.name === file.name && f.size === file.size
      );

      if (isDuplicate) {
        toast.warning(`Duplicate file skipped: ${file.name}`);
        return;
      }

      if (file.size === 0) {
        toast.error(`File "${file.name}" is empty.`);
        return;
      }

      const ext = file.name.split(".").pop()?.toLowerCase();
      if (!ext || !SUPPORTED_FORMATS.includes(ext)) {
        toast.error(`Unsupported file type: ${file.name}`);
        return;
      }

      newFiles.push(file);
    });

    setFiles([...files, ...newFiles]);
  };

  const removeFile = (target: File) => {
    setFiles(files.filter((f) => f !== target));
  };

  return (
    <div
      onDrop={(e) => {
        e.preventDefault();
        handleFiles(e.dataTransfer.files);
      }}
      onDragOver={(e) => e.preventDefault()}
      className="neon-border border-4 border-dashed rounded-xl p-4 space-y-4"
    >
      {/* Counter */}
      {files.length > 0 && (
        <p className="text-sm text-gray-600 font-medium">
          {files.length} file{files.length > 1 ? "s" : ""} added
        </p>
      )}

      {/* Scrollable / Wrapping file list */}
      {files.length > 0 && (
        <div className="overflow-x-auto">
          <div className="flex flex-wrap gap-3">
            {files.map((file) => (
              <FileCard
                key={file.name + file.lastModified}
                file={file}
                onRemove={() => removeFile(file)}
              />
            ))}
          </div>
        </div>
      )}

      {/* Upload UI */}
      <div className="flex flex-col items-center text-center text-gray-500 pt-2">
        <button
          type="button"
          onClick={() => inputRef.current?.click()}
          className="font-medium text-sm px-4 py-1 bg-purple-100 border border-purple-300 rounded hover:bg-purple-200"
        >
          Add Files
        </button>
        <p className="text-xs text-gray-400 mt-1">
          Drag & drop or use the button
        </p>
        <p className="text-[10px] text-gray-400">
          Accepted: mp3, wav, m4a • Max 25MB
        </p>
        <input
          ref={inputRef}
          type="file"
          accept="audio/*"
          multiple
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />
      </div>
    </div>
  );
}
