import { TrashIcon, PaperClipIcon } from "@heroicons/react/24/solid";

interface FileCardProps {
  file: File;
  onRemove: () => void;
}

export default function FileCard({ file, onRemove }: FileCardProps) {
  const formatBytes = (bytes: number) => {
    if (bytes === 0) return "0 Bytes (empty)";
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  const extension =
    file.type?.split("/")?.[1] || file.name.split(".").pop() || "unknown";

  return (
    <div className="relative min-w-[130px] max-w-[130px] h-[170px] border-2 border-purple-400 rounded-lg p-2 bg-white shadow-md flex flex-col items-center justify-between">
      {/* Remove button */}
      <button
        onClick={(e) => {
          e.stopPropagation();
          onRemove();
        }}
        className="absolute top-1 right-1 bg-red-500 rounded-full p-[2px] hover:bg-red-600 transition"
        title="Remove file"
      >
        <TrashIcon className="w-4 h-4 text-white" />
      </button>

      <PaperClipIcon className="w-6 h-6 text-purple-400 mt-4" />

      {/* Filename */}
      <p className="text-xs font-semibold text-center px-1 mt-1 leading-snug break-all line-clamp-2 w-full">
        {file.name}
      </p>

      {/* Extension */}
      <p className="text-[10px] text-gray-400">{extension}</p>

      {/* Size */}
      <p className="text-[10px] text-gray-500">{formatBytes(file.size)}</p>
    </div>
  );
}
