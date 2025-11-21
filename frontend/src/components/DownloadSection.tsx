import React, { useState, useEffect } from 'react';
import { Download } from 'lucide-react';

export function DownloadSection() {
    const [downloadCount, setDownloadCount] = useState(0);

    useEffect(() => {
        const stored = localStorage.getItem('nexusDownloadCount');
        if (stored) setDownloadCount(parseInt(stored));
    }, []);

    const handleDownload = (os: string) => {
        const newCount = downloadCount + 1;
        setDownloadCount(newCount);
        localStorage.setItem('nexusDownloadCount', newCount.toString());
        // We could add a toast notification here if we implemented a toast system
    };

    return (
        <section id="download" className="py-24 bg-gradient-to-br from-[#0f172a] via-[#1e293b] to-[#6366f1]/10">
            <div className="max-w-4xl mx-auto px-6">
                <div className="text-center mb-12">
                    <h2 className="text-4xl font-bold mb-4 text-white">Download AetherAI</h2>
                    <p className="text-lg text-slate-300 max-w-2xl mx-auto">Get started with AetherAI on your platform</p>
                    <p className="text-sm text-indigo-400 mt-2 font-mono">Total Downloads: {downloadCount.toLocaleString()}</p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                    {['Windows', 'Linux', 'macOS'].map((os) => (
                        <div key={os} className="bg-[#1e293b]/50 backdrop-blur border border-white/10 rounded-2xl p-8 text-center hover:border-indigo-400/50 transition-all group">
                            <div className="text-4xl mb-4 font-bold text-white">
                                {os === 'Windows' && '🪟'}
                                {os === 'Linux' && '🐧'}
                                {os === 'macOS' && '🍎'}
                            </div>
                            <h3 className="text-xl font-semibold mb-2 text-white">{os} Installer</h3>
                            <p className="text-slate-400 mb-6 text-sm">Automated setup script for {os}</p>
                            <a
                                href={`/dist/install_${os.toLowerCase()}.zip`}
                                download
                                onClick={() => handleDownload(os)}
                                className="inline-flex items-center gap-2 bg-white/10 hover:bg-indigo-500 text-white px-6 py-3 rounded-xl font-bold transition-all w-full justify-center group-hover:shadow-lg group-hover:shadow-indigo-500/25 cursor-pointer"
                            >
                                <Download className="w-4 h-4" /> Download
                            </a>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
