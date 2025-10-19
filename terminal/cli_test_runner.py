import importlib.util
import types
import sys
import os
import json

# Insert lightweight mocks for heavy external dependencies
module_names = ['google', 'google.generativeai', 'groq', 'ollama', 'openai']
for name in module_names:
    if name not in sys.modules:
        sys.modules[name] = types.ModuleType(name)

# genai mock (google.generativeai)
import google
genai = types.SimpleNamespace()

def genai_configure(api_key=None):
    genai.api_key = api_key

class DummyGen:
    def __init__(self, *args, **kwargs):
        pass
    def generate_content(self, prompt, generation_config=None):
        class R: pass
        r = R()
        r.text = f"GENAI_RESPONSE: {prompt[:80]}"
        return r

genai.configure = genai_configure
genai.GenerativeModel = DummyGen
sys.modules['google.generativeai'] = genai

# groq mock
class DummyGroq:
    class chat:
        class completions:
            @staticmethod
            def create(*, messages=None, model=None, max_tokens=None):
                class C: pass
                class M: pass
                C.choices = [types.SimpleNamespace(message=types.SimpleNamespace(content='GROQ_RESPONSE'))]
                return C

sys.modules['groq'].Groq = lambda *args, **kwargs: DummyGroq()

# ollama mock
class OllamaMock:
    @staticmethod
    def list():
        return {"models": [{"name": "llama2", "size": 50 * 1024 * 1024, "modified_at": "2023-01-01T00:00:00Z"}]}
    @staticmethod
    def chat(model=None, messages=None):
        return {"message": {"content": f"OLLAMA_RESPONSE for model={model}: {messages[-1]['content'][:60]}"}}

sys.modules['ollama'] = OllamaMock

# openai mock
openai = types.SimpleNamespace()

def openai_chatcreate(*, model=None, messages=None, max_tokens=None):
    return types.SimpleNamespace(choices=[types.SimpleNamespace(message=types.SimpleNamespace(content='OPENAI_RESPONSE'))])

openai.ChatCompletion = types.SimpleNamespace(create=openai_chatcreate)
sys.modules['openai'] = openai

# Load the main module
spec = importlib.util.spec_from_file_location('terminal_main', os.path.join(os.getcwd(), 'terminal', 'main.py'))
main = importlib.util.module_from_spec(spec)
# Execute module
spec.loader.exec_module(main)

ai = main.NexusAI()

commands = [
    '/help',
    '/models',
    '/current-model',
    '/run whoami',
    '/run echo hello',
    '/run rm -rf /',
    '/run ls ..',
    '/git status',
    '/git log 3',
    '/git branch',
    '/task add Test task from runner',
    '/tasks',
    '/task show 1',
    '/setkey openai dummykey1234567890',
    '/switch ollama',
    '/ollama-models',
    'Explain quantum computing',
]

print('=== CLI COMMAND RUNNER OUTPUT ===')
for cmd in commands:
    print('\n--- COMMAND:', cmd)
    try:
        out = ai.process_input(cmd)
    except Exception as e:
        out = f'EXCEPTION: {e}'
    print(out)

# Security checks
print('\n=== SECURITY CHECKS ===')
sec = ai.security
checks = [
    ("simple safe", "hello world"),
    ("blocked pattern", "rm -rf /tmp/test"),
    ("suspicious unicode", "normal\u202etext"),
    ("non-printable", "hello\x00world"),
    ("too long", 'x' * 20000),
]
for name, sample in checks:
    print(f'\n- {name}:')
    try:
        s = sec.sanitize(sample)
        print('SANITIZED:', repr(s))
    except Exception as e:
        print('REJECTED:', type(e).__name__, str(e))

# API key validation checks
print('\n=== API KEY VALIDATION ===')
for provider, key in [('gemini','AI123456789012345678901234567890'), ('groq','gsk_abcdefghijklmnopqrstuvwxyz0123456789ABCDEF'), ('huggingface','hf_123456789012345678901234567890'), ('generic','shortkey')]:
    ok = sec.validate_api_key(key, provider)
    print(provider, key[:16] + '...' , '->', ok)

print('\n=== URL VALIDATION ===')
for url in ['http://example.com', 'https://localhost', 'ftp://files']:
    print(url, '->', sec.validate_url(url))

print('\nDone.')
