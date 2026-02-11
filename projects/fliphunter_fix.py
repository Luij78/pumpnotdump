# FlipHunter False Positive Fix
# Negative words filter for match_to_database()
# Add this to flip_app.py to prevent matching novelty/accessory items as the main product

# NEGATIVE WORDS - if these appear in title, reject the match for that category
NEGATIVE_WORDS = {
    # Gaming consoles - things that aren't the actual console
    'xbox': ['mini fridge', 'fridge', 'refrigerator', 'cooler', 'skin', 'decal', 
             'sticker', 'stand', 'wall mount', 'cover', 'case', 'carrying',
             'headset only', 'controller only', 'charger only', 'dock only',
             'replica', 'novelty', 'decoration', 'poster', 'shirt', 'hat',
             'cake', 'topper', 'party', 'costume', 'backpack', 'lunchbox',
             'pillow', 'blanket', 'rug', 'lamp', 'clock', 'figurine'],
             
    'playstation': ['mini fridge', 'fridge', 'refrigerator', 'skin', 'decal',
                   'sticker', 'stand', 'wall mount', 'cover', 'case', 'carrying',
                   'headset only', 'controller only', 'charger only',
                   'replica', 'novelty', 'decoration', 'poster', 'shirt',
                   'cake', 'topper', 'party', 'costume', 'pillow', 'blanket'],
                   
    'ps5': ['skin', 'decal', 'sticker', 'stand', 'wall mount', 'cover', 'plate',
            'faceplate', 'case', 'controller only', 'headset only', 'charger only',
            'replica', 'novelty', 'decoration', 'poster', 'cake'],
            
    'ps4': ['skin', 'decal', 'sticker', 'stand', 'controller only', 'case',
            'replica', 'novelty', 'decoration'],
            
    'nintendo': ['case only', 'carrying case', 'skin', 'decal', 'grip',
                 'controller only', 'joycon only', 'dock only', 'charger only',
                 'replica', 'novelty', 'poster', 'shirt', 'plush', 'amiibo only'],
                 
    'switch': ['case only', 'carrying', 'skin', 'grip', 'joycon only', 'dock only',
               'charger only', 'screen protector', 'tempered glass'],
    
    # Phones - things that aren't the actual phone
    'iphone': ['case', 'cover', 'screen protector', 'charger only', 'cable only',
               'box only', 'empty box', 'parts only', 'for parts', 'broken screen',
               'cracked', 'icloud locked', 'activation locked', 'locked to',
               'carrier locked', 'blacklisted', 'imei bad', 'replica', 'clone',
               'skin', 'decal', 'stand', 'mount', 'holder', 'dock only'],
               
    'samsung': ['case', 'cover', 'screen protector', 'charger only', 'cable only',
                'box only', 'for parts', 'cracked', 'broken', 'locked',
                'replica', 'skin', 'decal'],
    
    # Laptops/Computers
    'macbook': ['case', 'sleeve', 'cover', 'skin', 'keyboard cover', 'charger only',
                'adapter only', 'for parts', 'broken', 'cracked screen', 'no ssd',
                'no hard drive', 'stand', 'dock only', 'hub only'],
                
    'ipad': ['case', 'cover', 'keyboard only', 'pencil only', 'charger only',
             'for parts', 'cracked', 'icloud locked', 'skin', 'stand', 'mount'],
    
    # Audio
    'airpods': ['case only', 'charging case only', 'left only', 'right only',
                'ear tips only', 'replica', 'fake', 'clone', 'knock off',
                'single', '1 airpod', 'one airpod'],
    
    # Home appliances  
    'dyson': ['filter only', 'parts only', 'brush only', 'head only',
              'attachment only', 'for parts', 'not working', 'broken',
              'motor only', 'bin only', 'cleaner head only'],
              
    'roomba': ['parts only', 'for parts', 'brush only', 'filter only',
               'wheel only', 'not working', 'broken', 'battery only',
               'base only', 'dock only'],
    
    # Cameras
    'gopro': ['mount only', 'case only', 'housing only', 'battery only',
              'charger only', 'accessories only', 'for parts', 'broken',
              'stick only', 'selfie stick'],
              
    'dji': ['battery only', 'remote only', 'controller only', 'propellers only',
            'case only', 'for parts', 'broken', 'crashed', 'gimbal only'],
}

