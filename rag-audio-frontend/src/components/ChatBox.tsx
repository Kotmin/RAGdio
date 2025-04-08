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
import { streamChatResponse } from "../hooks/useStreamingChat";
// import LoadingDots from "react-loading-dots";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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
  const containerRef = useRef<HTMLDivElement | null>(null);
  const [chatId, setChatId] = useState<string>(() => {
    const existing = localStorage.getItem("chat_id");
    if (existing) return existing;
    const newId = crypto.randomUUID();
    localStorage.setItem("chat_id", newId);
    return newId;
  });

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userId = crypto.randomUUID();
    const aiId = crypto.randomUUID();

    let currentChatId = chatId;
    if (!currentChatId) {
      currentChatId = crypto.randomUUID();
      setChatId(currentChatId);
    }

    setMessages((prev) => [
      ...prev,
      { id: userId, sender: "user", content: input },
      { id: aiId, sender: "ai", content: "", streaming: true },
    ]);

    setInput("");
    setLoading(true);

    await streamChatResponse(input, "default", {
      chatId: currentChatId,
      onToken: (chunk) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === aiId ? { ...m, content: (m.content || "") + chunk } : m
          )
        );
      },
      onDone: (metadata) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === aiId ? { ...m, streaming: false, metadata } : m
          )
        );
        setLoading(false);
      },
      onError: (err) => {
        setMessages((prev) =>
          prev.map((m) =>
            m.id === aiId
              ? {
                  ...m,
                  streaming: false,
                  content: `⚠️ Error: ${err}`,
                }
              : m
          )
        );
        setLoading(false);
      },
    });
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
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

  const clearChat = () => {
    setMessages([]);
    setInput("");
  };

  const isScrolledToBottom = () => {
    const el = containerRef.current;
    return el ? el.scrollHeight - el.scrollTop - el.clientHeight < 50 : false;
  };

  useEffect(() => {
    if (isScrolledToBottom()) {
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, loading]);

  return (
    <div className="flex flex-col h-[80vh] bg-white dark:bg-gray-900 border border-gray-300 dark:border-gray-700 rounded-xl shadow overflow-hidden">
      {/* Chat area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4" ref={containerRef}>
        {messages.map((msg, idx) => {
          const isUser = msg.sender === "user";
          const previous = messages[idx - 1];
          const isNewBlock = !previous || previous.sender !== msg.sender;

          return (
            <div
              key={msg.id}
              className={`flex ${isUser ? "justify-end" : "justify-start"} ${
                isNewBlock ? "mt-6 mb-4" : "my-"
              }`}
            >
              <div
                className={`max-w-[80%] px-4 py-2 rounded-2xl text-sm whitespace-pre-wrap relative ${
                  isUser
                    ? "bg-white border-2 border-purple-400 text-gray-800 dark:bg-gray-900 dark:text-white"
                    : "bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-100"
                }`}
              >
                <div className="mt-4 mb-4 prose prose-sm dark:prose-invert max-w-none break-words whitespace-pre-wrap">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      code({ node, inline, className, children, ...props }) {
                        return (
                          <code
                            className={`rounded px-1 py-0.5 text-sm ${
                              inline
                                ? "bg-gray-100 dark:bg-gray-800"
                                : "block bg-gray-900 text-white p-2 overflow-auto"
                            }`}
                            {...props}
                          >
                            {children}
                          </code>
                        );
                      },
                    }}
                  >
                    {msg.content || ""}
                  </ReactMarkdown>
                </div>

                {/* Copy to clipboard */}
                {msg.sender === "ai" && !msg.streaming && (
                  <button
                    onClick={() => handleCopy(msg.id, msg.content)}
                    className="absolute top-2 right-2 flex items-center gap-1 text-xs text-gray-400 hover:text-purple-500"
                    title="Copy to clipboard"
                  >
                    {copiedId === msg.id ? (
                      <>
                        <CheckCircleIcon className="w-4 h-4 text-green-500" />
                        <span className="text-green-500">Copied!</span>
                      </>
                    ) : (
                      <>
                        <ClipboardIcon className="w-4 h-4" />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                )}

                {/* Metadata toggle */}
                {msg.sender === "ai" && msg.metadata && !msg.streaming && (
                  <div className="mt-1 mb-4 flex justify-end pr-10">
                    <button
                      onClick={() => toggleMetadata(msg.id)}
                      className="text-gray-400 hover:text-purple-500 text-xs flex items-center gap-1"
                      title="Toggle metadata"
                    >
                      {msg.showMetadata ? (
                        <ChevronUpIcon className="w-4 h-4 inline-block" />
                      ) : (
                        <ChevronDownIcon className="w-4 h-4 inline-block" />
                      )}
                      <span>Metadata</span>
                    </button>
                  </div>
                )}

                {/* Metadata display */}
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
          );
        })}

        {loading && (
          <div className="text-sm text-gray-500 dark:text-gray-400">
            Assistant is typing...{" "}
            {/* <button className="ml-2 underline text-xs">Stop</button> */}
          </div>
          // <div className="text-sm text-gray-400 dark:text-gray-500 flex items-center gap-2">
          //   Assistant is typing <LoadingDots dots={3} />
          // </div>
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

      {/* Footer */}
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
