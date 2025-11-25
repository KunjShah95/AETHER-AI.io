import type { SearchableItem } from '@/utils/searchUtils';

/**
 * Complete searchable index for documentation
 */
export const documentationIndex: SearchableItem[] = [
    // Home Section
    {
        id: 'home-intro',
        section: 'home',
        sectionTitle: 'Home',
        title: 'NEXUS AI Terminal Assistant',
        description: 'Production‑ready, secure, multi‑model AI for your terminal. Switch between multiple AI providers with one CLI.',
        content: 'NEXUS AI is a production-ready, secure, multi-model AI terminal assistant. Version 3.0.1. Features multi-model switching, local AI, security, utilities, developer tools, and productivity suite.',
        keywords: ['nexus', 'ai', 'terminal', 'assistant', 'multi-model', 'production', 'secure']
    },
    {
        id: 'home-multi-model',
        section: 'home',
        sectionTitle: 'Home',
        category: 'Key Features',
        title: 'Multi-Model Switching',
        description: 'Switch between Gemini, Groq, Ollama, HuggingFace, ChatGPT, and MCP',
        content: 'Support for multiple AI models including Gemini, Groq, Ollama, HuggingFace, ChatGPT, and MCP',
        keywords: ['multi-model', 'gemini', 'groq', 'ollama', 'huggingface', 'chatgpt', 'mcp', 'switching']
    },
    {
        id: 'home-local-ai',
        section: 'home',
        sectionTitle: 'Home',
        category: 'Key Features',
        title: 'Local AI via Ollama',
        description: 'Run models locally with complete privacy and offline access',
        content: 'Run AI models locally using Ollama for complete privacy and offline access',
        keywords: ['local', 'ollama', 'privacy', 'offline', 'ai']
    },
    {
        id: 'home-security',
        section: 'home',
        sectionTitle: 'Home',
        category: 'Key Features',
        title: 'Secure by Default',
        description: 'Input sanitization, safe command allowlist, and boundary checks',
        content: 'Security features including input sanitization, safe command allowlist, and boundary checks',
        keywords: ['security', 'secure', 'safe', 'sanitization', 'allowlist']
    },
    {
        id: 'home-utilities',
        section: 'home',
        sectionTitle: 'Home',
        category: 'Key Features',
        title: 'Powerful Utilities',
        description: 'Web search, system info, notes, timers, and conversions',
        content: 'Utility features including web search, system information, notes, timers, and unit conversions',
        keywords: ['utilities', 'web search', 'system info', 'notes', 'timers', 'conversion']
    },
    {
        id: 'home-developer-tools',
        section: 'home',
        sectionTitle: 'Home',
        category: 'Key Features',
        title: 'Developer Tools',
        description: 'Code review, refactoring, TODO extraction, and Git helpers',
        content: 'Developer tools for code review, refactoring, TODO extraction, and Git integration',
        keywords: ['developer', 'code review', 'refactoring', 'todo', 'git']
    },
    {
        id: 'home-productivity',
        section: 'home',
        sectionTitle: 'Home',
        category: 'Key Features',
        title: 'Productivity Suite',
        description: 'Task manager, themes, reminders, analytics, and learning tools',
        content: 'Productivity features including task manager, themes, reminders, analytics, and learning tools',
        keywords: ['productivity', 'tasks', 'themes', 'reminders', 'analytics', 'learning']
    },

    // Commands Section
    {
        id: 'cmd-help',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'System Commands',
        title: '/help',
        description: 'Show comprehensive help menu',
        content: 'Display the comprehensive help menu with all available commands',
        keywords: ['help', 'menu', 'commands', 'system']
    },
    {
        id: 'cmd-status',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'System Commands',
        title: '/status',
        description: 'Display current model and system status',
        content: 'Show current AI model and system status information',
        keywords: ['status', 'model', 'system', 'current']
    },
    {
        id: 'cmd-clear',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'System Commands',
        title: '/clear',
        description: 'Clear the terminal screen',
        content: 'Clear the terminal screen',
        keywords: ['clear', 'screen', 'terminal']
    },
    {
        id: 'cmd-exit',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'System Commands',
        title: '/exit',
        description: 'Exit the NEXUS AI terminal',
        content: 'Exit and close the NEXUS AI terminal',
        keywords: ['exit', 'quit', 'close', 'terminal']
    },
    {
        id: 'cmd-sysinfo',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'System Commands',
        title: '/sysinfo',
        description: 'Show detailed system information',
        content: 'Display detailed system information including OS, CPU, memory',
        keywords: ['sysinfo', 'system', 'info', 'os', 'cpu', 'memory']
    },
    {
        id: 'cmd-config',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'System Commands',
        title: '/config',
        description: 'Display current configuration',
        content: 'Show current NEXUS AI configuration settings',
        keywords: ['config', 'configuration', 'settings']
    },
    {
        id: 'cmd-run',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/run',
        description: 'Execute safe system commands',
        content: 'Execute safe system commands. Example: /run ls -la',
        keywords: ['run', 'execute', 'command', 'system', 'shell']
    },
    {
        id: 'cmd-calc',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/calc',
        description: 'Calculate mathematical expressions',
        content: 'Calculate mathematical expressions. Example: /calc 2 + 2 * 3',
        keywords: ['calc', 'calculate', 'math', 'expression', 'calculator']
    },
    {
        id: 'cmd-websearch',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/websearch',
        description: 'Search the web using DuckDuckGo',
        content: 'Search the web using DuckDuckGo. Example: /websearch python tutorials',
        keywords: ['websearch', 'search', 'web', 'duckduckgo', 'internet']
    },
    {
        id: 'cmd-weather',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/weather',
        description: 'Get current weather information',
        content: 'Get current weather information for a city. Example: /weather New York',
        keywords: ['weather', 'forecast', 'temperature', 'city']
    },
    {
        id: 'cmd-note',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/note',
        description: 'Save a quick note',
        content: 'Save a quick note. Example: /note Buy milk',
        keywords: ['note', 'save', 'memo', 'reminder']
    },
    {
        id: 'cmd-notes',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/notes',
        description: 'View all saved notes',
        content: 'View all saved notes',
        keywords: ['notes', 'view', 'list', 'saved']
    },
    {
        id: 'cmd-timer',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/timer',
        description: 'Start a countdown timer',
        content: 'Start a countdown timer in seconds. Example: /timer 300',
        keywords: ['timer', 'countdown', 'alarm', 'time']
    },
    {
        id: 'cmd-convert',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/convert',
        description: 'Unit converter',
        content: 'Convert between units. Example: /convert 100 celsius fahrenheit',
        keywords: ['convert', 'converter', 'units', 'temperature', 'measurement']
    },
    {
        id: 'cmd-password',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Utility Commands',
        title: '/password',
        description: 'Generate secure password',
        content: 'Generate a secure password. Example: /password 16',
        keywords: ['password', 'generate', 'secure', 'random']
    },
    {
        id: 'cmd-codereview',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Developer Commands',
        title: '/codereview',
        description: 'AI code review for bugs and improvements',
        content: 'Get AI-powered code review for bugs and improvements',
        keywords: ['code review', 'review', 'bugs', 'improvements', 'ai']
    },
    {
        id: 'cmd-summarizefile',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Developer Commands',
        title: '/summarizefile',
        description: 'AI file summarization',
        content: 'Get AI-powered file summary',
        keywords: ['summarize', 'summary', 'file', 'ai']
    },
    {
        id: 'cmd-findbugs',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Developer Commands',
        title: '/findbugs',
        description: 'Find bugs in code using AI',
        content: 'Find bugs in code using AI analysis',
        keywords: ['find bugs', 'bugs', 'errors', 'ai', 'debug']
    },
    {
        id: 'cmd-refactor',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Developer Commands',
        title: '/refactor',
        description: 'AI code refactoring',
        content: 'AI-powered code refactoring with instructions',
        keywords: ['refactor', 'refactoring', 'code', 'ai', 'improve']
    },
    {
        id: 'cmd-gendoc',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Developer Commands',
        title: '/gendoc',
        description: 'Generate documentation for code',
        content: 'Generate documentation for code files',
        keywords: ['generate', 'documentation', 'docs', 'code']
    },
    {
        id: 'cmd-gentest',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Developer Commands',
        title: '/gentest',
        description: 'Generate unit tests for code',
        content: 'Generate unit tests for code files',
        keywords: ['generate', 'test', 'unit test', 'testing', 'code']
    },
    {
        id: 'cmd-git-commitmsg',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Developer Commands',
        title: '/git commitmsg',
        description: 'Generate git commit messages',
        content: 'Generate git commit messages from diff',
        keywords: ['git', 'commit', 'message', 'generate']
    },
    {
        id: 'cmd-todos',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Developer Commands',
        title: '/todos',
        description: 'Extract TODOs and FIXMEs from codebase',
        content: 'Extract all TODO and FIXME comments from codebase',
        keywords: ['todos', 'fixme', 'extract', 'codebase', 'comments']
    },
    {
        id: 'cmd-git-create-branch',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Git Advanced Commands',
        title: '/git create-branch',
        description: 'Create a new branch',
        content: 'Create a new git branch',
        keywords: ['git', 'branch', 'create', 'new']
    },
    {
        id: 'cmd-git-delete-branch',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Git Advanced Commands',
        title: '/git delete-branch',
        description: 'Delete a branch',
        content: 'Delete a git branch',
        keywords: ['git', 'branch', 'delete', 'remove']
    },
    {
        id: 'cmd-aifind',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Git Advanced Commands',
        title: '/aifind',
        description: 'AI-powered file search',
        content: 'AI-powered file search by keyword',
        keywords: ['aifind', 'search', 'file', 'ai', 'find']
    },
    {
        id: 'cmd-explore',
        section: 'commands',
        sectionTitle: 'Commands',
        category: 'Git Advanced Commands',
        title: '/explore',
        description: 'Explore codebase',
        content: 'Explore and navigate codebase',
        keywords: ['explore', 'codebase', 'navigate', 'browse']
    },

    // Advanced Features
    {
        id: 'adv-learn',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Context-Aware AI',
        title: '/learn',
        description: 'Teach AI about specific technologies or topics',
        content: 'Teach the AI about specific technologies or topics for more relevant responses',
        keywords: ['learn', 'teach', 'ai', 'context', 'technology']
    },
    {
        id: 'adv-remind',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Context-Aware AI',
        title: '/remind',
        description: 'Set a new reminder',
        content: 'Set a new reminder for tasks',
        keywords: ['remind', 'reminder', 'task', 'set']
    },
    {
        id: 'adv-reminders',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Context-Aware AI',
        title: '/reminders',
        description: 'View all reminders',
        content: 'View all active reminders',
        keywords: ['reminders', 'view', 'list', 'all']
    },
    {
        id: 'adv-complete-reminder',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Context-Aware AI',
        title: '/complete-reminder',
        description: 'Mark reminder as complete',
        content: 'Mark a reminder as complete',
        keywords: ['complete', 'reminder', 'done', 'finish']
    },
    {
        id: 'adv-analytics',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Analytics & Monitoring',
        title: '/analytics',
        description: 'View usage statistics',
        content: 'View usage statistics and analytics',
        keywords: ['analytics', 'statistics', 'usage', 'stats']
    },
    {
        id: 'adv-error-analytics',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Analytics & Monitoring',
        title: '/error-analytics',
        description: 'View error analytics',
        content: 'View error analytics and statistics',
        keywords: ['error', 'analytics', 'statistics', 'debugging']
    },
    {
        id: 'adv-start-monitoring',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Analytics & Monitoring',
        title: '/start-monitoring',
        description: 'Start system monitoring',
        content: 'Start system performance monitoring',
        keywords: ['monitoring', 'start', 'system', 'performance']
    },
    {
        id: 'adv-stop-monitoring',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Analytics & Monitoring',
        title: '/stop-monitoring',
        description: 'Stop system monitoring',
        content: 'Stop system performance monitoring',
        keywords: ['monitoring', 'stop', 'system', 'performance']
    },
    {
        id: 'adv-net-diag',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Analytics & Monitoring',
        title: '/net-diag',
        description: 'Network diagnostics',
        content: 'Run network diagnostics and analysis',
        keywords: ['network', 'diagnostics', 'connection', 'internet']
    },
    {
        id: 'adv-analyze-logs',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Analytics & Monitoring',
        title: '/analyze-logs',
        description: 'Analyze log files',
        content: 'Analyze log files for issues and patterns',
        keywords: ['analyze', 'logs', 'files', 'patterns']
    },
    {
        id: 'adv-health',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Analytics & Monitoring',
        title: '/health',
        description: 'System health check',
        content: 'Perform system health check',
        keywords: ['health', 'check', 'system', 'status']
    },
    {
        id: 'adv-challenge',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Games & Learning',
        title: '/challenge',
        description: 'Start a coding challenge',
        content: 'Start a coding challenge with specified difficulty',
        keywords: ['challenge', 'coding', 'practice', 'learning']
    },
    {
        id: 'adv-tutorial',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Games & Learning',
        title: '/tutorial',
        description: 'Interactive tutorial',
        content: 'Start an interactive tutorial on a topic',
        keywords: ['tutorial', 'interactive', 'learn', 'guide']
    },
    {
        id: 'adv-quiz',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Games & Learning',
        title: '/quiz',
        description: 'Take a knowledge quiz',
        content: 'Take a knowledge quiz on a topic',
        keywords: ['quiz', 'test', 'knowledge', 'learning']
    },
    {
        id: 'adv-user-stats',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Games & Learning',
        title: '/user-stats',
        description: 'View your learning statistics',
        content: 'View your learning progress and statistics',
        keywords: ['stats', 'statistics', 'learning', 'progress']
    },
    {
        id: 'adv-ascii',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Creative Tools',
        title: '/ascii',
        description: 'Generate ASCII art',
        content: 'Generate ASCII art from text',
        keywords: ['ascii', 'art', 'generate', 'creative']
    },
    {
        id: 'adv-colors',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Creative Tools',
        title: '/colors',
        description: 'Generate color schemes',
        content: 'Generate color schemes and palettes',
        keywords: ['colors', 'scheme', 'palette', 'design']
    },
    {
        id: 'adv-music',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Creative Tools',
        title: '/music',
        description: 'Generate music patterns',
        content: 'Generate music patterns based on mood and length',
        keywords: ['music', 'generate', 'pattern', 'creative']
    },
    {
        id: 'adv-story',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'Creative Tools',
        title: '/story',
        description: 'Generate creative stories',
        content: 'Generate creative stories by genre and length',
        keywords: ['story', 'generate', 'creative', 'writing']
    },
    {
        id: 'adv-setkey',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'User Management',
        title: '/setkey',
        description: 'Set API keys',
        content: 'Set API keys for different AI providers',
        keywords: ['setkey', 'api', 'key', 'configuration']
    },
    {
        id: 'adv-history',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'User Management',
        title: '/history',
        description: 'View chat history',
        content: 'View chat conversation history',
        keywords: ['history', 'chat', 'conversation', 'view']
    },
    {
        id: 'adv-clearhistory',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'User Management',
        title: '/clearhistory',
        description: 'Clear chat history',
        content: 'Clear all chat conversation history',
        keywords: ['clear', 'history', 'delete', 'chat']
    },
    {
        id: 'adv-myactivity',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'User Management',
        title: '/myactivity',
        description: 'View activity log',
        content: 'View your activity log',
        keywords: ['activity', 'log', 'view', 'history']
    },
    {
        id: 'adv-listusers',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'User Management',
        title: '/listusers',
        description: 'List all users (admin)',
        content: 'List all users - admin only',
        keywords: ['users', 'list', 'admin', 'management']
    },
    {
        id: 'adv-resetpw',
        section: 'advanced',
        sectionTitle: 'Advanced Features',
        category: 'User Management',
        title: '/resetpw',
        description: 'Reset password (admin)',
        content: 'Reset user password - admin only',
        keywords: ['reset', 'password', 'admin', 'user']
    },
];
