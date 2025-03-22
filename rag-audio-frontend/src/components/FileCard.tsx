import { TrashIcon, PaperClipIcon } from "@heroicons/react/24/solid";

interface FileCardProps {
  file: File;
  onRemove: () => void;
}

export default function FileCard({ file, onRemove }: FileCardProps) {
  const formatBytes = (bytes: number) => {
    const k = 1024;
    const sizes = ["Bytes", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
  };

  return (
    <div className="relative min-w-[110px] max-w-[110px] h-[150px] border-2 border-purple-400 rounded-lg p-2 bg-white shadow-md flex flex-col items-center">
      {/* Delete Button */}
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

      <PaperClipIcon className="w-6 h-6 text-purple-400 mt-4 mb-2" />

      <p className="text-xs font-semibold text-center px-1 leading-tight line-clamp-2 break-all">
        {file.name}
      </p>
      <p className="text-[10px] text-gray-400 text-center mt-1">
        {file.type.split("/")[1] || "unknown"}
      </p>
      <p className="text-[10px] text-gray-500 text-center">
        {formatBytes(file.size)}
      </p>
    </div>
  );
}
