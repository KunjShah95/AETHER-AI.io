// IIFE to encapsulate the code
(function() {
// DOM Elements
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('nav-menu');
const typingText = document.getElementById('typing-text');
const terminalOutput = document.getElementById('terminal-output');
const notification = document.getElementById('notification');
const notificationText = document.getElementById('notification-text');

// Download tracking
let downloadCount = parseInt(localStorage.getItem('nexusDownloadCount') || '0');
if (document.getElementById('download-counter')) {
    document.getElementById('download-counter').textContent = downloadCount;
}

function incrementDownloadCount() {
    downloadCount++;
    localStorage.setItem('nexusDownloadCount', downloadCount);
    if (document.getElementById('download-counter')) {
        document.getElementById('download-counter').textContent = downloadCount;
    }
}

window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.btn-download').forEach(btn => {
        btn.addEventListener('click', incrementDownloadCount);
    });
});

// Mobile Navigation
if (hamburger && navMenu) {
    hamburger.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
}

// Close mobile menu when clicking on a link
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', () => {
        if (navMenu) navMenu.classList.remove('active');
        if (hamburger) hamburger.classList.remove('active');
    });
});

// Typing Animation for Terminal
const commands = [
    'nexus --help',
    'nexus chat "Hello, how are you?"',
    'nexus model --list',
    'nexus config --set model=gemini',
    'nexus generate --prompt "Write a Python function"'
];

const responses = [
    'NEXUS AI Terminal v3.0<br>Usage: nexus [command] [options]<br><br>Commands:<br>  chat      Start interactive chat<br>  generate  Generate content<br>  model     Manage AI models<br>  config    Configuration settings',
    'AI: Hello! I\'m doing great, thank you for asking! How can I assist you today?',
    'Available Models:<br>✓ Gemini Pro<br>✓ Groq Llama<br>✓ HuggingFace Transformers<br>✓ DeepSeek Coder<br>✓ Ollama Local<br>✓ Claude Sonnet<br>✓ GPT-4<br>✓ Mistral AI',
    'Configuration updated successfully!<br>Active model: Gemini Pro<br>Status: Ready',
    'def fibonacci(n):<br>    if n <= 1:<br>        return n<br>    return fibonacci(n-1) + fibonacci(n-2)<br><br># Generated with NEXUS AI'
];

let currentCommandIndex = 0;
let currentCharIndex = 0;
let isTyping = false;
let currentTypingTextElement;

function typeCommand() {
    if (isTyping || !terminalOutput) return;

    isTyping = true;
    const command = commands[currentCommandIndex];
    
    // Create a new line for the command
    const promptElement = document.createElement('div');
    promptElement.className = 'terminal-prompt';
    promptElement.innerHTML = '<span>&gt;</span> ';
    
    currentTypingTextElement = document.createElement('span');
    promptElement.appendChild(currentTypingTextElement);
    terminalOutput.appendChild(promptElement);

    const textNode = document.createTextNode('');
    currentTypingTextElement.appendChild(textNode);
    currentCharIndex = 0;

    const typeInterval = setInterval(() => {
        if (currentCharIndex < command.length) {
            textNode.data += command[currentCharIndex];
            currentCharIndex++;
        } else {
            clearInterval(typeInterval);
            setTimeout(showResponse, 1000);
        }
    }, 100);
}

function showResponse() {
    if (!terminalOutput) return;

    const response = responses[currentCommandIndex];
    const responseElement = document.createElement('div');
    responseElement.className = 'terminal-response';
    responseElement.style.marginBottom = '1rem';
    responseElement.style.color = '#94a3b8';
    responseElement.innerHTML = response;

    terminalOutput.appendChild(responseElement);

    // Scroll to bottom
    terminalOutput.scrollTop = terminalOutput.scrollHeight;

    setTimeout(() => {
        isTyping = false;
        currentCommandIndex = (currentCommandIndex + 1) % commands.length;
        typeCommand();
    }, 3000);
}

// Counter Animation
function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    counters.forEach(counter => {
        const target = parseInt(counter.getAttribute('data-target'));
        if (isNaN(target)) return;
        
        const increment = target / 100;
        let current = 0;
        
        const updateCounter = () => {
            if (current < target) {
                current += increment;
                if (counter.id === 'download-counter') {
                    counter.textContent = Math.ceil(current).toLocaleString();
                } else {
                    counter.textContent = Math.ceil(current);
                }
                setTimeout(updateCounter, 20);
            } else {
                if (counter.id === 'download-counter') {
                    counter.textContent = target.toLocaleString();
                } else {
                    counter.textContent = target;
                }
            }
        };
        
        updateCounter();
    });
}

