import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Hero } from './components/Hero';
import { Features } from './components/Features';
import { HowItWorks } from './components/HowItWorks';
import { Pricing } from './components/Pricing';
import { FAQ } from './components/FAQ';
import { DownloadSection } from './components/DownloadSection';
import { CTA } from './components/CTA';
import { Footer } from './components/Footer';
import Documentation from './pages/Documentation';

function Landing() {
  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden relative font-sans antialiased">
      <Navbar />
      <Hero />
      <Features />
      <HowItWorks />
      <Pricing />
      <FAQ />
      <DownloadSection />
      <CTA />
      <Footer />
    </div>
  );
}

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/docs" element={<Documentation />} />
        <Route path="/docs/:slug" element={<Documentation />} />
      </Routes>
    </Router>
  );
}

export default App;
