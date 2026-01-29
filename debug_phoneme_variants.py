"""
Debug phoneme variants to see what's causing the problem
"""

from phoneme_variants import PhonemeVariants


def show_variants(phrase):
    """Show what variants are generated"""
    print(f"\nOriginal: '{phrase}'")
    
    variants = PhonemeVariants.generate_variants(phrase)
    print(f"Phoneme variants ({len(variants)}):")
    for v in sorted(variants)[:10]:  # Show first 10
        print(f"  - '{v}'")
    if len(variants) > 10:
        print(f"  ... and {len(variants) - 10} more")
    
    regional = PhonemeVariants.add_regional_variants(phrase, region='mixed')
    print(f"Regional variants ({len(regional)}):")
    for r in sorted(regional)[:10]:
        print(f"  - '{r}'")
    if len(regional) > 10:
        print(f"  ... and {len(regional) - 10} more")


if __name__ == "__main__":
    phrases = [
        "next slide",
        "back slide",
        "slide",
        "slid",
    ]
    
    for phrase in phrases:
        show_variants(phrase)
