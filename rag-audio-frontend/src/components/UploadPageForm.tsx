import { useRef, useState, useEffect } from "react";
import AudioUploadSection from "./AudioUploadSection";
import { useAudioUpload } from "../hooks/useAudioUpload";
import { toast } from "react-toastify";
import UploadResultModal from "./UploadResultModal";

interface TranscriptionResult {
  filename: string;
  transcription: string;
}

export default function UploadPageForm() {
  const [files, setFiles] = useState<File[]>([]);
  const [pendingResults, setPendingResults] = useState<TranscriptionResult[]>(
    []
  );
  const [currentResult, setCurrentResult] =
    useState<TranscriptionResult | null>(null);

  const languageRef = useRef<HTMLSelectElement | null>(null);
  const ragRef = useRef<HTMLSelectElement | null>(null);
  const { uploadFiles, loading } = useAudioUpload();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!files.length) {
      toast.error("Please add files before submitting.");
      return;
    }
    const language = languageRef.current?.value;
    const rag = ragRef.current?.value;

    await uploadFiles(
      files,
      language,
      rag,
      undefined,
      (filename, transcription) => {
        setPendingResults((prev) => [...prev, { filename, transcription }]);
      }
    );
  };

  // Show next modal when one is dismissed
  useEffect(() => {
    if (!currentResult && pendingResults.length > 0) {
      const [next, ...rest] = pendingResults;
      setCurrentResult(next);
      setPendingResults(rest);
    }
  }, [currentResult, pendingResults]);

  const handleSendToRAG = () => {
    toast.success(`Saved ${currentResult?.filename} to RAG`);
    setCurrentResult(null); // triggers effect to show next
  };

  const handleDiscard = () => {
    toast.info(`Discarded ${currentResult?.filename}`);
    setCurrentResult(null); // triggers effect to show next
  };

  return (
    <div className="w-full min-h-screen overflow-y-auto px-4">
      <form
        onSubmit={handleSubmit}
        className="space-y-6 w-full max-w-3xl mx-auto pb-10"
      >
        <h1 className="text-2xl font-bold text-center">
          Upload Audio for Transcription + RAG
        </h1>

        {/* Audio File Section */}
        <AudioUploadSection files={files} setFiles={setFiles} />

        {/* Language */}
        <div>
          <label className="block mb-1 font-medium text-sm text-gray-700 dark:text-gray-200">
            Language
          </label>
          <select
            ref={languageRef}
            className="w-full rounded border px-3 py-2"
            defaultValue="en"
          >
            <option value="en">English</option>
            <option value="pl">Polish</option>
            <option value="es">Spanish</option>
            <option value="fr">French</option>
            <option value="de">German</option>
          </select>
        </div>

        {/* RAG selector */}
        <div>
          <label className="block mb-1 font-medium text-sm text-gray-700 dark:text-gray-200">
            RAG Model
          </label>
          <select
            ref={ragRef}
            className="w-full rounded border px-3 py-2"
            defaultValue="default"
          >
            <option value="default">Default (Qdrant + GPT-4)</option>
            <option value="local">Local Model</option>
          </select>
        </div>

        <button
          type="submit"
          className="w-full bg-cyan-700 text-white px-4 py-2 rounded hover:bg-cyan-600 transition"
          disabled={loading}
        >
          {loading ? "Uploading..." : "Submit & Process"}
        </button>
      </form>

      {/* Result Modal */}
      {currentResult && (
        <UploadResultModal
          filename={currentResult.filename}
          transcription={currentResult.transcription}
          onSend={handleSendToRAG}
          onCancel={handleDiscard}
        />
      )}
    </div>
  );
}
