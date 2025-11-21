import React from 'react';
import { Brain, Terminal as TerminalIcon, ListTodo, Palette, Code2, Plug, Zap, Shield, Settings } from 'lucide-react';

const features = [
    {
        icon: <Brain className="w-8 h-8" />,
        title: "Multi-Model Support",
        description: "Seamlessly switch between 8+ AI models: Gemini, Groq, HuggingFace, DeepSeek, Ollama, Claude, GPT, and Mistral AI"
    },
    {
        icon: <TerminalIcon className="w-8 h-8" />,
        title: "Terminal Interface",
        description: "Powerful command-line interface with syntax highlighting and auto-completion"
    },
    {
        icon: <ListTodo className="w-8 h-8" />,
        title: "Task Management",
        description: "Complete task management system with categories, priorities, due dates, and progress tracking"
    },
    {
        icon: <Palette className="w-8 h-8" />,
        title: "Customizable Themes",
        description: "6 built-in themes plus custom theme creation with full color customization"
    },
    {
        icon: <Code2 className="w-8 h-8" />,
        title: "Code Review Assistant",
        description: "AI-powered code analysis supporting 15+ languages with security, performance, and quality assessments"
    },
    {
        icon: <Plug className="w-8 h-8" />,
        title: "Integration Hub",
        description: "Connect with 10+ services including GitHub, Slack, Discord, Trello, Jira, and more"
    },
    {
        icon: <Zap className="w-8 h-8" />,
        title: "Lightning Fast",
        description: "Optimized performance with instant responses and minimal resource usage"
    },
    {
        icon: <Shield className="w-8 h-8" />,
        title: "Secure & Private",
        description: "Your data stays local with enterprise-grade security and privacy protection"
    },
    {
        icon: <Settings className="w-8 h-8" />,
        title: "Highly Customizable",
        description: "Extensive configuration options to tailor the experience to your needs"
    }
];

export function Features() {
    return (
        <section id="features" className="py-24 bg-[#1e293b] relative">
            <div className="max-w-7xl mx-auto px-6">
                <div className="text-center mb-16">
                    <h2 className="text-4xl font-bold mb-4 text-white">Powerful Features</h2>
                    <p className="text-lg text-slate-300 max-w-2xl mx-auto">
                        Discover what makes AetherAI the ultimate terminal assistant
                    </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                    {features.map((feature, index) => (
                        <div key={index} className="bg-gradient-to-br from-[#6366f1]/10 to-[#1e293b] border border-indigo-400/20 rounded-2xl p-8 text-center shadow-xl hover:scale-105 transition-transform duration-300 group">
                            <div className="w-16 h-16 mx-auto mb-6 flex items-center justify-center bg-gradient-to-br from-indigo-400 to-fuchsia-400 rounded-2xl text-white shadow-lg group-hover:shadow-indigo-500/50 transition-all">
                                {feature.icon}
                            </div>
                            <h3 className="text-xl font-semibold mb-3 text-white">{feature.title}</h3>
                            <p className="text-slate-400 leading-relaxed">{feature.description}</p>
                        </div>
                    ))}
                </div>
            </div>
        </section>
    );
}
