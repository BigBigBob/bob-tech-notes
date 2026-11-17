"""Build all locale variants and assemble the GitHub Pages artifact."""

import gzip
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / ".build"
PREVIEW = BUILD / "preview"
SITE_NAME = "bob-tech-notes"
PROJECTS = (
    ("zensical.toml", "zh-hans"),
    ("zensical.en.toml", "en"),
    ("zensical.zh-hant.toml", "zh-hant"),
)
SITEMAP_NS = "http://www.sitemaps.org/schemas/sitemap/0.9"


def merge_sitemaps(builds: list[Path], target: Path) -> None:
    ET.register_namespace("", SITEMAP_NS)
    urlset = ET.Element(f"{{{SITEMAP_NS}}}urlset")
    seen = set()

    for build in builds:
        source = build / "sitemap.xml"
        for entry in ET.parse(source).getroot():
            address = entry.findtext(f"{{{SITEMAP_NS}}}loc")
            if not address or address in seen:
                raise ValueError(f"Missing or duplicate URL in {source}: {address!r}")
            seen.add(address)
            urlset.append(entry)

    if not seen:
        raise ValueError("The locale builds produced an empty sitemap")

    ET.indent(urlset)
    output = ET.tostring(urlset, encoding="utf-8", xml_declaration=True) + b"\n"
    (target / "sitemap.xml").write_bytes(output)
    (target / "sitemap.xml.gz").write_bytes(gzip.compress(output, mtime=0))


def main() -> None:
    BUILD.mkdir(exist_ok=True)
    if BUILD.resolve() != BUILD:
        raise RuntimeError(f"Build directory must be inside the checkout: {BUILD}")

    builds = []
    for config, locale in PROJECTS:
        output = BUILD / locale
        if output.resolve() != output:
            raise RuntimeError(f"Invalid locale output directory: {output}")
        if output.exists():
            shutil.rmtree(output)
        subprocess.run(
            ["zensical", "build", "--config-file", config, "--clean", "--strict"],
            cwd=ROOT,
            check=True,
        )
        builds.append(output)

    PREVIEW.mkdir(exist_ok=True)
    if PREVIEW.resolve() != PREVIEW:
        raise RuntimeError(f"Invalid preview directory: {PREVIEW}")
    with TemporaryDirectory(prefix="assemble-", dir=BUILD) as work:
        stage = Path(work)
        target = stage / SITE_NAME
        shutil.copytree(builds[0], target)
        for build in builds[1:]:
            shutil.copytree(build, target / build.name)
        merge_sitemaps(builds, target)

        published = PREVIEW / SITE_NAME
        if published.resolve() != published:
            raise RuntimeError(f"Invalid site output directory: {published}")
        previous = stage / "previous"
        if published.exists():
            published.rename(previous)
        try:
            target.rename(published)
        except OSError:
            if previous.exists():
                previous.rename(published)
            raise

    print(f"Site built at {published}")


if __name__ == "__main__":
    main()
