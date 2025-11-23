from rich.console import Console
from rich.panel import Panel
from rich.layout import Layout
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.markdown import Markdown
from rich.syntax import Syntax
from terminal.games_learning import GamesLearning
import time
import os

class GamesTUI:
    def __init__(self, console: Console):
        self.console = console
        self.games_manager = GamesLearning()

    def show_menu(self):
        while True:
            self.console.clear()
            self.console.print(Panel.fit(
                "[bold cyan] NEXUS AI Games & Learning[/bold cyan]\n\n"
                "1. Python Basics Challenge\n"
                "2. Algorithm Puzzles\n"
                "3. Web Development Challenge\n"
                "4. Tutorials\n"
                "5. Python Quiz\n"
                "6. My Stats\n"
                "0. Back to Main Menu",
                title="Game Menu",
                border_style="cyan"
            ))

            choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4", "5", "6", "0"])

            if choice == "0":
                break
            elif choice == "1":
                self.play_challenge("python_basics")
            elif choice == "2":
                self.play_challenge("algorithm_puzzles")
            elif choice == "3":
                self.play_challenge("web_development")
            elif choice == "4":
                self.show_tutorials()
            elif choice == "5":
                self.play_quiz("python_fundamentals")
            elif choice == "6":
                self.show_stats()

    def play_challenge(self, topic):
        challenge = self.games_manager.get_coding_challenge(topic=topic)
        if "error" in challenge:
            self.console.print(f"[red]{challenge['error']}[/red]")
            time.sleep(2)
            return

        while True:
            self.console.clear()
            self.console.print(Panel(
                f"[bold]{challenge['title']}[/bold]\n"
                f"Difficulty: {challenge['difficulty']}\n\n"
                f"[yellow]Question:[/yellow] {challenge['problem']['question']}\n\n"
                f"[blue]Hints:[/blue] {', '.join(challenge['problem']['hints'])}",
                title="Coding Challenge",
                border_style="green"
            ))

            self.console.print(Syntax(challenge['problem']['starter_code'], "python", theme="monokai", line_numbers=True))
            
            self.console.print("\n[dim]Type 'exit' to quit, 'submit' to enter your code (simulated)[/dim]")
            action = Prompt.ask("Action")

            if action.lower() == 'exit':
                break
            elif action.lower() == 'submit':
                # In a real TUI, we'd open an editor or take multi-line input.
                # For this simplified version, we'll simulate a submission or ask for a one-liner.
                code = Prompt.ask("Enter your one-line solution (or 'skip' to simulate success for demo)")
                
                if code.lower() == 'skip':
                    # Demo mode: Simulate success
                    result = self.games_manager.submit_challenge_solution(
                        challenge['challenge_id'], 
                        challenge['problem']['id'], 
                        "def solution(): return True # simulated", 
                        user="current_user"
                    )
                else:
                    result = self.games_manager.submit_challenge_solution(
                        challenge['challenge_id'], 
                        challenge['problem']['id'], 
                        code, 
                        user="current_user"
                    )

                if "error" in result:
                     self.console.print(f"[red]Error: {result['error']}[/red]")
                else:
                    score_color = "green" if result['score'] == 100 else "yellow"
                    self.console.print(f"\n[{score_color}]Score: {result['score']}%[/{score_color}]")
                    if result['achievements']:
                        self.console.print(f"\n[bold gold1] Achievements Unlocked: {', '.join(result['achievements'])}[/bold gold1]")
                    
                    Prompt.ask("\nPress Enter to continue")
                    break

    def show_tutorials(self):
        # Simplified tutorial viewer
        self.console.print("[yellow]Tutorials feature coming soon![/yellow]")
        time.sleep(2)

    def play_quiz(self, quiz_id):
        # Simplified quiz runner
        self.console.print("[yellow]Quiz feature coming soon![/yellow]")
        time.sleep(2)

    def show_stats(self):
        stats = self.games_manager.get_user_stats("current_user")
        self.console.print(Panel(
            f"Challenges Completed: {stats['challenges_completed']}\n"
            f"Total Score: {stats['total_score']}\n"
            f"Achievements: {len(stats['achievements'])}",
            title="User Statistics",
            border_style="magenta"
        ))
        Prompt.ask("Press Enter to continue")
