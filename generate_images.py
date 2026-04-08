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
    'giant-legs.png': f"exactly five enormous muscular purple monster legs growing out of the ground in a circle with NO body NO head NO torso NO face attached, just five disembodied legs standing in a dark haunted forest, each leg is thick and purple with clawed feet, dust clouds from stomping, the legs have no connection at the top just five separate legs, {STYLE}",
    'terradaxoar.png': f"a dark flying monster called Terradaxoar soaring through a night sky, it has exactly FIVE glowing orange eyes arranged in a horizontal row across its wide flat head like a row of five headlights, dark blue-grey bat-like wings spread wide, sharp talons, and a long whip-like tail crackling with blue-white electricity and lightning bolts, menacing, {STYLE}",
    'slime-blob.png': f"a round spiky green slime monster with an evil grin and glowing red eyes, covered in sharp spikes, pieces of it floating nearby reconnecting with green energy lines showing it can regenerate and heal, dark forest background, {STYLE}",
}

# === BATTLE SCENES ===
BATTLES = {
    'battle-spider-belly.png': f"Spider Scope monster with a telescope eye fighting Belly Bonker monster with a belly button eye, the belly bonker blasting the spider scope with energy from its belly eye, dark forest battle scene, {STYLE}",
    'battle-spider-tree.png': f"a spider creature with a glowing scope/telescope firing a beam of light at a monstrous evil tree creature that is burning, dark forest battle, {STYLE}",
    'battle-spider-rock.png': f"a spider creature with a glowing purple telescope scope detecting an invisible rock creature that is partially visible as a shimmer outline, dark cave scene, {STYLE}",
    'battle-spider-giantlegs.png': f"a spider creature with a scope being stomped flat by enormous disembodied giant legs, dust clouds and destruction, dark forest, {STYLE}",
    'battle-spider-terradaxoar.png': f"a dark flying monster with exactly FIVE glowing orange eyes in a row across its flat head and an electric lightning tail swooping down to attack a spider creature with a telescope, night sky battle, {STYLE}",
    'battle-spider-healbeast.png': f"a round spiky green slime blob reforming itself after being blasted to pieces by a spider with a scope, pieces reconnecting with green energy, dark forest, {STYLE}",
    'battle-belly-tree.png': f"a monster with a glowing belly button eye EXPLODING out of a monstrous tree creature that has THREE horrible mouths stacked vertically from the inside, wood splinters and green slime flying everywhere, massive explosion, dark forest, {STYLE}",
    'battle-belly-rock.png': f"an invisible rock creature pushing a confused belly-eye monster off a dark cliff edge, the belly monster falling, dark atmospheric scene, {STYLE}",
    'battle-belly-giantlegs.png': f"a small round monster with a belly button eye rolling between enormous disembodied legs and attacking their weak spot with a glowing beam, the giant legs wobbling and falling, {STYLE}",
    'battle-belly-terradaxoar.png': f"a dark flying monster with exactly FIVE glowing orange eyes in a horizontal row across its flat head and an electric lightning tail dive-bombing and carrying away a round furry monster with a glowing green belly button eye, dramatic night sky action scene, {STYLE}",
    'battle-belly-healbeast.png': f"a monster with a glowing hot belly button eye burning green slime pieces before they can reconnect, green pieces disintegrating in orange fire, dark scene, {STYLE}",
    'battle-tree-rock.png': f"a monstrous evil tree creature with THREE mouths stacked vertically swallowing an invisible shimmering rock creature whole, the biggest mouth open wide chomping down, dark forest, {STYLE}",
    'battle-tree-giantlegs.png': f"enormous disembodied giant legs stomping right through a monstrous evil tree creature with THREE mouths stacked vertically, smashing it to pieces without even noticing, wood flying everywhere, {STYLE}",
    'battle-tree-terradaxoar.png': f"a monstrous tree creature with THREE mouths grabbing a dark flying monster that has exactly FIVE glowing orange eyes in a row and an electric lightning tail with its branches and pulling it down, the flying creature struggling, dark forest, {STYLE}",
    'battle-tree-healbeast.png': f"a monstrous tree creature with THREE mouths stacked vertically shooting roots from the ground wrapping around a round green slime blob monster and dragging it underground, green energy being absorbed by the roots, dark scene, {STYLE}",
    'battle-rock-giantlegs.png': f"enormous disembodied giant legs tripping over an invisible rock creature and crashing into a dark canyon, the legs falling dramatically, dust everywhere, {STYLE}",
    'battle-rock-terradaxoar.png': f"a dark flying monster with exactly FIVE glowing orange eyes in a horizontal row across its flat head and an electric lightning tail grabbing an invisible partially-visible rock creature with its talons, one special eye glowing brighter than the others to see the invisible creature, night sky, {STYLE}",
    'battle-rock-healbeast.png': f"an invisible shimmering rock creature pushing a round green slime blob monster into a glowing orange volcano, the slime monster falling into lava, dramatic scene, {STYLE}",
    'battle-giantlegs-terradaxoar.png': f"a dark flying monster with exactly FIVE glowing orange eyes in a row across its flat head and an electric lightning tail attacking enormous disembodied legs from above, diving and striking repeatedly while the legs kick uselessly at the sky, dramatic battle, {STYLE}",
    'battle-giantlegs-healbeast.png': f"enormous disembodied giant legs repeatedly stomping a round green slime blob flat, the slime trying to reform but getting stomped again and again, dark dramatic scene, {STYLE}",
    'battle-terradaxoar-healbeast.png': f"a dark flying monster with exactly FIVE glowing orange eyes in a row across its flat head and an electric lightning tail carrying green slime pieces in different directions over five different oceans, dropping the pieces far apart so they cannot heal back together, epic aerial scene, {STYLE}",
}

