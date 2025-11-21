import React, { useState, useEffect, useRef } from 'react';

const commands = [
    'nexus --help',
    'nexus chat "Hello, how are you?"',
    'nexus model --list',
    'nexus config --set model=gemini',
    'nexus generate --prompt "Write a Python function"'
];

const responses = [
    'NEXUS AI Terminal v3.0\nUsage: nexus [command] [options]\n\nCommands:\n  chat      Start interactive chat\n  generate  Generate content\n  model     Manage AI models\n  config    Configuration settings',
    'AI: Hello! I\'m doing great, thank you for asking! How can I assist you today?',
    'Available Models:\n✓ Gemini Pro\n✓ Groq Llama\n✓ HuggingFace Transformers\n✓ DeepSeek Coder\n✓ Ollama Local\n✓ Claude Sonnet\n✓ GPT-4\n✓ Mistral AI',
    'Configuration updated successfully!\nActive model: Gemini Pro\nStatus: Ready',
    'def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\n# Generated with NEXUS AI'
];

export function Terminal() {
    const [text, setText] = useState('');
    const [output, setOutput] = useState<Array<{ command: string, response: string }>>([]);
    const [cmdIndex, setCmdIndex] = useState(0);
    const [charIndex, setCharIndex] = useState(0);
    const [isTyping, setIsTyping] = useState(true);
    const [showCursor, setShowCursor] = useState(true);
    const scrollRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const cursorInterval = setInterval(() => setShowCursor(prev => !prev), 500);
        return () => clearInterval(cursorInterval);
    }, []);

    useEffect(() => {
        if (scrollRef.current) {
            scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
        }
    }, [output, text]);

    useEffect(() => {
        if (!isTyping) return;

        if (charIndex < commands[cmdIndex].length) {
            const timeout = setTimeout(() => {
                setText(prev => prev + commands[cmdIndex][charIndex]);
                setCharIndex(prev => prev + 1);
            }, 50 + Math.random() * 50);
            return () => clearTimeout(timeout);
        } else {
            // Finished typing command
            setIsTyping(false);
            setTimeout(() => {
                setOutput(prev => [...prev, { command: commands[cmdIndex], response: responses[cmdIndex] }]);
                setText('');
                setCharIndex(0);
                setCmdIndex(prev => (prev + 1) % commands.length);
                setIsTyping(true);
            }, 1000);
        }
    }, [charIndex, cmdIndex, isTyping]);

    return (
        <div className="w-full max-w-lg mx-auto relative z-20">
            <div className="terminal-mockup shadow-2xl rounded-2xl border border-indigo-400/30 bg-[#1e293b]/90 backdrop-blur overflow-hidden transform transition-all hover:scale-[1.02] duration-500">
                <div className="flex items-center gap-3 px-4 py-2 border-b border-indigo-400/20 bg-[#1e293b]">
                    <div className="flex gap-2">
                        <span className="w-3 h-3 bg-red-400 rounded-full"></span>
                        <span className="w-3 h-3 bg-yellow-400 rounded-full"></span>
                        <span className="w-3 h-3 bg-green-400 rounded-full"></span>
                    </div>
                    <div className="text-xs text-slate-400 font-mono">AetherAI Terminal</div>
                </div>
                <div ref={scrollRef} className="px-6 py-6 font-mono h-[350px] overflow-y-auto text-slate-200 text-sm scrollbar-thin scrollbar-thumb-indigo-500/20 scrollbar-track-transparent">
                    {output.map((item, i) => (
                        <div key={i} className="mb-4">
                            <div className="flex items-center gap-2 text-cyan-400">
                                <span>aether@ai:~$</span>
                                <span className="text-white">{item.command}</span>
                            </div>
                            <div className="mt-1 text-slate-400 whitespace-pre-wrap pl-4 border-l-2 border-slate-700 ml-1">
                                {item.response}
                            </div>
                        </div>
                    ))}
                    <div className="flex items-center gap-2">
                        <span className="text-cyan-400 font-bold">aether@ai:~$</span>
                        <span>{text}</span>
                        <span className={`w-2 h-5 bg-cyan-400 ${showCursor ? 'opacity-100' : 'opacity-0'}`}></span>
                    </div>
                </div>
            </div>
        </div>
    );
}
