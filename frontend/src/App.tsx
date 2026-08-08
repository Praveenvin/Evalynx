import { Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import ResumeScreening from "./pages/ResumeScreening";
import MockInterview from "./pages/MockInterview";

export default function App() {
  return (
    <div className="min-h-screen bg-canvas">
      <Navbar />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/resume-screening" element={<ResumeScreening />} />
        <Route path="/mock-interview" element={<MockInterview />} />
      </Routes>
    </div>
  );
}
