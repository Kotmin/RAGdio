import { useRef, useState } from "react";
import AudioUploadSection from "./AudioUploadSection";
import { useAudioUpload } from "../hooks/useAudioUpload";
import { toast } from "react-toastify";
import UploadResultModal from "./UploadResultModal";

export default function UploadPageForm() {
  const [files, setFiles] = useState<File[]>([]);
  const languageRef = useRef<HTMLSelectElement | null>(null);
  const ragRef = useRef<HTMLSelectElement | null>(null);
  const [pendingResult, setPendingResult] = useState<{
    filename: string;
    transcription: string;
  } | null>(null);

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
      undefined, // onProgress — not used yet
      (filename, transcription) => {
        setPendingResult({ filename, transcription });
      }
    );
  };

  const handleSendToRAG = () => {
    // Future: Call backend RAG-save endpoint here
    toast.success("Saved to RAG!");
    setPendingResult(null);
  };

  const handleDiscard = () => {
    toast.info("Transcription discarded.");
    setPendingResult(null);
  };

  return (
    <>
      <form
        onSubmit={handleSubmit}
        className="space-y-6 w-full max-w-3xl mx-auto"
      >
        <h1 className="text-2xl font-bold text-center">
          Upload Audio for Transcription + RAG
        </h1>

        {/* Audio File Section */}
        <AudioUploadSection files={files} setFiles={setFiles} />

        {/* Language */}
        <div>
          <label className="block mb-1 font-medium text-sm text-gray-700">
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
          <label className="block mb-1 font-medium text-sm text-gray-700">
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
      {pendingResult && (
        <UploadResultModal
          filename={pendingResult.filename}
          transcription={pendingResult.transcription}
          onSend={handleSendToRAG}
          onCancel={handleDiscard}
        />
      )}
    </>
  );
}
