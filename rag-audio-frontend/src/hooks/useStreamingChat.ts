interface StreamingOptions {
  onToken: (token: string) => void;
  onDone?: (metadata?: Record<string, any>) => void;
  onError?: (err: string) => void;
}

const API_URL = import.meta.env.VITE_API_BASE_URL || "/api/";

export async function streamChatResponse(
  prompt: string,
  ragModel: string = "default",
  options: StreamingOptions
) {
  try {
    const res = await fetch(`${API_URL}/llm/chat/stream`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, ragModel }),
    });

    if (!res.body) throw new Error("No response body");

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      if (!value) continue;

      const chunk = decoder.decode(value, { stream: true });
      buffer += chunk;

      const endMarker = "\n[END_METADATA] ";
      if (buffer.includes(endMarker)) {
        const [textPart, metadataPart] = buffer.split(endMarker);
        options.onToken(textPart);
        try {
          const parsed = JSON.parse(metadataPart.trim());
          options.onDone?.(parsed);
        } catch {
          options.onDone?.({});
        }
        break;
      }

      // options.onToken(chunk);
    }
  } catch (err: any) {
    console.error("Streaming error:", err);
    options.onError?.(err.message || "Streaming failed");
  }
}
