import { useRef, useState } from "react";
import {
  CloudArrowUpIcon,
  PaperClipIcon,
  TrashIcon,
} from "@heroicons/react/24/solid";

interface FileItem {
  id: string;
  file: File;
}

function FileUpload() {
  const [files, setFiles] = useState<FileItem[]>([]);
  const inputRef = useRef<HTMLInputElement | null>(null);

  const handleFiles = (fileList: FileList | null) => {
    if (!fileList) return;
    const newFiles: FileItem[] = Array.from(fileList).map((file) => ({
      id: `${file.name}-${file.lastModified}`,
      file,
    }));
    setFiles((prev) => [...prev, ...newFiles]);
  };

  const removeFile = (id: string) => {
    setFiles((prev) => prev.filter((f) => f.id !== id));
  };

  const onDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    handleFiles(e.dataTransfer.files);
  };

  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  return (
    <div className="w-full space-y-2">
      {/* Counter */}
      <div className="text-sm text-gray-500 font-medium">
        {files.length > 0
          ? `${files.length} file(s) selected`
          : "No files added yet"}
      </div>

      {/* Upload Box */}
      <div
        onClick={() => inputRef.current?.click()}
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        className="neon-border relative border-4 border-dashed rounded-xl p-4 transition-all cursor-pointer hover:shadow-lg"
      >
        {/* Upload Icon + Label */}
        {files.length === 0 && (
          <div className="flex flex-col items-center text-center text-gray-500 py-4">
            <CloudArrowUpIcon className="w-8 h-8 text-purple-600 mb-2" />
            <p className="font-medium">Drag & drop or click to choose</p>
            <p className="text-sm text-gray-400">
              mp3, wav, m4a • max 25MB each
            </p>
          </div>
        )}

        <input
          ref={inputRef}
          type="file"
          accept="audio/*"
          multiple
          className="hidden"
          onChange={(e) => handleFiles(e.target.files)}
        />

        {/* Files inside the box */}
        {files.length > 0 && (
          <div className="mt-2 overflow-x-auto">
            <div className="flex space-x-3 pb-2">
              {files.map(({ id, file }) => (
                <div
                  key={id}
                  className="relative min-w-[110px] max-w-[110px] h-[140px] border-2 border-purple-400 rounded-lg p-2 bg-white shadow-md flex flex-col items-center justify-start"
                >
                  {/* Trash - ABSOLUTE TOP LEFT */}
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      removeFile(id);
                    }}
                    className="absolute top-1 left-1 bg-red-100 border border-red-300 rounded-full p-[2px] hover:bg-red-200"
                    title="Remove file"
                  >
                    <TrashIcon className="w-4 h-4 text-red-600" />
                  </button>

                  {/* Paper Clip Icon */}
                  <PaperClipIcon className="w-6 h-6 text-purple-400 mb-1 mt-4" />

                  {/* Filename */}
                  <p className="text-xs font-semibold text-center px-1 leading-tight line-clamp-2 break-all">
                    {file.name}
                  </p>

                  {/* File type */}
                  <p className="text-[10px] text-gray-400 text-center mt-1">
                    {file.type.split("/")[1] || "unknown"}
                  </p>

                  {/* File size */}
                  <p className="text-[10px] text-gray-500 text-center">
                    {formatBytes(file.size)}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default FileUpload;
