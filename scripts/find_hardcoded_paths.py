"""List hard-coded Windows paths (e.g. G:\\nih_split.csv) in every notebook, so you can edit them.

Usage:  python scripts/find_hardcoded_paths.py [--replace G: D:/cxr]
Without --replace the script only reports. With --replace OLD NEW it rewrites the drive prefix in place.
"""
import argparse, glob, json, re, sys

PAT = re.compile(r"[A-Za-z]:\\")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replace", nargs=2, metavar=("OLD", "NEW"))
    a = ap.parse_args()
    total = 0
    for f in sorted(glob.glob("notebooks/*/*.ipynb")):
        nb = json.load(open(f, encoding="utf-8"))
        hits, changed = 0, False
        for c in nb["cells"]:
            if c["cell_type"] != "code":
                continue
            for i, line in enumerate(c["source"]):
                if PAT.search(line):
                    hits += 1
                    if a.replace:
                        c["source"][i] = line.replace(*a.replace)
                        changed = True
        if hits:
            print(f"{f}: {hits} line(s)")
            total += hits
        if changed:
            json.dump(nb, open(f, "w", encoding="utf-8"), indent=1, ensure_ascii=False)
    print(f"total lines with a drive path: {total}")

if __name__ == "__main__":
    sys.exit(main())
