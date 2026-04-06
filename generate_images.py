#!/usr/bin/env python3
"""Generate monster portrait and battle scene images using Pollinations.ai"""
import urllib.request
import urllib.parse
import os
import concurrent.futures
import time
import sys

IMG_DIR = os.path.join(os.path.dirname(__file__), 'images')
os.makedirs(IMG_DIR, exist_ok=True)

STYLE = "dark fantasy digital art, spooky childrens book illustration, dark atmospheric lighting, moody purple and red tones, highly detailed, square composition, no text no words no letters"

# === MONSTER PORTRAITS ===
PORTRAITS = {
    'giant-legs.png': f"a terrifying creature that is ONLY giant muscular purple legs with NO body NO head NO torso, just four enormous legs stomping through a dark haunted forest at night, dust clouds from stomping, {STYLE}",
    'terradaxoar.png': f"a dark flying monster called Terradaxoar soaring through a night sky, it has FIVE glowing orange eyes in a row across its wide flat head, dark blue-grey bat-like wings spread wide, sharp talons, menacing, {STYLE}",
    'slime-blob.png': f"a round spiky green slime monster with an evil grin and glowing red eyes, covered in sharp spikes, pieces of it floating nearby reconnecting with green energy lines showing it can regenerate and heal, dark forest background, {STYLE}",
}

# === BATTLE SCENES ===
BATTLES = {
    'battle-spider-belly.png': f"Spider Scope monster with a telescope eye fighting Belly Bonker monster with a belly button eye, the belly bonker blasting the spider scope with energy from its belly eye, dark forest battle scene, {STYLE}",
    'battle-spider-tree.png': f"a spider creature with a glowing scope/telescope firing a beam of light at a monstrous evil tree creature that is burning, dark forest battle, {STYLE}",
    'battle-spider-rock.png': f"a spider creature with a glowing purple telescope scope detecting an invisible rock creature that is partially visible as a shimmer outline, dark cave scene, {STYLE}",
    'battle-spider-giantlegs.png': f"a spider creature with a scope being stomped flat by enormous disembodied giant legs, dust clouds and destruction, dark forest, {STYLE}",
    'battle-spider-terradaxoar.png': f"a flying monster with five glowing eyes swooping down to attack a spider creature with a telescope, night sky battle, {STYLE}",
    'battle-spider-healbeast.png': f"a round spiky green slime blob reforming itself after being blasted to pieces by a spider with a scope, pieces reconnecting with green energy, dark forest, {STYLE}",
    'battle-belly-tree.png': f"a monster with a glowing belly button eye EXPLODING out of a monstrous tree creature from the inside, wood splinters and green slime flying everywhere, massive explosion, dark forest, {STYLE}",
    'battle-belly-rock.png': f"an invisible rock creature pushing a confused belly-eye monster off a dark cliff edge, the belly monster falling, dark atmospheric scene, {STYLE}",
    'battle-belly-giantlegs.png': f"a small round monster with a belly button eye rolling between enormous disembodied legs and attacking their weak spot with a glowing beam, the giant legs wobbling and falling, {STYLE}",
    'battle-belly-terradaxoar.png': f"a five-eyed flying monster dive-bombing and carrying away a round monster with a belly button eye, dramatic night sky action scene, {STYLE}",
    'battle-belly-healbeast.png': f"a monster with a glowing hot belly button eye burning green slime pieces before they can reconnect, green pieces disintegrating in orange fire, dark scene, {STYLE}",
    'battle-tree-rock.png': f"a monstrous evil tree creature swallowing an invisible shimmering rock creature whole, the tree mouth open wide chomping down, dark forest, {STYLE}",
    'battle-tree-giantlegs.png': f"enormous disembodied giant legs stomping right through a monstrous evil tree creature, smashing it to pieces without even noticing, wood flying everywhere, {STYLE}",
    'battle-tree-terradaxoar.png': f"a monstrous tree creature grabbing a five-eyed flying monster with its branches and pulling it down, the flying creature struggling, dark forest, {STYLE}",
    'battle-tree-healbeast.png': f"tree roots shooting from the ground wrapping around a round green slime blob monster and dragging it underground, green energy being absorbed by the roots, dark scene, {STYLE}",
    'battle-rock-giantlegs.png': f"enormous disembodied giant legs tripping over an invisible rock creature and crashing into a dark canyon, the legs falling dramatically, dust everywhere, {STYLE}",
    'battle-rock-terradaxoar.png': f"a five-eyed flying monster grabbing an invisible partially-visible rock creature with its talons, one special eye glowing brighter than the others to see the invisible creature, night sky, {STYLE}",
    'battle-rock-healbeast.png': f"an invisible shimmering rock creature pushing a round green slime blob monster into a glowing orange volcano, the slime monster falling into lava, dramatic scene, {STYLE}",
    'battle-giantlegs-terradaxoar.png': f"a five-eyed flying monster attacking enormous disembodied legs from above, diving and striking repeatedly while the legs kick uselessly at the sky, dramatic battle, {STYLE}",
    'battle-giantlegs-healbeast.png': f"enormous disembodied giant legs repeatedly stomping a round green slime blob flat, the slime trying to reform but getting stomped again and again, dark dramatic scene, {STYLE}",
    'battle-terradaxoar-healbeast.png': f"a five-eyed flying monster carrying green slime pieces in different directions over five different oceans, dropping the pieces far apart so they cannot heal back together, epic aerial scene, {STYLE}",
}

def download_image(name, prompt, retries=2):
    filepath = os.path.join(IMG_DIR, name)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"  SKIP {name} (already exists)")
        return True

    encoded = urllib.parse.quote(prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded}?width=512&height=512&nologo=true&seed={hash(name) % 100000}"

    for attempt in range(retries + 1):
        try:
            print(f"  GET  {name} (attempt {attempt+1})...")
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = resp.read()
                if len(data) < 5000:
                    print(f"  WARN {name}: response too small ({len(data)} bytes), retrying...")
                    time.sleep(5)
                    continue
                with open(filepath, 'wb') as f:
                    f.write(data)
                print(f"  DONE {name} ({len(data)} bytes)")
                time.sleep(2)  # Rate limit pause
                return True
        except Exception as e:
            print(f"  ERR  {name}: {e}")
            if attempt < retries:
                time.sleep(8)

    print(f"  FAIL {name}")
    return False

def main():
    all_images = {}

    if '--battles-only' not in sys.argv:
        print("=== GENERATING MONSTER PORTRAITS ===")
        all_images.update(PORTRAITS)

    if '--portraits-only' not in sys.argv:
        print("=== GENERATING BATTLE SCENES ===")
        all_images.update(BATTLES)

    print(f"Total images to generate: {len(all_images)}")

    # Sequential downloads to avoid rate limits
    results = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
        futures = {executor.submit(download_image, name, prompt): name for name, prompt in all_images.items()}
        for future in concurrent.futures.as_completed(futures):
            name = futures[future]
            try:
                results[name] = future.result()
            except Exception as e:
                print(f"  EXCEPTION {name}: {e}")
                results[name] = False

    succeeded = sum(1 for v in results.values() if v)
    failed = sum(1 for v in results.values() if not v)
    print(f"\n=== COMPLETE: {succeeded} succeeded, {failed} failed ===")

if __name__ == '__main__':
    main()
