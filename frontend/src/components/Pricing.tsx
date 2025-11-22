import React from "react";
import { Check } from "lucide-react";

export function Pricing() {
    return (
        <section className="py-24 bg-black relative z-20">
            <div className="max-w-7xl mx-auto px-6">
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-5xl font-bold mb-4 text-white">
                        Pricing
                    </h2>
                    <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
                        Free for personal use. Enterprise plans available for teams.
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
                    {/* Free Plan */}
                    <div className="rounded-2xl border border-neutral-800 bg-neutral-900/50 p-8 flex flex-col relative overflow-hidden group hover:border-terminal-cyan/50 transition-colors">
                        <div className="mb-4">
                            <h3 className="text-xl font-bold text-white">Community</h3>
                            <p className="text-neutral-400 text-sm mt-1">For individual developers</p>
                        </div>
                        <div className="mb-6">
                            <span className="text-4xl font-bold text-white">$0</span>
                            <span className="text-neutral-500">/forever</span>
                        </div>
                        <ul className="space-y-4 mb-8 flex-1">
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-green-500" /> Local LLM Support
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-green-500" /> Basic Code Analysis
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-green-500" /> Unlimited Chat
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-green-500" /> Community Support
                            </li>
                        </ul>
                        <button className="w-full py-3 rounded-lg bg-red-600 text-white font-bold hover:bg-red-700 transition-colors">
                            Download Now
                        </button>
                    </div>

                    {/* Pro Plan (Highlighted) */}
                    <div className="rounded-2xl border border-terminal-cyan/50 bg-neutral-900/80 p-8 flex flex-col relative overflow-hidden shadow-2xl shadow-terminal-cyan/10 transform md:-translate-y-4">
                        <div className="absolute top-0 right-0 bg-terminal-cyan text-black text-xs font-bold px-3 py-1 rounded-bl-lg">
                            POPULAR
                        </div>
                        <div className="mb-4">
                            <h3 className="text-xl font-bold text-white">Pro</h3>
                            <p className="text-neutral-400 text-sm mt-1">For power users</p>
                        </div>
                        <div className="mb-6">
                            <span className="text-4xl font-bold text-white">$19</span>
                            <span className="text-neutral-500">/month</span>
                        </div>
                        <ul className="space-y-4 mb-8 flex-1">
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-terminal-cyan" /> Everything in Community
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-terminal-cyan" /> GPT-4 & Claude 3 Access
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-terminal-cyan" /> Cloud Sync
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-terminal-cyan" /> Priority Support
                            </li>
                        </ul>
                        <button className="w-full py-3 rounded-lg bg-red-600 text-white font-bold hover:bg-red-700 transition-colors">
                            Get Pro
                        </button>
                    </div>

                    {/* Enterprise Plan */}
                    <div className="rounded-2xl border border-neutral-800 bg-neutral-900/50 p-8 flex flex-col relative overflow-hidden group hover:border-terminal-cyan/50 transition-colors">
                        <div className="mb-4">
                            <h3 className="text-xl font-bold text-white">Enterprise</h3>
                            <p className="text-neutral-400 text-sm mt-1">For large teams</p>
                        </div>
                        <div className="mb-6">
                            <span className="text-4xl font-bold text-white">Custom</span>
                        </div>
                        <ul className="space-y-4 mb-8 flex-1">
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-green-500" /> SSO & Audit Logs
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-green-500" /> Custom Model Fine-tuning
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-green-500" /> On-premise Deployment
                            </li>
                            <li className="flex items-center gap-2 text-neutral-300 text-sm">
                                <Check className="w-4 h-4 text-green-500" /> Dedicated Account Manager
                            </li>
                        </ul>
                        <button className="w-full py-3 rounded-lg bg-red-600 text-white font-bold hover:bg-red-700 transition-colors">
                            Contact Sales
                        </button>
                    </div>

                </div>
            </div>
        </section>
    );
}
