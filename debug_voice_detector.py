"""
Debug script for voice detector fuzzy matching
Traces exact matching scores to identify the bug
"""

from voice_detector import SmartVoiceDetector
from fuzzywuzzy import fuzz


def debug_matching(voice_input: str):
    """Debug matching process for a voice input"""
    
    detector = SmartVoiceDetector()
    detector.cooldown_seconds = 0
    
    print(f"\n{'='*70}")
    print(f"DEBUG: Matching input: '{voice_input}'")
    print(f"{'='*70}")
    
    text_lower = voice_input.lower()
    input_words = text_lower.split()
    
    print(f"\nInput words: {input_words}")
    print(f"Input word count: {len(input_words)}")
    
    # Manually compute scores for each command
    scores = {}
    
    for command, data in detector.wake_words.items():
        weight = data["weight"]
        phrases = data["phrases"]
        
        print(f"\n--- Command: {command} (weight: {weight}) ---")
        
        best_score = 0
        best_phrase = None
        
        for phrase in phrases:
            phrase_lower = phrase.lower()
            phrase_words = phrase_lower.split()
            
            # 1. EXACT MATCH
            if phrase_lower == text_lower:
                score = weight + 20
                print(f"  ✓ EXACT: '{phrase}' → {score}")
                if score > best_score:
                    best_score = score
                    best_phrase = phrase
                continue
            
            # 2. PHRASE CONTAINS
            if phrase_lower in text_lower or text_lower in phrase_lower:
                score = weight + 10
                print(f"  ✓ CONTAINS: '{phrase}' → {score}")
                if score > best_score:
                    best_score = score
                    best_phrase = phrase
                continue
            
            # 3. PARTIAL MATCH (2+ words match)
            matching_words = sum(1 for word in phrase_words if word in input_words)
            if matching_words >= 2:
                score = weight + (matching_words * 3)
                print(f"  ✓ PARTIAL: '{phrase}' ({matching_words} words) → {score}")
                if score > best_score:
                    best_score = score
                    best_phrase = phrase
                continue
            
            # 4. FUZZY MATCH
            ratio = fuzz.ratio(text_lower, phrase_lower)
            if ratio >= 85:
                score = weight + (ratio / 20)
                print(f"  ✓ FUZZY: '{phrase}' (ratio: {ratio}%) → {score:.1f}")
                if score > best_score:
                    best_score = score
                    best_phrase = phrase
                continue
            
            # No match
            if best_score == 0:
                print(f"  ✗ NOMATCH: '{phrase}' (fuzzy: {ratio}%)")
        
        if best_score > 0:
            scores[command] = {
                "score": best_score,
                "phrase": best_phrase
            }
            print(f"  → Best for this command: {best_score} (phrase: '{best_phrase}')")
        else:
            scores[command] = {"score": 0, "phrase": None}
            print(f"  → No matching phrases for this command")
    
    # Find winner
    print(f"\n{'='*70}")
    print("SCORING SUMMARY:")
    print(f"{'='*70}")
    
    for cmd in sorted(scores.keys(), key=lambda x: scores[x]["score"], reverse=True):
        data = scores[cmd]
        print(f"  {cmd:20s}: {data['score']:6.1f}  (phrase: '{data['phrase']}')")
    
    # Get actual result from detector
    actual_result = detector.detect(voice_input)
    print(f"\n{'='*70}")
    print(f"ACTUAL RESULT: {actual_result['command']} (score: {actual_result['score']:.1f})")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    # Debug the failing test cases
    failing_cases = [
        "black slide",
        "preview slide",
        "opn slaid sho",
        "klos slaid sho",
    ]
    
    print("\n" + "="*70)
    print("DEBUGGING FUZZY MATCHING FAILURES")
    print("="*70)
    
    for case in failing_cases:
        debug_matching(case)
    
    # Also debug some passing cases
    print("\n" + "="*70)
    print("DEBUGGING PASSING CASES (for comparison)")
    print("="*70)
    
    passing_cases = [
        "next slide",
        "back slide",
        "open slide show",
        "close slide show",
    ]
    
    for case in passing_cases:
        debug_matching(case)
