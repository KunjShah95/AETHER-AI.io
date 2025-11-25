import { useState } from 'react';
import { Copy, Check } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

interface CodeBlockProps {
    code: string;
    language: string;
}

const CodeBlock = ({ code, language }: CodeBlockProps) => {
    const [copied, setCopied] = useState(false);

    const handleCopy = () => {
        navigator.clipboard.writeText(code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
    };

    return (
        <div className="relative group">
            <div className="absolute top-3 right-3 z-10">
                <button
                    onClick={handleCopy}
                    className="p-2 bg-slate-700/50 hover:bg-slate-700 rounded-lg border border-slate-600/50 transition-all duration-200"
                >
                    <AnimatePresence mode="wait">
                        {copied ? (
                            <motion.div
                                key="check"
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                exit={{ scale: 0 }}
                            >
                                <Check className="w-4 h-4 text-green-400" />
                            </motion.div>
                        ) : (
                            <motion.div
                                key="copy"
                                initial={{ scale: 0 }}
                                animate={{ scale: 1 }}
                                exit={{ scale: 0 }}
                            >
                                <Copy className="w-4 h-4 text-slate-400" />
                            </motion.div>
                        )}
                    </AnimatePresence>
                </button>
            </div>

            <div className="bg-slate-900/50 border border-slate-700/50 rounded-lg overflow-hidden">
                <div className="px-4 py-2 bg-slate-800/50 border-b border-slate-700/50 flex items-center gap-2">
                    <div className="flex gap-1.5">
                        <div className="w-3 h-3 rounded-full bg-red-500/80" />
                        <div className="w-3 h-3 rounded-full bg-yellow-500/80" />
                        <div className="w-3 h-3 rounded-full bg-green-500/80" />
                    </div>
                    <span className="text-xs text-slate-400 ml-2">{language}</span>
                </div>
                <pre className="p-4 overflow-x-auto text-sm">
                    <code className="text-slate-300 font-mono">{code}</code>
                </pre>
            </div>
        </div>
    );
};

export default CodeBlock;
