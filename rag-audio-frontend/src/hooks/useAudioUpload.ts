import { useState } from "react";
import { toast } from "react-toastify";

const API_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export function useAudioUpload() {
  const [loading, setLoading] = useState(false);

  const uploadFiles = async (
    files: File[],
    language?: string,
    rag?: string,
    onProgress?: (file: File, percent: number) => void,
    onSuccess?: (filename: string, transcription: string) => void
  ) => {
    if (!files.length) {
      toast.error("Please select at least one file.");
      return;
    }

    setLoading(true);

    try {
      for (const file of files) {
        const formData = new FormData();
        formData.append("file", file);
        if (language) formData.append("language", language);
        if (rag) formData.append("rag", rag);

        const response = await fetch(`${API_URL}/audio/upload_audio/`, {
          method: "POST",
          body: formData,
        });

        if (!response.ok) {
          let errorMessage = `Upload failed for ${file.name}`;
          try {
            const errData = await response.json();
            errorMessage += `: ${errData.detail}`;
          } catch {
            const errText = await response.text();
            errorMessage += `: ${errText}`;
          }
          throw new Error(errorMessage);
        }

        // ✅ Safe JSON parse
        let data: { filename?: string; transcription?: string };
        try {
          data = await response.json();
          console.log("✅ Upload success:", data);
        } catch (err) {
          throw new Error(`Upload succeeded but response is not valid JSON.`);
        }

        if (!data.transcription || !data.filename) {
          throw new Error(`Upload succeeded but missing data in response.`);
        }

        // Show modal per file
        if (onSuccess) {
          onSuccess(data.filename, data.transcription);
        }

        toast.success(`Uploaded ${file.name} ✅`);
      }
    } catch (err: any) {
      console.error("Upload error2:", err);
      toast.error(err.message || "Unknown upload error.");
    } finally {
      setLoading(false);
    }
  };

  return { uploadFiles, loading };
}
