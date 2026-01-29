"""
Debug specific failing test cases
"""

from voice_detector import SmartVoiceDetector
from fuzzywuzzy import fuzz


def debug_ambiguous_case(voice_input: str, expected: str):
    """Debug why a voice input gets wrong command"""
    
    detector = SmartVoiceDetector()
    detector.cooldown_seconds = 0
    
    print(f"\n{'='*70}")
    print(f"Analyzing: '{voice_input}' (expected: {expected})")
    print(f"{'='*70}\n")
    
    text_lower = voice_input.lower()
    input_words = set(text_lower.split())
    
    # Check word-level matching
    print(f"Input words: {input_words}\n")
    
    scores = {}
    
    for command, data in detector.wake_words.items():
        weight = data["weight"]
        phrases = data["phrases"]
        
        best_score = 0
        best_phrase = None
        
        for phrase in phrases:
            phrase_lower = phrase.lower()
            phrase_words = set(phrase_lower.split())
            
            # Exact match
            if phrase_lower == text_lower:
                score = weight + 20
                best_score = max(best_score, score)
                best_phrase = phrase if best_score == score else best_phrase
                continue
            
            # Contains
            if phrase_lower in text_lower or text_lower in phrase_lower:
                score = weight + 10
                best_score = max(best_score, score)
                best_phrase = phrase if best_score == score else best_phrase
                continue
            
            # Partial (2+ words match)
            matching_words = len(input_words & phrase_words)
            if matching_words >= 2:
                score = weight + (matching_words * 3)
                best_score = max(best_score, score)
                best_phrase = phrase if best_score == score else best_phrase
                continue
            
            # Fuzzy match
            ratio = fuzz.ratio(text_lower, phrase_lower)
            if ratio >= 85:
                score = weight + (ratio / 20)
                best_score = max(best_score, score)
                best_phrase = phrase if best_score == score else best_phrase
        
        if best_score > 0:
            scores[command] = (best_score, best_phrase)
    
    # Show sorted scores
    sorted_scores = sorted(scores.items(), key=lambda x: x[1][0], reverse=True)
    
    print("Command Scores (sorted):")
    for i, (cmd, (score, phrase)) in enumerate(sorted_scores[:5]):
        marker = " [WINNER]" if i == 0 else ""
        marker += " [EXPECTED]" if cmd == expected else ""
        print(f"  {i+1}. {cmd:20s}: {score:6.1f} (phrase: '{phrase}'){marker}")
    
    # Get actual result
    result = detector.detect(voice_input)
    print(f"\nActual result: {result['command']} (score: {result['score']:.1f})")
    
    # Analysis
    if result["command"] == expected:
        print("✓ CORRECT")
    else:
        print(f"✗ WRONG - Got {result['command']} instead of {expected}")
        
        # Suggest fix
        if expected in scores:
            expected_score, expected_phrase = scores[expected]
            winner_score, winner_phrase = scores[result["command"]]
            print(f"\n  Expected score: {expected_score:.1f}")
            print(f"  Winner score: {winner_score:.1f}")
            print(f"  Difference: {winner_score - expected_score:.1f}")
            
            # Find why expected lost
            print(f"\n  Issue: '{expected}' phrase '{expected_phrase}' scores lower than '{result['command']}'")
            print(f"  Potential fix: Strengthen matching for '{expected_phrase}'")


if __name__ == "__main__":
    failing_cases = [
        ("black slide", "previous"),
        ("preview slide", "previous"),
        ("opn slaid sho", "open_slideshow"),
        ("klos slaid sho", "close_slideshow"),
    ]
    
    for input_str, expected_cmd in failing_cases:
        debug_ambiguous_case(input_str, expected_cmd)
