import { motion } from 'framer-motion';
import { Palette, Sparkles, Droplet, Trees, Sunset, Minimize } from 'lucide-react';
import CodeBlock from '../CodeBlock';

const ThemesDoc = () => {
    const builtInThemes = [
        {
            name: 'Default',
            icon: Palette,
            color: 'from-slate-600 to-slate-800',
            description: 'Classic dark theme with purple accents',
            command: '/theme default'
        },
        {
            name: 'Neon',
            icon: Sparkles,
            color: 'from-purple-600 via-pink-600 to-blue-600',
            description: 'Bright neon colors for a vibrant experience',
            command: '/theme neon'
        },
        {
            name: 'Ocean',
            icon: Droplet,
            color: 'from-blue-600 to-cyan-600',
            description: 'Cool ocean blue theme',
            command: '/theme ocean'
        },
        {
            name: 'Forest',
            icon: Trees,
            color: 'from-green-700 to-emerald-700',
            description: 'Calm forest green theme',
            command: '/theme forest'
        },
        {
            name: 'Sunset',
            icon: Sunset,
            color: 'from-orange-600 to-red-600',
            description: 'Warm sunset colors',
            command: '/theme sunset'
        },
        {
            name: 'Minimal',
            icon: Minimize,
            color: 'from-gray-700 to-gray-900',
            description: 'Clean minimal design',
            command: '/theme minimal'
        },
    ];

    const themeProperties = [
        'primary_color',
        'secondary_color',
        'background_color',
        'text_color',
        'border_color',
        'success_color',
        'error_color',
        'warning_color',
    ];

    return (
        <div className="space-y-10">
            <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
            >
                <h1 className="text-4xl lg:text-5xl font-bold mb-4 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
                    UI Themes
                </h1>
                <p className="text-lg text-slate-300">
                    Customize the look and feel of your terminal with built-in themes or create your own.
                </p>
            </motion.div>

            {/* Built-in Themes */}
            <div className="space-y-4">
                <h2 className="text-2xl font-bold text-white">Built-in Themes</h2>

                <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                    {builtInThemes.map((theme, index) => {
                        const Icon = theme.icon;
                        return (
                            <motion.div
                                key={theme.name}
                                initial={{ y: 20, opacity: 0 }}
                                animate={{ y: 0, opacity: 1 }}
                                transition={{ delay: index * 0.1 }}
                                className="group relative overflow-hidden bg-slate-800/30 border border-purple-500/20 rounded-xl p-6 hover:border-purple-500/40 transition-all duration-300"
                            >
                                {/* Theme preview bar */}
                                <div className={`absolute top-0 left-0 right-0 h-1 bg-gradient-to-r ${theme.color}`} />

                                <div className="mt-2 space-y-4">
                                    <div className="flex items-center gap-3">
                                        <div className={`w-12 h-12 rounded-lg bg-gradient-to-br ${theme.color} flex items-center justify-center`}>
                                            <Icon className="w-6 h-6 text-white" />
                                        </div>
                                        <div>
                                            <h3 className="text-lg font-semibold text-white">{theme.name}</h3>
                                            <p className="text-xs text-slate-400">Built-in</p>
                                        </div>
                                    </div>

                                    <p className="text-slate-300 text-sm">{theme.description}</p>

                                    <code className="block px-3 py-1.5 bg-slate-900/50 border border-purple-500/30 rounded-lg text-purple-400 font-mono text-xs">
                                        {theme.command}
                                    </code>
                                </div>
                            </motion.div>
                        );
                    })}
                </div>
            </div>

            {/* Custom Themes */}
            <div className="space-y-6">
                <h2 className="text-2xl font-bold text-white">Custom Themes</h2>

                <p className="text-slate-300">
                    Create your own themes to match your personal style or workspace.
                </p>

                <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.6 }}
                    className="bg-gradient-to-br from-purple-500/10 to-blue-500/10 border border-purple-500/30 rounded-xl p-6 space-y-4"
                >
                    <h3 className="text-lg font-semibold text-white">Creating a Custom Theme</h3>

                    <div className="grid md:grid-cols-2 gap-4">
                        <div>
                            <h4 className="text-sm font-semibold text-purple-400 mb-2">Management Commands</h4>
                            <div className="space-y-2 text-sm">
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme create [name]</code>
                                    <span className="text-slate-400 text-xs">Create new theme</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme save [name]</code>
                                    <span className="text-slate-400 text-xs">Save current theme</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme load [name]</code>
                                    <span className="text-slate-400 text-xs">Load saved theme</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme delete [name]</code>
                                    <span className="text-slate-400 text-xs">Delete theme</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme list</code>
                                    <span className="text-slate-400 text-xs">List all themes</span>
                                </div>
                            </div>
                        </div>

                        <div>
                            <h4 className="text-sm font-semibold text-blue-400 mb-2">Customization Commands</h4>
                            <div className="space-y-2 text-sm">
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme set [property] [value]</code>
                                    <span className="text-slate-400 text-xs">Set property</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme preview [name]</code>
                                    <span className="text-slate-400 text-xs">Preview theme</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme info [name]</code>
                                    <span className="text-slate-400 text-xs">View theme info</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme export [name]</code>
                                    <span className="text-slate-400 text-xs">Export theme</span>
                                </div>
                                <div className="flex items-start gap-2">
                                    <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-xs shrink-0">/theme import [file]</code>
                                    <span className="text-slate-400 text-xs">Import theme</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </motion.div>

                {/* Theme Properties */}
                <motion.div
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.7 }}
                    className="space-y-4"
                >
                    <h3 className="text-xl font-semibold text-white">Theme Properties</h3>

                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-3">
                        {themeProperties.map((property, index) => (
                            <motion.div
                                key={property}
                                initial={{ scale: 0.9, opacity: 0 }}
                                animate={{ scale: 1, opacity: 1 }}
                                transition={{ delay: index * 0.05 + 0.8 }}
                                className="bg-slate-800/30 border border-purple-500/20 rounded-lg p-3"
                            >
                                <code className="text-sm text-purple-400 font-mono">{property}</code>
                            </motion.div>
                        ))}
                    </div>
                </motion.div>
            </div>

            {/* Example Workflow */}
            <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 1.0 }}
                className="space-y-4"
            >
                <h2 className="text-2xl font-bold text-white">Example: Creating a Custom Theme</h2>

                <CodeBlock language="bash" code={`# Create a new theme
/theme create myawesometheme

# Set colors
/theme set primary_color #a855f7
/theme set secondary_color #3b82f6
/theme set background_color #0f172a
/theme set text_color #e2e8f0
/theme set border_color #6366f1
/theme set success_color #10b981
/theme set error_color #ef4444
/theme set warning_color #f59e0b

# Preview the theme
/theme preview myawesometheme

# Save it
/theme save myawesometheme

# Export to share with others
/theme export myawesometheme`} />
            </motion.div>

            {/* Tips */}
            <motion.div
                initial={{ y: 20, opacity: 0 }}
                animate={{ y: 0, opacity: 1 }}
                transition={{ delay: 1.1 }}
                className="bg-gradient-to-r from-purple-500/10 to-blue-500/10 border border-purple-500/30 rounded-xl p-6"
            >
                <h3 className="text-lg font-semibold text-white mb-3 flex items-center gap-2">
                    💡 Tips for Great Themes
                </h3>
                <ul className="space-y-2 text-slate-300">
                    <li className="flex items-start gap-2">
                        <span className="text-purple-400 shrink-0">•</span>
                        <span>Use hex color codes (#RRGGBB) for precise color control</span>
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="text-purple-400 shrink-0">•</span>
                        <span>Ensure sufficient contrast between background and text colors</span>
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="text-purple-400 shrink-0">•</span>
                        <span>Test your theme with different commands to see how it looks</span>
                    </li>
                    <li className="flex items-start gap-2">
                        <span className="text-purple-400 shrink-0">•</span>
                        <span>Use <code className="px-2 py-1 bg-slate-800 rounded text-purple-400 text-sm">/theme reset</code> to return to default if needed</span>
                    </li>
                </ul>
            </motion.div>
        </div>
    );
};

export default ThemesDoc;
