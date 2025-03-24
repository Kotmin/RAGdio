import {
  XMarkIcon,
  CheckCircleIcon,
  TrashIcon,
} from "@heroicons/react/24/solid";

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
    <div className="fixed inset-0 bg-black bg-opacity-40 backdrop-blur-sm flex items-center justify-center z-50">
      <div className="bg-white rounded-lg shadow-xl p-6 max-w-md w-full relative space-y-4">
        <button
          onClick={onCancel}
          className="absolute top-2 right-2 text-gray-400 hover:text-gray-600"
        >
          <XMarkIcon className="w-5 h-5" />
        </button>

        <h3 className="text-lg font-semibold text-gray-800 text-center">
          Transcription for: <span className="text-purple-600">{filename}</span>
        </h3>

        <div className="max-h-60 overflow-y-auto border rounded p-2 text-sm bg-gray-50">
          <pre className="whitespace-pre-wrap">{transcription}</pre>
        </div>

        <div className="flex justify-between pt-2">
          <button
            onClick={onSend}
            className="flex items-center gap-1 bg-green-600 text-white px-3 py-1 rounded hover:bg-green-700 text-sm"
          >
            <CheckCircleIcon className="w-4 h-4" />
            Save to RAG
          </button>
          <button
            onClick={onCancel}
            className="flex items-center gap-1 bg-red-500 text-white px-3 py-1 rounded hover:bg-red-600 text-sm"
          >
            <TrashIcon className="w-4 h-4" />
            Discard
          </button>
        </div>
      </div>
    </div>
  );
}