// Update download counter in real-time
function updateDownloadCounter() {
    const downloadCountElement = document.getElementById('download-counter');
    if (downloadCountElement) {
        downloadCountElement.textContent = downloadCount.toLocaleString();
        downloadCountElement.setAttribute('data-target', downloadCount);
    }
}

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            if (entry.target.classList.contains('hero-stats')) {
                animateCounters();
            }
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Smooth scrolling for navigation links
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
}

// Download functionality with real-time counter update
function downloadFile(os) {
    let url = '';
    let filename = '';
    let fallbackUrl = '';
    
    if (os === 'Windows') {
        url = './terminal/install_windows.zip';
        filename = 'nexus-ai-installer-windows.zip';
        fallbackUrl = 'https://github.com/KunjShah95/NEXUS-AI.io/raw/main/terminal/install.bat';
    } else if (os === 'Linux') {
        url = './terminal/install_linux.zip';
        filename = 'nexus-ai-installer-linux.zip';
        fallbackUrl = 'https://github.com/KunjShah95/NEXUS-AI.io/raw/main/terminal/install.sh';
    } else if (os === 'macOS') {
        url = './terminal/install_mac.zip';
        filename = 'nexus-ai-installer-mac.zip';
        fallbackUrl = 'https://github.com/KunjShah95/NEXUS-AI.io/raw/main/terminal/install_mac.sh';
    }
    
    if (!url) return;
    
    // Primary download attempt (local ZIP file)
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.style.display = 'none';
    document.body.appendChild(a);
    
    try {
        a.click();
        incrementDownloadCount();
        showNotification(`✅ ${filename} download started successfully!`);
        console.log(`Download initiated for ${filename}`);
    } catch (error) {
        console.error('Primary download failed, trying fallback:', error);
        
        // Fallback: try to download individual installer file
        const fallbackLink = document.createElement('a');
        fallbackLink.href = fallbackUrl;
        fallbackLink.download = `nexus-installer-${os.toLowerCase()}.${fallbackUrl.endsWith('.bat') ? 'bat' : 'sh'}`;
        fallbackLink.style.display = 'none';
        document.body.appendChild(fallbackLink);
        
        try {
            fallbackLink.click();
            incrementDownloadCount();
            showNotification(`📦 Fallback download initiated for ${os}. Please also download other required files from GitHub.`);
        } catch (fallbackError) {
            console.error('Fallback download also failed:', fallbackError);
            showNotification(`❌ Download failed. Please visit our GitHub repository: https://github.com/KunjShah95/NEXUS-AI.io`);
            // Open GitHub as last resort
            setTimeout(() => {
                window.open('https://github.com/KunjShah95/NEXUS-AI.io/tree/main/terminal', '_blank');
            }, 2000);
        }
        
        document.body.removeChild(fallbackLink);
    }
    
    document.body.removeChild(a);
}

function openGuide() {
    showNotification('📖 Opening installation guide...');
    setTimeout(() => {
        window.open('#', '_blank');
    }, 500);
}

function openGitHub() {
    showNotification('🚀 Opening GitHub repository...');
    setTimeout(() => {
        window.open('https://github.com/KunjShah95/NEXUS-AI.io', '_blank');
    }, 500);
}

// Notification system
function showNotification(message) {
    if (notificationText && notification) {
        notificationText.textContent = message;
        notification.classList.add('show');
        
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }
}

// Demo functionality - opens YouTube video
function startDemo() {
    showNotification('🎬 Opening YouTube demo...');
    
    // Open YouTube demo
    setTimeout(() => {
        window.open('https://www.youtube.com/watch?v=DLyrTzcYgbI', '_blank');
    }, 500);
    
    // Also scroll to terminal for visual effect
    const terminal = document.querySelector('.terminal-mockup');
    if (terminal) {
        terminal.scrollIntoView({
            behavior: 'smooth',
            block: 'center'
        });
        
        // Add highlight effect
        terminal.style.boxShadow = '0 0 30px rgba(99, 102, 241, 0.5)';
        setTimeout(() => {
            terminal.style.boxShadow = '';
        }, 2000);
    }
}

// Parallax effect for hero section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.hero-visual');
    
    if (parallax) {
        const speed = scrolled * 0.2; // Reduced speed for better performance
        parallax.style.transform = `translateY(${speed}px)`;
    }
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 100) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
            navbar.style.backdropFilter = 'blur(20px)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.9)';
            navbar.style.backdropFilter = 'blur(20px)';
        }
    }
});

// Add click effects to buttons
document.addEventListener('click', function(e) {
    if (e.target.closest('.btn')) {
        const btn = e.target.closest('.btn');
        const ripple = document.createElement('span');
        const rect = btn.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = e.clientX - rect.left - size / 2;
        const y = e.clientY - rect.top - size / 2;
        
        ripple.style.width = ripple.style.height = size + 'px';
        ripple.style.left = x + 'px';
        ripple.style.top = y + 'px';
        ripple.classList.add('ripple');
        
        btn.appendChild(ripple);
        
        setTimeout(() => {
            if (ripple.parentNode) {
                ripple.remove();
            }
        }, 600);
    }
});

