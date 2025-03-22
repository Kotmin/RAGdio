import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import "../index.css";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-gray-50 to-gray-100">
      <App />
    </div>
  </React.StrictMode>
);
