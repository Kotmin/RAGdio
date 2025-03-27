import { useState, useEffect } from "react";
import ChatBox from "./components/ChatBox";
import UploadPageForm from "./components/UploadPageForm";
import { Menu, Close, DarkMode, LightMode } from "@mui/icons-material";
import {
  IconButton,
  Drawer,
  Divider,
  AppBar,
  Toolbar,
  Typography,
  useTheme,
  useMediaQuery,
} from "@mui/material";

function App() {
  const [openDrawer, setOpenDrawer] = useState(false);
  const [darkMode, setDarkMode] = useState(
    () => localStorage.getItem("darkMode") === "true"
  );

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));

  // Toggle Tailwind dark mode class
  useEffect(() => {
    document.documentElement.classList.toggle("dark", darkMode);
    localStorage.setItem("darkMode", String(darkMode));
  }, [darkMode]);

  return (
    <div className="min-h-screen w-full flex flex-col bg-gray-100 dark:bg-gray-900 text-gray-800 dark:text-gray-100 overflow-x-hidden">
      {/* Header */}
      <AppBar
        position="static"
        color="default"
        className="shadow-sm dark:bg-gray-800"
      >
        <Toolbar className="flex justify-between items-center">
          <Typography
            variant="h6"
            className="text-purple-700 dark:text-purple-400 font-bold"
          >
            🧠 RAG Over Audio
          </Typography>
          <div className="flex items-center gap-2">
            <IconButton
              aria-label="Toggle dark mode"
              onClick={() => setDarkMode((prev) => !prev)}
            >
              {darkMode ? <LightMode /> : <DarkMode />}
            </IconButton>
            <IconButton onClick={() => setOpenDrawer(true)} aria-label="Upload">
              <Menu />
            </IconButton>
          </div>
        </Toolbar>
      </AppBar>

      {/* Scrollable Main Area */}
      <main className="flex-1 overflow-y-auto px-4 py-6 flex justify-center">
        <div className="w-full max-w-3xl">
          <ChatBox />
        </div>
      </main>

      {/* Upload Sidebar Drawer */}
      <Drawer
        anchor="right"
        open={openDrawer}
        onClose={() => setOpenDrawer(false)}
        PaperProps={{
          className:
            "w-full max-w-md overflow-y-auto bg-white dark:bg-gray-800",
        }}
      >
        <div className="p-4 min-h-screen">
          <div className="flex items-center justify-between mb-2">
            <h2 className="text-lg font-bold">Upload Audio</h2>
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