// Add ripple effect styles
const style = document.createElement('style');
style.textContent = `
    .btn {
        position: relative;
        overflow: hidden;
    }
    
    .ripple {
        position: absolute;
        border-radius: 50%;
        background: rgba(255, 255, 255, 0.3);
        transform: scale(0);
        animation: ripple-animation 0.6s linear;
        pointer-events: none;
    }
    
    @keyframes ripple-animation {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Easter egg: Konami code
let konamiCode = [];
const konamiSequence = [
    'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
    'KeyB', 'KeyA'
];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.code);
    
    if (konamiCode.length > konamiSequence.length) {
        konamiCode.shift();
    }
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        showNotification('🎉 Easter egg activated! You found the secret!');
        document.body.style.filter = 'hue-rotate(180deg)';
        setTimeout(() => {
            document.body.style.filter = '';
        }, 3000);
        konamiCode = [];
    }
});

// Add keyboard navigation
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        if (navMenu) navMenu.classList.remove('active');
        if (hamburger) hamburger.classList.remove('active');
    }
});

// Scroll to top when clicking the NEXUS AI logo
const nexusLogo = document.getElementById('nexus-logo');
if (nexusLogo) {
    nexusLogo.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    console.log('🚀 NEXUS AI Website Loaded Successfully!');
    
    // Initialize download counter on page load
    updateDownloadCounter();
    
    // Start typing animation
    setTimeout(typeCommand, 2000);
    
    // Observe elements for animation
    document.querySelectorAll('.feature-card, .download-card, .hero-stats').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        observer.observe(el);
    });
    
    // Add loading animation
    const heroElements = document.querySelectorAll('.hero-content > *');
    heroElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'all 0.6s ease';
        
        setTimeout(() => {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }, index * 200);
    });
    
    // Add subtle entrance animation to particles
    setTimeout(() => {
        document.querySelectorAll('.particle').forEach((particle, index) => {
            particle.style.opacity = '0.6';
            particle.style.animation = `float 6s ease-in-out infinite ${index * 0.5}s`;
        });
    }, 1000);
});

// Update download counter every 30 seconds to simulate real activity
setInterval(() => {
    // Randomly increment download count (1-3 downloads)
    const randomIncrement = Math.floor(Math.random() * 3) + 1;
    downloadCount += randomIncrement;
    localStorage.setItem('nexusDownloadCount', downloadCount.toString());
    updateDownloadCounter();
}, 30000); // Every 30 seconds

// Performance optimization
let ticking = false;

function updateOnScroll() {
    // Parallax effect
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.hero-visual');
    
    if (parallax) {
        const speed = scrolled * 0.2;
        parallax.style.transform = `translateY(${speed}px)`;
    }
    
    // Navbar effect
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (scrolled > 100) {
            navbar.style.background = 'rgba(15, 23, 42, 0.95)';
        } else {
            navbar.style.background = 'rgba(15, 23, 42, 0.9)';
        }
    }
    
    ticking = false;
}

window.addEventListener('scroll', () => {
    if (!ticking) {
        requestAnimationFrame(updateOnScroll);
        ticking = true;
    }
});

// Event Listeners for buttons
document.addEventListener('DOMContentLoaded', () => {
    // Handle download buttons
    document.querySelectorAll('[onclick^="downloadFile("]').forEach(btn => {
        const onclickAttr = btn.getAttribute('onclick');
        if (onclickAttr) {
            const match = onclickAttr.match(/downloadFile\('([^']+)'\)/);
            if (match) {
                const platform = match[1];
                btn.removeAttribute('onclick'); // Remove inline onclick
                btn.addEventListener('click', (e) => {
                    e.preventDefault();
                    downloadFile(platform);
                });
            }
        }
    });
    
    // Handle other buttons
    const demoBtn = document.querySelector('button[onclick="startDemo()"]');
    if (demoBtn) {
        demoBtn.removeAttribute('onclick');
        demoBtn.addEventListener('click', startDemo);
    }
    
    const downloadNavBtn = document.querySelector('button[onclick="scrollToSection(\'download\')"]');
    if (downloadNavBtn) {
        downloadNavBtn.removeAttribute('onclick');
        downloadNavBtn.addEventListener('click', () => scrollToSection('download'));
    }
});

// Smooth Scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();

        const targetId = this.getAttribute('href');
        const targetElement = document.querySelector(targetId);

        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 100, // Offset for fixed navbar
                behavior: 'smooth'
            });
        }
    });
});

})();