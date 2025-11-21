import React from 'react';
import { Github, Twitter, Linkedin, Book } from 'lucide-react';

export function Footer() {
    return (
        <footer className="w-full py-8 bg-[#1e293b] border-t border-indigo-400/10 mt-16">
            <div className="max-w-4xl mx-auto px-6 text-center">
                <div className="mb-8 flex flex-col md:flex-row justify-center gap-4">
                    <a href="docs.html" className="inline-flex items-center justify-center gap-2 bg-gradient-to-r from-indigo-500 to-fuchsia-500 text-white px-6 py-3 rounded-xl font-bold shadow-xl hover:scale-105 transition">
                        <Book className="w-5 h-5" /> Complete Documentation
                    </a>
                    <a href="https://github.com/KunjShah95/NEXUS-AI.io" target="_blank" rel="noreferrer" className="inline-flex items-center justify-center gap-2 border-2 border-indigo-400 text-white px-6 py-3 rounded-xl font-bold shadow hover:border-fuchsia-400 transition">
                        <Github className="w-5 h-5" /> View on GitHub
                    </a>
                </div>
                <div className="flex justify-center items-center gap-6 mb-4">
                    <span className="text-slate-400 text-lg hidden md:inline">Connect with me / Follow me on:</span>
                    <a href="https://twitter.com/INDIA_KUNJ" target="_blank" rel="noreferrer" title="Follow on Twitter" className="text-slate-400 hover:text-indigo-400 transition-colors">
                        <Twitter className="w-6 h-6" />
                    </a>
                    <a href="https://www.linkedin.com/in/kunjshah05/" target="_blank" rel="noreferrer" title="Connect on LinkedIn" className="text-slate-400 hover:text-indigo-400 transition-colors">
                        <Linkedin className="w-6 h-6" />
                    </a>
                    <a href="https://github.com/KunjShah95" target="_blank" rel="noreferrer" title="View on GitHub" className="text-slate-400 hover:text-indigo-400 transition-colors">
                        <Github className="w-6 h-6" />
                    </a>
                </div>
                <div className="mt-4 text-slate-400 text-sm">
                    &copy; 2025 AetherAI. All rights reserved.
                </div>
            </div>
        </footer>
    );
}
