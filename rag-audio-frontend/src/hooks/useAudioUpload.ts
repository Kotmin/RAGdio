import { useState } from "react";
import { toast } from "react-toastify";

const API_URL = import.meta.env.VITE_API_BASE_URL || "/api";

export function useAudioUpload() {
  const [loading, setLoading] = useState(false);

  const uploadFiles = async (
    files: File[],
    language?: string,
    rag?: string
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

        const res = await fetch(`${API_URL}/audio/upload_audio`, {
          method: "POST",
          body: formData,
        });

        if (!res.ok) {
          throw new Error(`Upload failed for ${file.name}`);
        }

        const result = await res.json();
        toast.success(`Uploaded ${file.name}`);
        console.log(result);
      }
    } catch (err: any) {
      toast.error(err.message || "Upload error occurred");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return { uploadFiles, loading };
}
