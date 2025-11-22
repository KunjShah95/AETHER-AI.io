import React from "react";
import { Laptop, Server, ShieldCheck, ArrowRight } from "lucide-react";

export function HowItWorks() {
    return (
        <section className="py-24 bg-black relative z-20">
            <div className="max-w-7xl mx-auto px-6">
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-5xl font-bold mb-4 text-white">
                        How AetherAI Works
                    </h2>
                    <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
                        A local-first architecture designed for privacy and speed.
                    </p>
                </div>

                <div className="flex flex-col md:flex-row items-center justify-center gap-8 relative">
                    {/* Step 1 */}
                    <div className="flex flex-col items-center text-center max-w-xs relative z-10">
                        <div className="w-20 h-20 rounded-2xl bg-neutral-900 border border-neutral-800 flex items-center justify-center mb-6 shadow-lg shadow-indigo-500/10">
                            <Laptop className="w-10 h-10 text-indigo-400" />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2">1. Install Locally</h3>
                        <p className="text-neutral-400 text-sm">
                            Download the CLI or desktop app. It runs as a background service on your machine.
                        </p>
                    </div>

                    {/* Arrow 1 */}
                    <div className="hidden md:block text-neutral-700">
                        <ArrowRight className="w-8 h-8" />
                    </div>

                    {/* Step 2 */}
                    <div className="flex flex-col items-center text-center max-w-xs relative z-10">
                        <div className="w-20 h-20 rounded-2xl bg-neutral-900 border border-neutral-800 flex items-center justify-center mb-6 shadow-lg shadow-purple-500/10">
                            <Server className="w-10 h-10 text-purple-400" />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2">2. Select Model</h3>
                        <p className="text-neutral-400 text-sm">
                            Choose from Llama 3, Mistral, or connect to OpenAI/Anthropic APIs if you prefer cloud.
                        </p>
                    </div>

                    {/* Arrow 2 */}
                    <div className="hidden md:block text-neutral-700">
                        <ArrowRight className="w-8 h-8" />
                    </div>

                    {/* Step 3 */}
                    <div className="flex flex-col items-center text-center max-w-xs relative z-10">
                        <div className="w-20 h-20 rounded-2xl bg-neutral-900 border border-neutral-800 flex items-center justify-center mb-6 shadow-lg shadow-emerald-500/10">
                            <ShieldCheck className="w-10 h-10 text-emerald-400" />
                        </div>
                        <h3 className="text-xl font-bold text-white mb-2">3. Secure Inference</h3>
                        <p className="text-neutral-400 text-sm">
                            Your code is analyzed locally. No data leaves your device without your explicit permission.
                        </p>
                    </div>

                    {/* Connecting Line (Background) */}
                    <div className="absolute top-10 left-1/4 right-1/4 h-0.5 bg-gradient-to-r from-indigo-500/20 via-purple-500/20 to-emerald-500/20 hidden md:block -z-10" />
                </div>
            </div>
        </section>
    );
}
