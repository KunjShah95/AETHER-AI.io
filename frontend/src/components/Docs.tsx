import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Link, useParams, Navigate } from 'react-router-dom';
import { cn } from '@/lib/utils';
// import { ScrollArea } from '@/components/ui/ScrollArea';
import { ArrowLeft, Menu } from 'lucide-react';

// Import markdown files
import indexMd from '../docs/index.md?raw';
import gettingStartedMd from '../docs/getting-started.md?raw';
import commandsMd from '../docs/commands.md?raw';
import advancedFeaturesMd from '../docs/advanced-features.md?raw';
import modelsMd from '../docs/models.md?raw';
import themesMd from '../docs/themes.md?raw';
import tasksMd from '../docs/tasks.md?raw';
import securityMd from '../docs/security.md?raw';
import developerGuideMd from '../docs/developer-guide.md?raw';
import referenceMd from '../docs/reference.md?raw';

const docsMap: Record<string, { title: string; content: string }> = {
    'introduction': { title: 'Introduction', content: indexMd },
    'getting-started': { title: 'Getting Started', content: gettingStartedMd },
    'commands': { title: 'Commands', content: commandsMd },
    'advanced-features': { title: 'Advanced Features', content: advancedFeaturesMd },
    'models': { title: 'Models', content: modelsMd },
    'themes': { title: 'Themes', content: themesMd },
    'tasks': { title: 'Tasks', content: tasksMd },
    'security': { title: 'Security', content: securityMd },
    'developer-guide': { title: 'Developer Guide', content: developerGuideMd },
    'reference': { title: 'API Reference', content: referenceMd },
};

export function Docs() {
    const { slug } = useParams();
    const [isMobileMenuOpen, setIsMobileMenuOpen] = React.useState(false);

    // Default to introduction if no slug
    const currentSlug = slug || 'introduction';
    const currentDoc = docsMap[currentSlug];

    if (!currentDoc) {
        return <Navigate to="/docs/introduction" replace />;
    }

    return (
        <div className="min-h-screen bg-black text-white flex flex-col md:flex-row font-sans">
            {/* Mobile Header */}
            <div className="md:hidden flex items-center justify-between p-4 border-b border-neutral-800 bg-black/50 backdrop-blur-md sticky top-0 z-50">
                <Link to="/" className="flex items-center gap-2 text-neutral-400 hover:text-white">
                    <ArrowLeft className="w-5 h-5" />
                    <span>Back</span>
                </Link>
                <button onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
                    <Menu className="w-6 h-6 text-white" />
                </button>
            </div>

            {/* Sidebar */}
            <aside className={cn(
                "fixed inset-y-0 left-0 z-40 w-64 bg-neutral-900/50 border-r border-neutral-800 transform transition-transform duration-300 md:translate-x-0 md:static md:h-screen overflow-y-auto",
                isMobileMenuOpen ? "translate-x-0" : "-translate-x-full"
            )}>
                <div className="p-6">
                    <Link to="/" className="flex items-center gap-2 text-neutral-400 hover:text-white mb-8 transition-colors">
                        <ArrowLeft className="w-4 h-4" />
                        <span>Back to Home</span>
                    </Link>
                    <h2 className="text-xl font-bold text-white mb-6 px-2">Documentation</h2>
                    <nav className="space-y-1">
                        {Object.entries(docsMap).map(([key, doc]) => (
                            <Link
                                key={key}
                                to={`/docs/${key}`}
                                onClick={() => setIsMobileMenuOpen(false)}
                                className={cn(
                                    "block px-3 py-2 rounded-md text-sm font-medium transition-colors",
                                    currentSlug === key
                                        ? "bg-terminal-cyan/10 text-terminal-cyan"
                                        : "text-neutral-400 hover:text-white hover:bg-neutral-800"
                                )}
                            >
                                {doc.title}
                            </Link>
                        ))}
                    </nav>
                </div>
            </aside>

            {/* Main Content */}
            <main className="flex-1 min-w-0 overflow-y-auto h-screen">
                <div className="max-w-4xl mx-auto px-6 py-12 md:py-16">
                    <article className="prose prose-invert prose-lg max-w-none prose-headings:font-bold prose-a:text-terminal-cyan prose-code:text-terminal-cyan prose-pre:bg-neutral-900 prose-pre:border prose-pre:border-neutral-800">
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                            {currentDoc.content}
                        </ReactMarkdown>
                    </article>
                </div>
            </main>

            {/* Overlay for mobile sidebar */}
            {isMobileMenuOpen && (
                <div
                    className="fixed inset-0 bg-black/50 z-30 md:hidden"
                    onClick={() => setIsMobileMenuOpen(false)}
                />
            )}
        </div>
    );
}
