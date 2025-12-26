"""
Beautiful Interactive CLI Menu untuk SlideSense.id
Menggunakan InquirerPy untuk pengalaman user yang modern dan intuitif
"""

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich import box
import time
import sys

# Initialize Rich console untuk beautiful output
console = Console()

class BeautifulMenu:
    """Menu system yang cantik dan user-friendly"""
    
    def __init__(self):
        self.voice = None
        self.detector = None
        self.ppt = None
        self.popup = None
        
    def show_welcome_screen(self):
        """
        Tampilkan welcome screen yang cantik.
        Ini adalah first impression user - harus welcoming dan jelas.
        """
        console.clear()
        
        # Logo/Banner yang simple tapi eye-catching
        welcome_panel = Panel.fit(
            "[bold cyan]🎤 SlideSense.id[/bold cyan]\n"
            "[dim]Voice-Controlled PowerPoint Presentation[/dim]\n\n"
            "[green]✨ Control presentasi dengan suara Anda[/green]\n"
            "[yellow]♿ Fitur aksesibilitas untuk semua[/yellow]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(welcome_panel)
        console.print()
        
    def show_main_menu(self):
        """
        Main menu dengan pilihan yang jelas dan terstruktur.
        Menggunakan inquirer untuk interactive selection.
        """
        
        # Choices yang descriptive dan mudah dipahami
        choices = [
            Choice(value="start", name="🚀 Mulai Voice Control"),
            Choice(value="test", name="🎤 Test Microphone"),
            Choice(value="settings", name="⚙️  Pengaturan"),
            Separator(),  # Visual separator untuk grouping
            Choice(value="tutorial", name="📖 Tutorial & Bantuan"),
            Choice(value="about", name="ℹ️  Tentang Program"),
            Separator(),
            Choice(value="exit", name="🚪 Keluar")
        ]
        
        # Inquirer dengan custom style
        action = inquirer.select(
            message="Pilih menu:",
            choices=choices,
            default="start",
            pointer="👉",  # Custom pointer
            style={
                "pointer": "cyan bold",
                "highlighted": "cyan bold",
                "question": "bold"
            }
        ).execute()
        
        return action
    
    def show_microphone_setup_wizard(self):
        """
        Setup wizard untuk microphone - guided dan tidak menakutkan.
        Ini contoh bagaimana membuat setup yang complex menjadi simple.
        """
        console.print("\n[bold cyan]🎙️  Setup Microphone[/bold cyan]\n")
        
        # Step 1: Auto-detect atau manual?
        setup_method = inquirer.select(
            message="Bagaimana Anda ingin setup microphone?",
            choices=[
                Choice(value="auto", name="✨ Auto-detect (Recommended)"),
                Choice(value="manual", name="🔧 Pilih manual"),
            ],
            default="auto"
        ).execute()
        
        if setup_method == "auto":
            # Show progress untuk auto-detection
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console
            ) as progress:
                task = progress.add_task("[cyan]Mencari microphone terbaik...", total=None)
                
                # Simulate detection (replace dengan actual code)
                time.sleep(1)
                best_device = self._detect_best_microphone()
                
                progress.update(task, completed=True)
            
            console.print(f"[green]✅ Microphone terdeteksi: {best_device['name']}[/green]")
            
            # Konfirmasi
            confirm = inquirer.confirm(
                message="Gunakan microphone ini?",
                default=True
            ).execute()
            
            if confirm:
                return best_device
            else:
                return self._show_manual_microphone_selection()
        else:
            return self._show_manual_microphone_selection()
    
    def _show_manual_microphone_selection(self):
        """Manual microphone selection dengan list yang cantik"""
        
        # Get available devices
        devices = self._get_available_microphones()
        
        # Create choices dengan informasi yang helpful
        choices = []
        for i, device in enumerate(devices):
            # Add device info yang user-friendly
            name = f"#{i}: {device['name']}"
            if device.get('is_default'):
                name += " [DEFAULT]"
            if device.get('quality') == 'excellent':
                name += " ⭐⭐⭐"
            elif device.get('quality') == 'good':
                name += " ⭐⭐"
            
            choices.append(Choice(value=i, name=name))
        
        selected = inquirer.select(
            message="Pilih microphone:",
            choices=choices,
            pointer="🎯"
        ).execute()
        
        return devices[selected]
    
    def show_voice_control_interface(self):
        """
        Interface saat voice control aktif - minimal dan tidak mengganggu.
        Hanya show info penting.
        """
        console.clear()
        
        # Header yang compact
        console.print(Panel(
            "[bold green]🎤 Voice Control AKTIF[/bold green]\n"
            "[dim]Bicara perintah atau tekan Ctrl+C untuk stop[/dim]",
            border_style="green"
        ))
        
        # Status table yang simple
        status_table = Table(show_header=False, box=box.SIMPLE)
        status_table.add_column(style="cyan")
        status_table.add_column()
        
        status_table.add_row("Status", "[green]● Listening[/green]")
        status_table.add_row("Mode", "Voice Only")
        status_table.add_row("Help", "Katakan 'help menu'")
        
        console.print(status_table)
        console.print()
        
    def show_command_feedback(self, command, confidence):
        """
        Feedback setelah command terdeteksi - simple dan visual.
        """
        # Color based on confidence
        if confidence >= 80:
            color = "green"
            icon = "✅"
        elif confidence >= 60:
            color = "yellow"
            icon = "⚠️"
        else:
            color = "red"
            icon = "❌"
        
        console.print(
            f"{icon} [{color}]Command: {command} ({confidence}%)[/{color}]"
        )
    
    def show_tutorial(self):
        """
        Tutorial yang interactive - tidak boring wall of text.
        """
        console.clear()
        
        console.print(Panel(
            "[bold cyan]📖 Tutorial Cepat[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
        
        # Tutorial dengan sections yang jelas
        tutorial_sections = [
            {
                "title": "🎯 Dasar Voice Control",
                "content": [
                    "• Katakan 'next slide' untuk maju",
                    "• Katakan 'back slide' untuk mundur",
                    "• Katakan 'help menu' untuk bantuan"
                ]
            },
            {
                "title": "🎤 Tips Microphone",
                "content": [
                    "• Jarak ideal: 15-30cm dari mulut",
                    "• Bicara jelas tapi santai",
                    "• Kurangi noise background"
                ]
            },
            {
                "title": "✨ Fitur Khusus",
                "content": [
                    "• 'popup on' - Tampilkan guide untuk audience",
                    "• 'caption on' - Aktifkan subtitle",
                    "• 'show analytics' - Lihat statistik"
                ]
            }
        ]
        
        for section in tutorial_sections:
            console.print(f"\n[bold]{section['title']}[/bold]")
            for item in section['content']:
                console.print(f"  {item}")
        
        console.print()
        inquirer.confirm(
            message="Lanjutkan?",
            default=True
        ).execute()
    
    def show_settings_menu(self):
        """
        Settings menu dengan kategorisasi yang jelas.
        """
        console.clear()
        
        console.print(Panel(
            "[bold cyan]⚙️  Pengaturan[/bold cyan]",
            border_style="cyan"
        ))
        console.print()
        
        setting_choices = [
            Choice(value="mic", name="🎤 Microphone Settings"),
            Choice(value="voice", name="🗣️  Voice Recognition Settings"),
            Choice(value="popup", name="📺 Popup & Display Settings"),
            Separator(),
            Choice(value="back", name="← Kembali")
        ]
        
        selected = inquirer.select(
            message="Pilih kategori:",
            choices=setting_choices
        ).execute()
        
        if selected == "mic":
            self._show_microphone_settings()
        elif selected == "voice":
            self._show_voice_settings()
        elif selected == "popup":
            self._show_popup_settings()
    
    def _show_microphone_settings(self):
        """Microphone settings yang interactive"""
        
        # Example: Sensitivity slider
        sensitivity = inquirer.number(
            message="Sensitivitas microphone (0-100):",
            min_allowed=0,
            max_allowed=100,
            default=50,
            validate=lambda x: 0 <= x <= 100
        ).execute()
        
        # Noise reduction toggle
        noise_reduction = inquirer.confirm(
            message="Aktifkan noise reduction?",
            default=True
        ).execute()
        
        console.print(f"\n[green]✅ Settings disimpan![/green]")
        time.sleep(1)
    
    def _show_voice_settings(self):
        """Voice recognition settings"""
        
        # Language selection
        language = inquirer.select(
            message="Bahasa recognition:",
            choices=[
                Choice(value="id", name="🇮🇩 Bahasa Indonesia"),
                Choice(value="en", name="🇺🇸 English"),
            ],
            default="id"
        ).execute()
        
        # Confidence threshold
        threshold = inquirer.number(
            message="Minimum confidence (0-100):",
            min_allowed=0,
            max_allowed=100,
            default=70
        ).execute()
        
        console.print(f"\n[green]✅ Settings disimpan![/green]")
        time.sleep(1)
    
    def _show_popup_settings(self):
        """Popup display settings"""
        
        # Position
        position = inquirer.select(
            message="Posisi popup:",
            choices=[
                Choice(value="bottom-right", name="Kanan Bawah"),
                Choice(value="bottom-left", name="Kiri Bawah"),
                Choice(value="top-right", name="Kanan Atas"),
                Choice(value="top-left", name="Kiri Atas"),
            ],
            default="bottom-right"
        ).execute()
        
        # Transparency
        transparency = inquirer.number(
            message="Transparansi (0-100):",
            min_allowed=0,
            max_allowed=100,
            default=85
        ).execute()
        
        console.print(f"\n[green]✅ Settings disimpan![/green]")
        time.sleep(1)
    
    def show_about(self):
        """About screen dengan credits"""
        console.clear()
        
        about_panel = Panel.fit(
            "[bold cyan]SlideSense.id[/bold cyan]\n"
            "[dim]Version 2.0.0[/dim]\n\n"
            "Voice-controlled PowerPoint presentation\n"
            "dengan fitur accessibility untuk semua.\n\n"
            "[yellow]Dibuat dengan ❤️ untuk pendidikan[/yellow]\n\n"
            "[dim]License: Apache 2.0[/dim]",
            border_style="cyan",
            padding=(1, 2)
        )
        
        console.print(about_panel)
        console.print()
        
        inquirer.confirm(
            message="Kembali ke menu?",
            default=True
        ).execute()
    
    def show_error(self, error_type, message):
        """
        Error handling yang user-friendly - tidak menakutkan.
        """
        console.print()
        
        error_panel = Panel(
            f"[bold red]❌ Oops! Ada masalah[/bold red]\n\n"
            f"{message}\n\n"
            "[yellow]💡 Saran:[/yellow]\n"
            "• Cek koneksi microphone\n"
            "• Restart program\n"
            "• Lihat tutorial untuk bantuan",
            border_style="red",
            padding=(1, 2)
        )
        
        console.print(error_panel)
        console.print()
    
    # Helper methods (simplified)
    def _detect_best_microphone(self):
        """Detect best microphone (placeholder)"""
        return {
            'name': 'Microphone Array (Realtek)',
            'index': 1,
            'quality': 'excellent'
        }
    
    def _get_available_microphones(self):
        """Get available microphones (placeholder)"""
        return [
            {'name': 'Default Microphone', 'index': 0, 'quality': 'good', 'is_default': True},
            {'name': 'Microphone Array (Realtek)', 'index': 1, 'quality': 'excellent'},
            {'name': 'USB Microphone', 'index': 2, 'quality': 'good'},
        ]
    
    def run(self):
        """
        Main run loop dengan error handling yang proper.
        """
        try:
            self.show_welcome_screen()
            time.sleep(1)
            
            while True:
                action = self.show_main_menu()
                
                if action == "start":
                    # Setup microphone first
                    device = self.show_microphone_setup_wizard()
                    
                    # Start voice control
                    self.show_voice_control_interface()
                    
                    # TODO: Actual voice control loop here
                    console.print("\n[yellow]Voice control akan dimulai...[/yellow]")
                    console.print("[dim]Press Ctrl+C to stop[/dim]\n")
                    
                    try:
                        # Simulate voice control
                        while True:
                            time.sleep(0.1)
                    except KeyboardInterrupt:
                        console.print("\n[yellow]Voice control stopped[/yellow]")
                        time.sleep(1)
                
                elif action == "test":
                    console.print("\n[cyan]Testing microphone...[/cyan]")
                    time.sleep(2)
                    console.print("[green]✅ Microphone works![/green]\n")
                    inquirer.confirm(message="Continue?", default=True).execute()
                
                elif action == "settings":
                    self.show_settings_menu()
                
                elif action == "tutorial":
                    self.show_tutorial()
                
                elif action == "about":
                    self.show_about()
                
                elif action == "exit":
                    console.print("\n[cyan]Terima kasih telah menggunakan SlideSense.id![/cyan]")
                    console.print("[dim]See you next time! 👋[/dim]\n")
                    sys.exit(0)
        
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Program terminated by user[/yellow]")
            sys.exit(0)
        except Exception as e:
            self.show_error("unknown", str(e))
            sys.exit(1)


# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    menu = BeautifulMenu()
    menu.run()
