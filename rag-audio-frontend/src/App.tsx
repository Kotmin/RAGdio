import { useState } from "react";
import ChatBox from "./components/ChatBox";
import UploadPageForm from "./components/UploadPageForm";
import { Menu, Close } from "@mui/icons-material";
import { IconButton, Drawer, Divider } from "@mui/material";

function App() {
  const [openDrawer, setOpenDrawer] = useState(false);

  return (
    <div className="min-h-screen w-full bg-gray-100 flex flex-col items-center">
      {/* Header */}
      <div className="w-full flex items-center justify-between px-4 py-3 bg-white shadow-md">
        <h1 className="text-xl font-semibold text-purple-700">
          🧠 RAG Over Audio
        </h1>
        <IconButton onClick={() => setOpenDrawer(true)} aria-label="Upload">
          <Menu />
        </IconButton>
      </div>

      {/* Main chat layout */}
      <div className="w-full max-w-3xl px-4 py-6">
        <ChatBox />
      </div>

      {/* Upload Sidebar */}
      <Drawer
        anchor="right"
        open={openDrawer}
        onClose={() => setOpenDrawer(false)}
        PaperProps={{ className: "w-full max-w-md" }}
      >
        <div className="p-4">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-bold text-gray-700">Upload Audio</h2>
            <IconButton onClick={() => setOpenDrawer(false)}>
              <Close />
            </IconButton>
          </div>
          <Divider className="mb-4" />
          <UploadPageForm />
        </div>
      </Drawer>
    </div>
  );
}

export default App;
