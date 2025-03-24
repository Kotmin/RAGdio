import { useRef } from "react";
import FileCard from "./FileCard";

interface Props {
  files: File[];
  setFiles: (files: File[]) => void;
}

export default function AudioUploadSection({ files, setFiles }: Props) {
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    const valid = Array.from(fileList).filter((file) =>
      ["audio/mpeg", "audio/wav", "audio/mp3", "audio/mp4"].includes(file.type)
    );
    setFiles([...files, ...valid]);
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

      {/* File gallery */}
      {files.length > 0 && (
        <div className="overflow-x-auto">
          <div className="flex space-x-3 w-fit">
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

      {/* File upload input */}
      <div className="flex flex-col items-center text-center text-gray-500">
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