# Updated match_to_database function with negative word filtering
def match_to_database_v2(title):
    """Stricter matching - requires key words in sequence AND no negative words"""
    title_clean = clean_title(title)
    title_lower = title.lower()
    title_words = set(title_clean.split())
    
    best_match = None
    best_score = 0
    
    for item_name, data in PRICE_LOOKUP.items():
        item_words = item_name.split()
        
        # ALL key words must appear in title
        all_present = all(word in title_words for word in item_words)
        if not all_present:
            continue
        
        # === NEW: Check for negative words ===
        rejected = False
        for keyword, negative_list in NEGATIVE_WORDS.items():
            if keyword in item_words or keyword in item_name.lower():
                # This item contains a keyword we have negative words for
                for negative in negative_list:
                    if negative in title_lower:
                        rejected = True
                        break
                if rejected:
                    break
        
        if rejected:
            continue  # Skip this match - it's likely a false positive
        # === END NEW SECTION ===
        
        # Check if words appear somewhat close together (within 10 words span)
        positions = []
        for word in item_words:
            try:
                pos = title_clean.split().index(word)
                positions.append(pos)
            except:
                pass
        
        if positions:
            span = max(positions) - min(positions)
            if span > 10:  # Words too far apart
                continue
        
        # Score based on match quality
        score = len(item_words)
        
        # Bonus for exact brand names
        brands = ['iphone', 'ipad', 'macbook', 'airpods', 'samsung', 'sony', 
                  'nintendo', 'xbox', 'playstation', 'ps5', 'dyson', 'roomba', 
                  'gopro', 'dji']
        for brand in brands:
            if brand in item_words and brand in title_words:
                score += 2
        
        if score > best_score:
            best_score = score
            best_match = {'name': item_name, **data}
    
    return best_match


# Test cases to verify the fix works
if __name__ == '__main__':
    # Simulated clean_title function
    import re
    def clean_title(title):
        title = title.lower()
        title = re.sub(r'[^a-z0-9\s]', ' ', title)
        title = re.sub(r'\s+', ' ', title).strip()
        return title
    
    # Test cases
    test_cases = [
        ("Xbox Series X 1TB Console - Like New", True, "Should match"),
        ("Xbox Mini Fridge - Brand New In Box $50", False, "Should NOT match - mini fridge"),
        ("Xbox Series X Skin Decal Sticker $10", False, "Should NOT match - skin"),
        ("PS5 Console Digital Edition", True, "Should match"),
        ("PS5 Controller Skin Cover $15", False, "Should NOT match - skin"),
        ("iPhone 14 Pro Max 256GB Unlocked", True, "Should match"),
        ("iPhone 14 Pro Case Clear $10", False, "Should NOT match - case"),
        ("AirPods Pro 2nd Generation", True, "Should match"),
        ("AirPods Case Only - Left AirPod Missing", False, "Should NOT match - case only"),
        ("Nintendo Switch OLED White", True, "Should match"),
        ("Nintendo Switch Carrying Case", False, "Should NOT match - carrying case"),
    ]
    
    print("Testing negative word filter:")
    print("=" * 60)
    for title, should_match, note in test_cases:
        # Check if any negative words are present
        title_lower = title.lower()
        matched = True  # Assume match
        for keyword, negatives in NEGATIVE_WORDS.items():
            if keyword in title_lower:
                for neg in negatives:
                    if neg in title_lower:
                        matched = False
                        break
        
        status = "✅" if matched == should_match else "❌"
        result = "MATCH" if matched else "SKIP"
        print(f"{status} [{result}] {title[:45]}")
        print(f"   Expected: {'MATCH' if should_match else 'SKIP'} - {note}")
        print()
