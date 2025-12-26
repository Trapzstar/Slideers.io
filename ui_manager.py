"""
UI Manager - Beautiful Interactive CLI Menu System
Handles all user interface interactions with InquirerPy and Rich
"""

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.table import Table
from rich.layout import Layout
from rich.live import Live
from rich import box
import time
import sys
import os

console = Console()

class UIManager:
    """Manages all UI interactions - beautiful and user-friendly"""
    
    def __init__(self):
        self.version = "2.0.0"
        
    def clear(self):
        """Clear screen safely"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_welcome(self):
        """Show welcome screen"""
        self.clear()
        
        welcome = Panel.fit(
            "[bold cyan]🎤 SlideSense.id[/bold cyan]\n"
            "[dim]Voice-Controlled PowerPoint Presentation[/dim]\n\n"
            "[green]✨ Kontrol presentasi dengan suara Anda[/green]\n"
            "[yellow]♿ Fitur aksesibilitas untuk semua audiens[/yellow]\n\n"
            f"[dim]Version {self.version}[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(welcome)
        console.print()
        time.sleep(0.8)
    
    def show_main_menu(self):
        """Main menu with clear options"""
        
        choices = [
            Choice(value="start", name="🚀 Mulai Voice Control"),
            Choice(value="test_mic", name="🎤 Test Microphone"),
            Separator(),
            Choice(value="tutorial", name="📖 Tutorial & Bantuan"),
            Choice(value="about", name="ℹ️  Tentang Program"),
            Separator(),
            Choice(value="exit", name="🚪 Keluar")
        ]
        
        try:
            action = inquirer.select(
                message="Pilih menu:",
                choices=choices,
                default="start",
                pointer="👉",
                style={
                    "pointer": "cyan bold",
                    "highlighted": "cyan bold",
                    "question": "bold"
                }
            ).execute()
            
            return action
        except KeyboardInterrupt:
            return "exit"
    
    def show_microphone_setup(self, devices_list):
        """Interactive microphone setup wizard"""
        
        console.print("\n[bold cyan]🎙️  Setup Microphone[/bold cyan]\n")
        
        # Ask setup method
        setup_method = inquirer.select(
            message="Bagaimana Anda ingin setup microphone?",
            choices=[
                Choice(value="auto", name="✨ Auto-detect (Recommended)"),
                Choice(value="manual", name="🔧 Pilih manual dari list"),
            ],
            default="auto"
        ).execute()
        
        return setup_method
    
    def show_microphone_list(self, devices):
        """Show microphone list for manual selection"""
        
        if not devices:
            console.print("[red]❌ Tidak ada microphone terdeteksi[/red]")
            return None
        
        choices = []
        for device in devices:
            idx = device.get('index', 0)
            name = device.get('name', 'Unknown')
            channels = device.get('channels', 0)
            
            display_name = f"#{idx}: {name}"
            if channels > 0:
                display_name += f" [{channels} channels]"
            
            choices.append(Choice(value=idx, name=display_name))
        
        try:
            selected = inquirer.select(
                message="Pilih microphone:",
                choices=choices,
                pointer="🎯"
            ).execute()
            
            return selected
        except KeyboardInterrupt:
            return None
    
    def show_auto_detect_progress(self):
        """Show progress while auto-detecting microphone"""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console,
            transient=True
        ) as progress:
            task = progress.add_task("[cyan]🔍 Mencari microphone terbaik...", total=100)
            
            for i in range(100):
                progress.update(task, advance=1)
                time.sleep(0.01)
        
        console.print("[green]✅ Auto-detect selesai![/green]\n")
    
    def show_device_found(self, device_name, device_index):
        """Show device found message"""
        
        device_panel = Panel(
            f"[bold green]✅ Microphone Terdeteksi[/bold green]\n\n"
            f"[cyan]Device:[/cyan] {device_name}\n"
            f"[cyan]Index:[/cyan] {device_index}",
            border_style="green"
        )
        
        console.print(device_panel)
        console.print()
        
        confirm = inquirer.confirm(
            message="Gunakan microphone ini?",
            default=True
        ).execute()
        
        return confirm
    
    def show_microphone_test_start(self, duration=3):
        """Show microphone test starting"""
        
        console.print(f"\n[bold cyan]🎤 Testing Microphone ({duration} detik)[/bold cyan]")
        console.print("[yellow]💡 Bicara sekarang untuk test...[/yellow]\n")
    
    def show_test_progress(self, duration=3):
        """Show test progress"""
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            console=console
        ) as progress:
            task = progress.add_task("[cyan]Recording...", total=duration * 10)
            
            for i in range(duration * 10):
                progress.update(task, advance=1)
                time.sleep(0.1)
    
    def show_test_result(self, success, message=""):
        """Show test result"""
        
        if success:
            console.print("[bold green]✅ Test Berhasil![/bold green]")
            if message:
                console.print(f"[green]📝 Detected: '{message}'[/green]")
        else:
            console.print("[bold red]❌ Test Gagal[/bold red]")
            if message:
                console.print(f"[yellow]💡 {message}[/yellow]")
        
        console.print()
        
        inquirer.confirm(
            message="Lanjutkan?",
            default=True
        ).execute()
    
    def show_voice_control_starting(self):
        """Show voice control is starting"""
        
        self.clear()
        
        console.print(Panel(
            "[bold green]🎤 Voice Control Sedang Dimulai...[/bold green]\n"
            "[dim]Mempersiapkan sistem...[/dim]",
            border_style="green"
        ))
        
        time.sleep(1)
    
    def show_voice_control_active(self):
        """Show voice control active interface"""
        
        self.clear()
        
        # Header
        header = Panel(
            "[bold green]🎤 VOICE CONTROL AKTIF[/bold green]\n"
            "[dim]Bicara perintah atau tekan Ctrl+C untuk berhenti[/dim]",
            border_style="green"
        )
        console.print(header)
        
        # Quick guide
        guide = Table(show_header=False, box=box.SIMPLE, padding=(0, 1))
        guide.add_column(style="cyan bold", width=15)
        guide.add_column()
        
        guide.add_row("Status", "[green]● Listening[/green]")
        guide.add_row("Mode", "Voice Only")
        guide.add_row("Help", "Katakan 'help menu'")
        guide.add_row("Stop", "Katakan 'stop program'")
        
        console.print(guide)
        console.print()
    
    def show_listening(self):
        """Show listening indicator"""
        
        console.print("🎤 " + "="*56)
        console.print("[bold cyan]LISTENING...[/bold cyan] (bicara sekarang)")
        console.print("="*60)
    
    def show_command_detected(self, command, text, confidence):
        """Show command detected with confidence"""
        
        # Color based on confidence
        if confidence >= 80:
            color = "green"
            icon = "✅"
            bar = "████████████████████"
        elif confidence >= 60:
            color = "yellow"
            icon = "⚠️"
            filled = int(confidence / 5)
            bar = "█" * filled + "░" * (20 - filled)
        else:
            color = "red"
            icon = "❌"
            filled = int(confidence / 5)
            bar = "█" * filled + "░" * (20 - filled)
        
        console.print(f"\n    📝 Detected: '{text}'")
        console.print(f"    {icon} [{color}]Command: {command}[/{color}]")
        console.print(f"    📊 Confidence: [{color}][{bar}][/{color}] {confidence:.0f}%")
    
    def show_command_feedback(self, feedback_text):
        """Show command execution feedback"""
        console.print(f"    {feedback_text}")
    
    def show_no_speech(self):
        """Show no speech detected"""
        console.print("    [yellow]⏰ Tidak mendengar suara[/yellow]")
        console.print("    [dim]💡 Coba bicara lebih keras atau dekat ke microphone[/dim]")
    
    def show_unknown_command(self, text):
        """Show unknown command"""
        console.print(f"    [yellow]❓ Perintah tidak dikenali: '{text}'[/yellow]")
        console.print("    [dim]💡 Katakan 'help menu' untuk daftar perintah[/dim]")
    
    def show_tutorial(self):
        """Show interactive tutorial"""
        
        self.clear()
        
        console.print(Panel(
            "[bold cyan]📖 Tutorial SlideSense.id[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
        
        # Section 1
        console.print("[bold cyan]🎯 Perintah Dasar[/bold cyan]")
        console.print("  • [green]'next slide'[/green] atau [green]'lanjut slide'[/green] - Slide maju")
        console.print("  • [green]'back slide'[/green] atau [green]'mundur slide'[/green] - Slide mundur")
        console.print("  • [green]'help menu'[/green] - Bantuan lengkap")
        console.print("  • [green]'stop program'[/green] - Keluar\n")
        
        # Section 2
        console.print("[bold cyan]🎤 Tips Microphone[/bold cyan]")
        console.print("  • Jarak ideal: 15-30cm dari mulut")
        console.print("  • Bicara jelas tapi santai")
        console.print("  • Kurangi background noise")
        console.print("  • Pastikan microphone tidak mute\n")
        
        # Section 3
        console.print("[bold cyan]🎬 Cara Menggunakan[/bold cyan]")
        console.print("  1. Buka PowerPoint file yang ingin dipresentasikan")
        console.print("  2. Tekan F5 untuk mulai slideshow")
        console.print("  3. Kembali ke window SlideSense.id")
        console.print("  4. Mulai bicara perintah!")
        console.print("  5. Program akan kontrol PowerPoint otomatis\n")
        
        # Section 4
        console.print("[bold cyan]✨ Fitur Lanjutan[/bold cyan]")
        console.print("  • [green]'open slide show'[/green] - Buka presentasi (tekan F5)")
        console.print("  • [green]'close slide show'[/green] - Tutup presentasi (tekan ESC)")
        console.print("  • [green]'popup on'[/green] - Tampilkan guide untuk audiens")
        console.print("  • [green]'caption on'[/green] - Aktifkan subtitle\n")
        
        inquirer.confirm(
            message="Kembali ke menu utama?",
            default=True
        ).execute()
    
    def show_about(self):
        """Show about screen"""
        
        self.clear()
        
        about = Panel.fit(
            "[bold cyan]SlideSense.id[/bold cyan]\n"
            f"[dim]Version {self.version}[/dim]\n\n"
            "Voice-controlled PowerPoint presentation system\n"
            "dengan fitur accessibility untuk semua audiens.\n\n"
            "[bold]Fitur Utama:[/bold]\n"
            "• Voice recognition dengan Google Speech API\n"
            "• Smart command detection dengan fuzzy matching\n"
            "• Real-time feedback dan confidence scoring\n"
            "• Accessibility popup untuk audiens difabel\n"
            "• Multi-language caption support\n\n"
            "[yellow]Dibuat dengan ❤️ untuk pendidikan[/yellow]\n"
            "[dim]Gratis dan open source[/dim]\n\n"
            "[dim]License: Apache 2.0[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(about)
        console.print()
        
        inquirer.confirm(
            message="Kembali ke menu utama?",
            default=True
        ).execute()
    
    def show_error(self, title, message, suggestions=None):
        """Show error with helpful suggestions"""
        
        content = f"[bold red]{title}[/bold red]\n\n{message}"
        
        if suggestions:
            content += "\n\n[yellow]💡 Saran:[/yellow]"
            for suggestion in suggestions:
                content += f"\n  • {suggestion}"
        
        error_panel = Panel(
            content,
            border_style="red",
            padding=(1, 2)
        )
        
        console.print("\n")
        console.print(error_panel)
        console.print()
    
    def show_goodbye(self):
        """Show goodbye message"""
        
        self.clear()
        
        goodbye = Panel.fit(
            "[bold cyan]Terima kasih telah menggunakan[/bold cyan]\n"
            "[bold cyan]SlideSense.id[/bold cyan]\n\n"
            "[yellow]See you next time! 👋[/yellow]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(goodbye)
        console.print()
    
    def show_initializing(self):
        """Show initializing message"""
        
        console.print("\n[bold cyan]⚙️  Initializing System...[/bold cyan]")
    
    def show_initialization_step(self, step_name, success=True):
        """Show initialization step result"""
        
        if success:
            console.print(f"  [green]✅ {step_name}[/green]")
        else:
            console.print(f"  [red]❌ {step_name}[/red]")
    
    def pause(self, message="Tekan Enter untuk melanjutkan..."):
        """Pause with message"""
        console.print(f"\n[dim]{message}[/dim]")
        input()


# Global instance
ui = UIManager()