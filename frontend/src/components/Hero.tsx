import React from 'react';
import { Terminal } from './Terminal';
import { Download, Play } from 'lucide-react';

export function Hero() {
    return (
        <section id="home" className="pt-32 pb-20 px-6 min-h-screen flex items-center relative overflow-hidden">
            <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative z-10">
                <div>
                    <h1 className="text-5xl md:text-6xl font-extrabold mb-6 leading-tight text-white">
                        The <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-400 to-fuchsia-400">Next Generation</span><br />
                        AI Terminal is Here
                    </h1>
                    <p className="text-lg text-slate-300 mb-8 max-w-xl leading-relaxed">
                        Experience next-generation AI with AetherAI - A revolutionary multi-model terminal assistant
                        supporting 8+ AI models including Gemini, Groq, HuggingFace, DeepSeek, Ollama, Claude, GPT, and more.
                    </p>

                    <div className="flex flex-wrap gap-4 mb-12">
                        <button
                            onClick={() => document.getElementById('download')?.scrollIntoView({ behavior: 'smooth' })}
                            className="bg-gradient-to-r from-indigo-500 to-fuchsia-500 text-white px-8 py-4 rounded-xl font-bold shadow-lg shadow-indigo-500/25 hover:scale-105 transition-all flex items-center gap-2"
                        >
                            <Download className="w-5 h-5" /> Download Now
                        </button>
                        <button
                            onClick={() => window.open('https://www.youtube.com/watch?v=DLyrTzcYgbI', '_blank')}
                            className="border-2 border-indigo-400/50 text-white px-8 py-4 rounded-xl font-bold hover:bg-indigo-400/10 hover:border-indigo-400 transition-all flex items-center gap-2"
                        >
                            <Play className="w-5 h-5" /> Live Demo
                        </button>
                    </div>

                    <div className="grid grid-cols-3 gap-8 border-t border-white/10 pt-8">
                        <div className="text-center">
                            <span className="text-3xl font-bold text-indigo-400 block">2.5k+</span>
                            <span className="text-sm text-slate-400">Downloads</span>
                        </div>
                        <div className="text-center">
                            <span className="text-3xl font-bold text-indigo-400 block">8+</span>
                            <span className="text-sm text-slate-400">AI Models</span>
                        </div>
                        <div className="text-center">
                            <span className="text-3xl font-bold text-indigo-400 block">99%</span>
                            <span className="text-sm text-slate-400">Uptime</span>
                        </div>
                    </div>
                </div>

                <div className="relative">
                    <div className="absolute -inset-1 bg-gradient-to-r from-indigo-500 to-fuchsia-500 rounded-2xl blur opacity-20 animate-pulse"></div>
                    <Terminal />
                </div>
            </div>
        </section>
    );
}
