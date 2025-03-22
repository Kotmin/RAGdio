import { useRef, useState } from "react";
import { CloudArrowUpIcon, TrashIcon } from "@heroicons/react/24/solid";

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
    <div className="w-full">
      {/* Counter */}
      {files.length > 0 && (
        <p className="mb-2 text-sm text-gray-500 font-medium">
          {files.length} file{files.length > 1 ? "s" : ""} selected
        </p>
      )}

      {/* Upload Box */}
      <div
        onClick={() => inputRef.current?.click()}
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        className="group relative w-full border-4 border-dashed rounded-xl p-6 text-center cursor-pointer neon-border hover:shadow-lg"
      >
        <CloudArrowUpIcon className="w-8 h-8 mx-auto text-purple-600 group-hover:scale-110 transition-transform" />
        <p className="text-gray-700 font-medium mt-2">
          Drag & drop or click to choose
        </p>
        <p className="text-sm text-gray-400">
          Supported: mp3, wav, m4a. Max 25MB
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

      {/* Files List */}
      {files.length > 0 && (
        <div className="mt-4 overflow-x-auto pb-2">
          <div className="flex space-x-4">
            {files.map(({ id, file }) => (
              <div
                key={id}
                className="relative min-w-[160px] max-w-[160px] rounded-lg border-2 border-purple-400 bg-white p-3 flex-shrink-0 shadow-md"
              >
                {/* Delete Button */}
                <button
                  onClick={() => removeFile(id)}
                  className="absolute top-1 right-1 p-1 rounded-full bg-white hover:bg-red-100 border border-red-300"
                >
                  <TrashIcon className="w-4 h-4 text-red-500" />
                </button>

                {/* File Info */}
                <p className="text-sm font-semibold truncate">{file.name}</p>
                <p className="text-xs text-gray-500">
                  {formatBytes(file.size)} •{" "}
                  {file.type.split("/")[1] || "unknown"}
                </p>

                {/* Placeholder for Progress */}
                <div className="mt-2 w-full bg-gray-200 h-1 rounded">
                  <div
                    className="bg-purple-500 h-1 rounded animate-pulse"
                    style={{ width: "60%" }} // simulate upload progress
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default FileUpload;
