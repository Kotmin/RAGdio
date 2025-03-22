import FileUpload from "./components/FileUpload";
import RAGSelector from "./components/RAGSelector";
import ChatBox from "./components/ChatBox";
import UploadPageForm from "./components/UploadPageForm";

// function App() {
//   return (
//     <div className="w-full max-w-4xl bg-white rounded-xl shadow-xl p-6 space-y-6">
//       <h1 className="text-3xl font-bold text-center text-gray-800">
//         🧠 RAG Over Audio
//       </h1>
//       <RAGSelector />
//       <FileUpload />

//       {/* <UploadPageForm /> */}
//       <ChatBox />
//       <div className="bg-red-300 p-4 text-white text-center">
//         If you see red, Tailwind works 🎯
//       </div>
//       <div className="bg-red-400 text-white p-4">Tailwind is working!</div>
//     </div>
//   );
// }

// export default App;

// import UploadPageForm from "./components/UploadPageForm";

function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 flex items-center justify-center px-4 py-8">
      <div className="w-full max-w-4xl bg-white rounded-xl shadow-lg p-6 space-y-6">
        <h1 className="text-3xl font-bold text-center text-gray-800">
          🧠 RAG Over Audio
        </h1>
        <UploadPageForm />
      </div>
    </div>
  );
}

export default App;
