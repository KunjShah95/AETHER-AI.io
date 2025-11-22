import React from "react";
import { Spotlight } from "@/components/ui/Spotlight";
import { Button } from "@/components/ui/MovingBorder";
import { TextGenerateEffect } from "@/components/ui/TextGenerateEffect";
import { Terminal } from "./Terminal";
import { Download, Play } from "lucide-react";

export function Hero() {
    return (
        <div className="h-[40rem] md:h-[50rem] w-full rounded-md flex md:items-center md:justify-center bg-black/[0.96] antialiased bg-grid-white/[0.02] relative overflow-hidden">
            <Spotlight
                className="-top-40 left-0 md:left-60 md:-top-20"
                fill="white"
            />

            <div className="p-4 max-w-7xl mx-auto relative z-10 w-full pt-20 md:pt-0 flex flex-col md:flex-row items-center justify-between gap-12">

                {/* Text Content */}
                <div className="flex-1 text-center md:text-left">
                    <h1 className="text-4xl md:text-7xl font-bold text-white leading-tight pb-4">
                        AI in Your Terminal.<br />
                        <span className="text-terminal-cyan">Not in the Cloud.</span>
                    </h1>

                    <TextGenerateEffect
                        words="Local-first AI assistant. Multi-model support. Zero telemetry."
                        className="mt-4 font-normal text-base text-neutral-400 max-w-lg mx-auto md:mx-0"
                    />

                    <div className="mt-10 flex flex-col md:flex-row gap-4 justify-center md:justify-start items-center">
                        <Button
                            borderRadius="1.75rem"
                            className="bg-slate-900 text-white border-slate-800 font-bold"
                            onClick={() => document.getElementById('download')?.scrollIntoView({ behavior: 'smooth' })}
                        >
                            <div className="flex items-center gap-2">
                                <Download className="w-4 h-4" />
                                <span>Get Started</span>
                            </div>
                        </Button>

                        <button
                            onClick={() => window.open('https://www.youtube.com/watch?v=DLyrTzcYgbI', '_blank')}
                            className="px-8 py-3 rounded-full bg-transparent border border-neutral-700 text-neutral-300 hover:bg-neutral-800 transition-colors flex items-center gap-2 font-medium"
                        >
                            <Play className="w-4 h-4" />
                            <span>Watch Demo</span>
                        </button>
                    </div>
                </div>

                {/* Terminal Mockup */}
                <div className="flex-1 w-full max-w-xl relative">
                    <div className="absolute -inset-0.5 bg-terminal-cyan/20 rounded-2xl blur-sm"></div>
                    <Terminal />
                </div>

            </div>
        </div>
    );
}
