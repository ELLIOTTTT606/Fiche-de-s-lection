import { Route, Routes } from "react-router-dom";
import AnimatedBackground from "./components/layout/AnimatedBackground";
import Navigation from "./components/layout/Navigation";
import Home from "./pages/Home";
import Machine from "./pages/Machine";
import Projet from "./pages/Projet";
import Contacts from "./pages/Contacts";
import Options from "./pages/Options";
import Generate from "./pages/Generate";
import Maintenance from "./pages/Maintenance";

export default function App() {
  return (
    <>
      <AnimatedBackground />
      <Navigation />
      <main className="mx-auto max-w-6xl px-4 py-8">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/machine" element={<Machine />} />
          <Route path="/projet" element={<Projet />} />
          <Route path="/contacts" element={<Contacts />} />
          <Route path="/options" element={<Options />} />
          <Route path="/generate" element={<Generate />} />
          <Route path="/maintenance" element={<Maintenance />} />
        </Routes>
      </main>
      <footer className="mx-auto max-w-6xl px-4 py-8 text-center text-xs text-slate-400">
        INVENIO · France Air — Solution Habitat · 100% interne
      </footer>
    </>
  );
}
