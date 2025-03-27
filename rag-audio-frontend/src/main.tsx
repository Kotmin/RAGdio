import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { ToastContainer } from "react-toastify";
import { CssBaseline } from "@mui/material";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import "react-toastify/dist/ReactToastify.css";
import "../index.css";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#9333ea" }, // Purple accent
    background: {
      default: "#f9fafb",
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <App />
      <ToastContainer position="bottom-right" />
    </ThemeProvider>
  </React.StrictMode>
);
