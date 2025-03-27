import {
  XMarkIcon,
  CheckCircleIcon,
  TrashIcon,
} from "@heroicons/react/24/outline";

interface Props {
  filename: string;
  transcription: string;
  onSend: () => void;
  onCancel: () => void;
}

export default function UploadResultModal({
  filename,
  transcription,
  onSend,
  onCancel,
}: Props) {
  return (
    <div className="absolute inset-0 z-50 flex items-center justify-center bg-black bg-opacity-40 backdrop-blur-sm px-4 py-8">
      <div className="w-full max-w-md bg-white dark:bg-gray-800 rounded-xl shadow-lg p-6 space-y-5 relative text-gray-900 dark:text-gray-100">
        {/* Close */}
        <button
          onClick={onCancel}
          className="absolute top-3 right-3 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <XMarkIcon className="w-5 h-5" />
        </button>

        {/* Title */}
        <h3 className="text-base font-semibold text-center">
          Transcription of{" "}
          <span className="text-purple-600 break-words">{filename}</span>
        </h3>

        {/* Scrollable transcription box */}
        <div className="max-h-64 overflow-y-auto border border-gray-200 dark:border-gray-700 rounded-md p-3 text-sm bg-gray-50 dark:bg-gray-900 whitespace-pre-wrap leading-snug">
          {transcription}
        </div>

        {/* Buttons */}
        <div className="flex justify-between pt-2">
          <button
            onClick={onCancel}
            className="flex items-center gap-1 px-3 py-1.5 text-sm rounded bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 text-gray-700 dark:text-gray-100 border border-gray-300 dark:border-gray-600"
          >
            <TrashIcon className="w-4 h-4" />
            Discard
          </button>
          <button
            onClick={onSend}
            className="flex items-center gap-1 px-3 py-1.5 text-sm rounded bg-purple-600 hover:bg-purple-700 text-white shadow"
          >
            <CheckCircleIcon className="w-4 h-4" />
            Save to RAG
          </button>
        </div>
      </div>
    </div>
  );
}
