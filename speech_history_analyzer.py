#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SPEECH_HISTORY_ANALYZER.py - Auto-Learning System

Menganalisis speech_history.txt untuk:
1. Mendeteksi perintah yang tidak dikenali
2. Mengelompokkan dengan perintah utama berdasarkan kesamaan
3. Menyarankan penambahan keyword baru
4. Membantu continuous improvement
"""

import os
import json
from typing import Dict, List, Tuple
from datetime import datetime
from constants import MAIN_COMMANDS, KEYWORDS_INDEX, get_command_by_keyword

class SpeechHistoryAnalyzer:
    def __init__(self, history_file: str = "speech_history.txt"):
        self.history_file = history_file
        self.unrecognized_commands = []
        self.grouped_commands = {}
        self.suggestions = {}
        
    def analyze(self):
        """Analisis seluruh speech history"""
        if not os.path.exists(self.history_file):
            print(f"⚠️  File {self.history_file} tidak ditemukan")
            return
        
        print(f"\n📊 Menganalisis {self.history_file}...\n")
        
        with open(self.history_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        total_commands = len(lines)
        recognized = 0
        unrecognized = 0
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Parse format: [timestamp] command -> result
            try:
                if "[RECOGNIZED]" in line:
                    recognized += 1
                elif "[UNRECOGNIZED]" in line or "[FAILED]" in line:
                    unrecognized += 1
                    # Extract command
                    parts = line.split(":")
                    if len(parts) > 1:
                        command = parts[1].strip()
                        self.unrecognized_commands.append(command)
            except:
                pass
        
        print(f"Total Commands: {total_commands}")
        print(f"Recognized: {recognized}")
        print(f"Unrecognized: {unrecognized}")
        print(f"Success Rate: {(recognized / total_commands * 100) if total_commands > 0 else 0:.1f}%\n")
        
        # Analyze unrecognized commands
        self.group_unrecognized_commands()
        
        return {
            "total": total_commands,
            "recognized": recognized,
            "unrecognized": unrecognized,
            "success_rate": (recognized / total_commands) if total_commands > 0 else 0
        }
    
    def group_unrecognized_commands(self):
        """Kelompokkan perintah tidak dikenali dengan perintah utama"""
        print(f"🔍 Mengelompokkan {len(self.unrecognized_commands)} perintah tidak dikenali...\n")
        
        for cmd_name in MAIN_COMMANDS.keys():
            self.grouped_commands[cmd_name] = []
        
        for unrecognized in self.unrecognized_commands:
            best_match, confidence = self._find_best_match(unrecognized)
            
            if best_match and confidence > 0.5:  # Confidence threshold
                self.grouped_commands[best_match].append({
                    "phrase": unrecognized,
                    "confidence": confidence
                })
                
                # Create suggestion
                if best_match not in self.suggestions:
                    self.suggestions[best_match] = []
                
                self.suggestions[best_match].append({
                    "phrase": unrecognized,
                    "confidence": confidence,
                    "timestamp": datetime.now().isoformat()
                })
        
        # Display grouped commands
        print("\n📋 GROUPED COMMANDS:\n")
        for cmd_name, phrases in self.grouped_commands.items():
            if phrases:
                print(f"→ {cmd_name.upper()} ({len(phrases)} suggestions)")
                for phrase_data in phrases[:3]:  # Show top 3
                    confidence = phrase_data['confidence']
                    print(f"  • '{phrase_data['phrase']}' (confidence: {confidence:.2f})")
                if len(phrases) > 3:
                    print(f"  ... and {len(phrases) - 3} more")
                print()
    
    def _find_best_match(self, unrecognized: str) -> Tuple[str, float]:
        """
        Cari perintah utama yang paling cocok dengan frasa tidak dikenali.
        Menggunakan similarity matching dengan phonetic comparison.
        """
        try:
            from fuzzywuzzy import fuzz
        except ImportError:
            # Simple fallback jika fuzzywuzzy tidak ada
            return self._simple_match(unrecognized)
        
        best_command = None
        best_score = 0
        
        unrecognized_lower = unrecognized.lower().strip()
        
        for cmd_name, cmd_data in MAIN_COMMANDS.items():
            # Check direct keyword match
            for keyword in cmd_data['keywords']:
                score = fuzz.ratio(unrecognized_lower, keyword.lower())
                if score > best_score:
                    best_score = score
                    best_command = cmd_name
            
            # Check partial match
            cmd_keywords_str = " ".join(cmd_data['keywords'])
            score = fuzz.token_set_ratio(unrecognized_lower, cmd_keywords_str)
            if score > best_score:
                best_score = score
                best_command = cmd_name
        
        # Normalize score to 0-1
        confidence = best_score / 100.0 if best_score > 0 else 0
        
        return best_command, confidence
    
    def _simple_match(self, unrecognized: str) -> Tuple[str, float]:
        """Simple string matching fallback"""
        best_command = None
        best_score = 0
        
        unrecognized_lower = unrecognized.lower()
        
        for cmd_name, cmd_data in MAIN_COMMANDS.items():
            for keyword in cmd_data['keywords']:
                # Check if keyword is in unrecognized phrase
                if keyword.lower() in unrecognized_lower:
                    score = len(keyword) / len(unrecognized_lower)  # Ratio
                    if score > best_score:
                        best_score = score
                        best_command = cmd_name
        
        return best_command, best_score
    
    def get_suggestions(self) -> Dict[str, List]:
        """Dapatkan saran untuk command baru"""
        return self.suggestions
    
    def export_suggestions(self, output_file: str = "suggestions.json"):
        """Export saran ke file JSON"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.suggestions, f, indent=2, ensure_ascii=False)
        
        print(f"\n✅ Suggestions exported to {output_file}")
    
    def print_summary(self):
        """Print ringkasan analisis"""
        print("\n" + "="*60)
        print("ANALYSIS SUMMARY")
        print("="*60)
        
        total_suggestions = sum(len(phrases) for phrases in self.suggestions.values())
        
        print(f"\nTotal Unrecognized Commands: {len(self.unrecognized_commands)}")
        print(f"Total Suggestions: {total_suggestions}")
        print(f"Commands with Suggestions: {len(self.suggestions)}")
        
        print(f"\nTOP COMMANDS BY SUGGESTIONS:")
        sorted_suggestions = sorted(
            self.suggestions.items(),
            key=lambda x: len(x[1]),
            reverse=True
        )
        
        for cmd_name, suggestions in sorted_suggestions[:5]:
            print(f"  • {cmd_name}: {len(suggestions)} suggestions")
        
        print("\n" + "="*60)

def analyze_and_report(history_file: str = "speech_history.txt"):
    """Convenience function untuk analisis dan report"""
    analyzer = SpeechHistoryAnalyzer(history_file)
    analyzer.analyze()
    analyzer.print_summary()
    analyzer.export_suggestions()
    
    return analyzer

if __name__ == "__main__":
    # Test jika dijalankan langsung
    analyzer = analyze_and_report()
    
    print("\n\nGROUPED COMMANDS DETAIL:")
    print(json.dumps(analyzer.suggestions, indent=2, ensure_ascii=False))
