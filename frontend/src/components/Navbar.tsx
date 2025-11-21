import React, { useState } from 'react';
import { Menu, X, Github } from 'lucide-react';

export function Navbar() {
    const [isOpen, setIsOpen] = useState(false);

    return (
        <nav className="w-full bg-[#1e293b]/80 shadow-lg fixed top-0 left-0 z-50 backdrop-blur-md border-b border-white/10">
            <div className="max-w-7xl mx-auto flex justify-between items-center px-6 py-4">
                <div className="flex items-center gap-2 text-2xl font-bold cursor-pointer text-white">
                    <span className="text-indigo-400">🧠</span>
                    <span>AetherAI</span>
                </div>

                <div className="hidden md:flex gap-8 items-center text-sm font-medium text-slate-200">
                    <a href="#home" className="hover:text-indigo-400 transition-colors">Home</a>
                    <a href="#features" className="hover:text-indigo-400 transition-colors">Features</a>
                    <a href="#download" className="hover:text-indigo-400 transition-colors">Download</a>
                    <a href="docs.html" className="hover:text-indigo-400 transition-colors">Docs</a>
                    <a href="https://github.com/KunjShah95/NEXUS-AI.io" target="_blank" rel="noreferrer" className="hover:text-indigo-400 transition-colors">
                        <Github className="w-5 h-5" />
                    </a>
                </div>

                <div className="md:hidden flex items-center text-white cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
                    {isOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
                </div>
            </div>

            {isOpen && (
                <div className="md:hidden bg-[#1e293b] border-t border-white/10 absolute w-full">
                    <div className="flex flex-col gap-4 px-6 py-4 text-slate-200">
                        <a href="#home" className="hover:text-indigo-400 transition-colors" onClick={() => setIsOpen(false)}>Home</a>
                        <a href="#features" className="hover:text-indigo-400 transition-colors" onClick={() => setIsOpen(false)}>Features</a>
                        <a href="#download" className="hover:text-indigo-400 transition-colors" onClick={() => setIsOpen(false)}>Download</a>
                        <a href="docs.html" className="hover:text-indigo-400 transition-colors" onClick={() => setIsOpen(false)}>Docs</a>
                        <a href="https://github.com/KunjShah95/NEXUS-AI.io" target="_blank" rel="noreferrer" className="hover:text-indigo-400 transition-colors">
                            GitHub
                        </a>
                    </div>
                </div>
            )}
        </nav>
    );
}
