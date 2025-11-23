import React from "react";
import { Check, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/MovingBorder";

export function Pricing() {
    return (
        <section className="py-24 bg-black relative z-20" id="pricing">
            <div className="max-w-7xl mx-auto px-6">
                <div className="text-center mb-16">
                    <h2 className="text-3xl md:text-5xl font-bold mb-4 text-white">
                        Pricing
                    </h2>
                    <p className="text-lg text-neutral-400 max-w-2xl mx-auto">
                        Open source and free forever. No hidden fees.
                    </p>
                </div>

                <div className="flex justify-center">
                    {/* Free Plan */}
                    <div className="w-full max-w-lg rounded-2xl border border-terminal-cyan/50 bg-neutral-900/50 p-8 flex flex-col relative overflow-hidden shadow-2xl shadow-terminal-cyan/10">
                        <div className="absolute top-0 right-0 bg-terminal-cyan text-black text-xs font-bold px-3 py-1 rounded-bl-lg">
                            OPEN SOURCE
                        </div>
                        <div className="mb-4">
                            <h3 className="text-2xl font-bold text-white">Community Edition</h3>
                            <p className="text-neutral-400 text-sm mt-1">Everything you need to run local AI</p>
                        </div>
                        <div className="mb-6">
                            <span className="text-5xl font-bold text-white">$0</span>
                            <span className="text-neutral-500 text-xl">/forever</span>
                        </div>
                        <ul className="space-y-4 mb-8 flex-1">
                            <li className="flex items-center gap-3 text-neutral-300">
                                <Check className="w-5 h-5 text-terminal-cyan" />
                                <span>Full Local LLM Support (Llama 3, Mistral, etc.)</span>
                            </li>
                            <li className="flex items-center gap-3 text-neutral-300">
                                <Check className="w-5 h-5 text-terminal-cyan" />
                                <span>Advanced Code Analysis & Refactoring</span>
                            </li>
                            <li className="flex items-center gap-3 text-neutral-300">
                                <Check className="w-5 h-5 text-terminal-cyan" />
                                <span>Unlimited Chat History</span>
                            </li>
                            <li className="flex items-center gap-3 text-neutral-300">
                                <Check className="w-5 h-5 text-terminal-cyan" />
                                <span>Zero Telemetry / 100% Privacy</span>
                            </li>
                            <li className="flex items-center gap-3 text-neutral-300">
                                <Check className="w-5 h-5 text-terminal-cyan" />
                                <span>Community Plugins & Themes</span>
                            </li>
                        </ul>

                        <Button
                            borderRadius="1.75rem"
                            className="bg-slate-900 text-white border-slate-800 font-bold w-full"
                            onClick={() => document.getElementById('download')?.scrollIntoView({ behavior: 'smooth' })}
                        >
                            <div className="flex items-center justify-center gap-2">
                                <span>Download Now</span>
                                <ArrowRight className="w-4 h-4" />
                            </div>
                        </Button>
                    </div>
                </div>
            </div>
        </section>
    );
}
