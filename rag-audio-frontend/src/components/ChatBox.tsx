import { useRef, useState, useEffect } from "react";
import {
  PaperAirplaneIcon,
  MicrophoneIcon,
  Cog6ToothIcon,
  ChevronDownIcon,
  ChevronUpIcon,
  ClipboardIcon,
  CheckCircleIcon,
} from "@heroicons/react/24/solid";

const API_URL = import.meta.env.VITE_API_BASE_URL || "/api/";

interface Message {
  id: string;
  sender: "user" | "ai";
  content: string;
  streaming?: boolean;
  metadata?: Record<string, any>;
  showMetadata?: boolean;
}

export default function ChatBox() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [showFooter, setShowFooter] = useState(false);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const bottomRef = useRef<HTMLDivElement | null>(null);

  const animateAssistantReply = (
    fullText: string,
    msgId: string,
    metadata?: Record<string, any>
  ) => {
    let i = 0;
    const interval = setInterval(() => {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === msgId ? { ...m, content: fullText.slice(0, i) } : m
        )
      );

      if (i >= fullText.length) {
        clearInterval(interval);
        setMessages((prev) =>
          prev.map((m) =>
            m.id === msgId
              ? { ...m, content: fullText, streaming: false, metadata }
              : m
          )
        );
      }

      i++;
    }, 5);
  };

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userId = crypto.randomUUID();
    const aiId = crypto.randomUUID();

    const userMessage: Message = {
      id: userId,
      sender: "user",
      content: input,
    };
    const aiPlaceholder: Message = {
      id: aiId,
      sender: "ai",
      content: "",
      streaming: true,
    };

    setMessages((prev) => [...prev, userMessage, aiPlaceholder]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/llm/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: input }),
      });

      if (!res.ok) {
        throw new Error(`Server error (${res.status})`);
      }

      const data = await res.json();
      animateAssistantReply(data.response, aiId, data.metadata || {});
    } catch (err: any) {
      console.error("LLM Error:", err);
      setMessages((prev) =>
        prev.map((m) =>
          m.id === aiId
            ? {
                ...m,
                content: `⚠️ Error fetching assistant response: ${err.message}`,
                streaming: false,
              }
            : m
        )
      );
    } finally {
      setLoading(false);
    }
  };

  const toggleMetadata = (msgId: string) => {
    setMessages((prev) =>
      prev.map((msg) =>
        msg.id === msgId ? { ...msg, showMetadata: !msg.showMetadata } : msg
      )
    );
  };

  const handleCopy = (msgId: string, content: string) => {
    navigator.clipboard.writeText(content);
    setCopiedId(msgId);
    setTimeout(() => setCopiedId(null), 1500);
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const clearChat = () => {
    setMessages([]);
    setInput("");
  };

  return (
    <div className="flex flex-col h-[80vh] bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-xl shadow overflow-hidden">
      {/* Chat area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`flex ${
              msg.sender === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] px-4 py-2 rounded-2xl text-sm whitespace-pre-wrap relative ${
                msg.sender === "user"
                  ? "bg-white border-2 border-purple-400 text-gray-800 dark:bg-gray-900 dark:text-white"
                  : "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100"
              }`}
            >
              {msg.content}

              {/* Clipboard copy button */}
              {msg.sender === "ai" && !msg.streaming && (
                <button
                  onClick={() => handleCopy(msg.id, msg.content)}
                  className="absolute top-1 right-2 text-gray-400 hover:text-purple-500 text-xs"
                  title="Copy to clipboard"
                >
                  {copiedId === msg.id ? (
                    <CheckCircleIcon className="w-4 h-4 text-green-500" />
                  ) : (
                    <ClipboardIcon className="w-4 h-4" />
                  )}
                </button>
              )}

              {/* Metadata toggle button (only AI) */}
              {msg.sender === "ai" && !msg.streaming && msg.metadata && (
                <button
                  onClick={() => toggleMetadata(msg.id)}
                  className="absolute bottom-1 right-2 text-gray-400 hover:text-purple-500 text-xs"
                  title="Toggle metadata"
                >
                  {msg.showMetadata ? (
                    <ChevronUpIcon className="w-4 h-4 inline-block" />
                  ) : (
                    <ChevronDownIcon className="w-4 h-4 inline-block" />
                  )}
                </button>
              )}

              {/* Metadata content */}
              {msg.sender === "ai" &&
                msg.metadata &&
                msg.showMetadata &&
                !msg.streaming && (
                  <pre className="text-xs mt-2 p-2 rounded bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 max-h-40 overflow-auto">
                    {JSON.stringify(msg.metadata, null, 2)}
                  </pre>
                )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Assistant is typing...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="px-4 py-3 border-t border-gray-200 dark:border-gray-700 space-y-2">
        <div className="flex items-end gap-2">
          <textarea
            rows={3}
            className="flex-1 resize-none rounded-md border px-3 py-2 text-sm dark:bg-gray-800 dark:text-white border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-400"
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
          />
          <button
            onClick={sendMessage}
            className="p-2 bg-purple-600 hover:bg-purple-700 text-white rounded-md flex items-center justify-center"
            title="Send"
          >
            <PaperAirplaneIcon className="w-5 h-5 rotate-45" />
          </button>
        </div>

        {/* Chat actions + settings */}
        <div className="flex justify-between items-center text-xs text-gray-400">
          <div className="flex gap-2">
            <button onClick={clearChat} className="hover:text-red-500">
              Clear chat
            </button>
            <button
              onClick={() => setMessages([])}
              className="hover:text-blue-500"
            >
              New topic
            </button>
          </div>

          <div className="flex gap-3 items-center">
            <button
              className="text-gray-400 dark:text-gray-500 cursor-not-allowed"
              disabled
              title="Speech input coming soon"
            >
              <MicrophoneIcon className="w-4 h-4" />
            </button>
            <button
              onClick={() => setShowFooter((prev) => !prev)}
              className="hover:text-purple-500 text-gray-400 dark:text-gray-500"
              title="Toggle chat settings"
            >
              <Cog6ToothIcon className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Expandable footer */}
      {showFooter && (
        <div className="border-t border-gray-200 dark:border-gray-700 p-4 bg-gray-50 dark:bg-gray-800 text-sm text-gray-700 dark:text-gray-200 space-y-3">
          <p className="font-semibold text-xs">⚙️ Settings & Info</p>

          <div className="text-xs space-y-1">
            <p className="text-gray-500 dark:text-gray-400">
              🧠 <strong>Model selector</strong> — coming soon
            </p>
            <p className="text-gray-500 dark:text-gray-400">
              📄 <strong>RAG support</strong> — in development
            </p>
            <p className="text-gray-500 dark:text-gray-400">
              🔊 <strong>Speech input</strong> — not available yet
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