# === PART ONE STORY SCENES (regen candidates) ===
STORY_SCENES = {
    'belly-bonker-attacks.png': f"a huge dark purple shaggy furry monster with a bright glowing GREEN eye in its belly attacking a small purple spider creature with a telescope scope bolted to its head, the belly eye glowing bright green, the furry monster swinging massive claws at the spider in a dark forest, {STYLE}",
    'tree-eats-belly.png': f"a monstrous tree creature with THREE mouths stacked vertically on its trunk opening all three mouths wide and swallowing a large dark purple shaggy furry monster with a glowing green belly eye, the furry monster being pulled into the tree, dark forest scene, {STYLE}",
    'belly-explodes-tree.png': f"a large dark purple shaggy furry monster with a bright glowing green belly eye BLASTING out through the trunk of a monstrous tree creature, the tree cracking open with green slime and wood flying everywhere, the furry monster emerging from inside the tree trunk, explosive dark forest scene, {STYLE}",
    'dead-tree.png': f"a monstrous tree creature with three mouths lying on the ground cracked and damaged but still ALIVE, its eyes still open and glowing faintly green, green sap oozing from cracks in its trunk as it slowly heals, dark moody forest floor scene, {STYLE}",
    'zombie-vs-all.png': f"monstrous tree creatures with glowing eyes and mouths full of teeth charging at a giant zombie, the trees fighting the zombie with whipping branches while a small purple spider with a telescope scope watches from behind a rock, epic dark forest battle, {STYLE}",
}

# === PART TWO STORY SCENES ===
PART_TWO = {
    'p2-villains-hunt.png': f"three distinct monsters prowling through a dark forest at night: a round spiky GREEN SLIME BLOB with red eyes and spikes, a dark bat-winged flying creature with glowing orange eyes and blue lightning crackling from its tail in the sky above, and five enormous disembodied purple legs with NO body stomping on the ground, all three hunting together, {STYLE}",
    'p2-too-many-trees.png': f"hundreds of monstrous evil tree creatures with glowing eyes and mouths full of teeth filling an entire dark forest, three small monsters looking overwhelmed and surrounded, {STYLE}",
    'p2-eat-sleepy-tree.png': f"three monsters attacking a single sleepy monstrous tree creature, a slime blob a flying bat creature and giant legs all jumping on the tree and tearing it apart, wood flying everywhere, dark forest, {STYLE}",
    'p2-too-full-explode.png': f"three distinct monsters about to EXPLODE from eating too much in a destroyed forest full of wood debris: a bloated round GREEN SLIME BLOB with red eyes swollen huge, a dark bat-winged creature with lightning tail too heavy to fly lying on the ground bloated, and five enormous purple disembodied legs wobbling and about to collapse, all three about to burst, {STYLE}",
    'p2-belly-returns.png': f"a dark furry monster with a glowing green belly button eye crawling out of a crack in the ground, a giant zombie stomping nearby eating monster remains, dark dramatic scene, {STYLE}",
    'p2-five-legs.png': f"five enormous muscular purple monster legs with NO body NO head NO face NO torso bursting out of the belly of a giant rotting green zombie, the five disembodied legs kicking through the zombie stomach, purple energy glowing, debris and zombie guts flying, dramatic dark scene, {STYLE}",
    'p2-ten-zombies.png': f"TEN giant zombies crawling out of cracks in the ground simultaneously, rotting green flesh and glowing red eyes, the ground splitting open in ten places, apocalyptic dark scene, {STYLE}",
    'p2-zombies-belly-friends.png': f"ELEVEN giant rotting green zombies with glowing red eyes standing in a group looking down fondly at a dark purple shaggy furry monster with a bright glowing GREEN EYE in its belly, they are friends not fighting, peaceful moment in a dark forest clearing, the furry belly-eye monster is much smaller than the zombies, {STYLE}",
    'p2-biggest-tree.png': f"the BIGGEST most enormous monstrous tree creature ever seen towering over an entire forest, taller than a skyscraper, with dozens of mouths full of teeth and glowing eyes all over its trunk, roots as thick as cars, eleven tiny zombies charging at its base, epic scale dark fantasy scene, {STYLE}",
    'p2-zombies-feast.png': f"eleven giant zombies tearing apart an enormous monstrous tree creature from every side, ripping branches and eating wood, green slime and wood debris everywhere, epic dark fantasy battle feast scene, {STYLE}",
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

    print("=== GENERATING STORY SCENES ===")
    all_images.update(STORY_SCENES)

    print("=== GENERATING PART TWO SCENES ===")
    all_images.update(PART_TWO)

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
