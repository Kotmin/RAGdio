import FileUpload from "./components/FileUpload";
import RAGSelector from "./components/RAGSelector";
import ChatBox from "./components/ChatBox";

function App() {
  return (
    <div className="w-full max-w-4xl bg-white rounded-xl shadow-xl p-6 space-y-6 m-4">
      <h1 className="text-3xl font-bold text-center text-gray-800">
        🧠 RAG Over Audio
      </h1>
      <RAGSelector />
      <FileUpload />
      <ChatBox />
    </div>
  );
}

export default App;
