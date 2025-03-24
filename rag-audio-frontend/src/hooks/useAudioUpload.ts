import { useState } from "react";
import { toast } from "react-toastify";

const API_URL = import.meta.env.VITE_API_BASE_URL || "/api";

interface UploadResult {
  filename: string;
  transcription?: string;
  error?: string;
}

export function useAudioUpload() {
  const [loading, setLoading] = useState(false);

  const uploadFiles = async (
    files: File[],
    language?: string,
    rag?: string,
    _onProgress?: (file: File, percent: number) => void,
    onSuccess?: (filename: string, transcription: string) => void
  ) => {
    if (!files.length) {
      toast.error("Please select at least one file.");
      return;
    }

    setLoading(true);

    try {
      const formData = new FormData();
      for (const file of files) {
        formData.append("files", file);
      }
      if (language) formData.append("language", language);
      if (rag) formData.append("rag", rag);

      const response = await fetch(`${API_URL}/audio/upload_audio/`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(`Upload failed: ${errText}`);
      }

      const data = await response.json();

      if (!data.results || !Array.isArray(data.results)) {
        throw new Error("Invalid response from server.");
      }

      data.results.forEach((result: UploadResult) => {
        if (result.error) {
          toast.error(`❌ ${result.filename}: ${result.error}`);
        } else if (result.transcription) {
          onSuccess?.(result.filename, result.transcription);
          toast.success(`✅ ${result.filename} transcribed`);
        } else {
          toast.warn(
            `⚠️ ${result.filename}: No transcription or error received`
          );
        }
      });
    } catch (err: any) {
      toast.error(err.message || "Unknown upload error");
      console.error("Upload error:", err);
    } finally {
      setLoading(false);
    }
  };

  return { uploadFiles, loading };
}
