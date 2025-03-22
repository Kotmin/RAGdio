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

  return (
    <div className="w-full">
      <div
        onClick={() => inputRef.current?.click()}
        onDrop={onDrop}
        onDragOver={(e) => e.preventDefault()}
        className="group relative w-full border-4 border-dashed rounded-xl p-6 text-center transition-all cursor-pointer neon-border hover:shadow-lg"
      >
        <CloudArrowUpIcon className="w-7 h-7 mx-auto text-purple-600 group-hover:scale-105 transition-transform" />
        <p className="text-gray-700 font-medium mt-2">
          Drop or click to upload
        </p>
        <p className="text-sm text-gray-400">
          Supports mp3, wav, m4a (max 25MB)
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

      {files.length > 0 && (
        <div className="mt-4 space-y-2">
          {files.map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between bg-white border rounded p-2 shadow-sm hover:bg-gray-50 transition"
            >
              <div className="text-sm truncate max-w-[75%]">
                {item.file.name}
              </div>
              <button
                onClick={() => removeFile(item.id)}
                className="hover:scale-105 transition-transform"
              >
                <TrashIcon className="w-5 h-5 text-red-500 hover:text-red-700" />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default FileUpload;
