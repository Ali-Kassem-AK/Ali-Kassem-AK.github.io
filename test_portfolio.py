import os
import re
import json
import subprocess
import sys
import xml.etree.ElementTree as ET

class PortfolioTest:
    def __init__(self, root_dir):
        self.root = root_dir
        self.index_path = os.path.join(root_dir, 'index.html')
        self.css_path = os.path.join(root_dir, 'style.css')
        self.input_css_path = os.path.join(root_dir, 'input.css')
        self.scm_svg_path = os.path.join(root_dir, 'images', 'scm-sim.svg')
        self.failures = []
        self.passes = []

    def assert_true(self, condition, message):
        if condition:
            self.passes.append(message)
            print(f"  [PASS] {message}")
        else:
            self.failures.append(message)
            print(f"  [FAIL] {message}")

    def run_all(self):
        print("=== RUNNING PORTFOLIO VERIFICATION SUITE ===")
        self.test_files_exist()
        self.test_html_content()
        self.test_json_ld()
        self.test_anchor_links()
        self.test_asset_references()
        self.test_content_rules()
        self.test_translations_consistency()
        self.test_accessibility()
        self.test_prerendered_seo_content()
        self.test_sitemap_xml()
        self.test_css_build()
        
        print("\n=== TEST SUMMARY ===")
        print(f"Passed: {len(self.passes)}")
        print(f"Failed: {len(self.failures)}")
        if self.failures:
            print("\nFailures:")
            for f in self.failures:
                print(f"  - {f}")
            return False
        return True

    def test_files_exist(self):
        print("\n--- 1. File Existence Checks ---")
        expected_files = [
            'index.html', 'input.css', 'style.css', 'tailwind.config.js',
            'package.json', 'Ali_Ahmed_Kassem_Resume_Data_AI_Engineer.pdf',
            'robots.txt', 'sitemap.xml'
        ]
        for f in expected_files:
            path = os.path.join(self.root, f)
            self.assert_true(os.path.exists(path) and os.path.getsize(path) > 0, f"File {f} exists and is non-empty")
        
        for img in ['images/xare-v2.png', 'images/scm-sim.svg']:
            path = os.path.join(self.root, img)
            self.assert_true(os.path.exists(path) and os.path.getsize(path) > 0, f"Asset {img} exists and is non-empty")

    def test_html_content(self):
        print("\n--- 2. HTML Structure & Metadata Checks ---")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assert_true('<!DOCTYPE html>' in content, "HTML5 Doctype present")
        self.assert_true('<title>Ali Kassem' in content, "Page title contains 'Ali Kassem'")
        self.assert_true('<meta name="description"' in content, "Meta description tag present")
        self.assert_true('<link rel="canonical"' in content, "Canonical link tag present")
        self.assert_true('<meta property="og:title"' in content, "OpenGraph title present")
        self.assert_true('<meta property="og:image"' in content, "OpenGraph image present")
        self.assert_true('<meta name="twitter:card"' in content, "Twitter card meta present")
        self.assert_true('class="skip-link"' in content, "Accessible skip-link present")
        self.assert_true('<noscript>' in content and '.reveal-element' in content, "Progressive enhancement noscript fallback present")

    def test_json_ld(self):
        print("\n--- 3. Structured Data (JSON-LD) Validation ---")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        match = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        self.assert_true(match is not None, "JSON-LD script block found")
        if match:
            try:
                data = json.loads(match.group(1))
                self.assert_true(data.get("@type") == "Person", "Schema type is Person")
                self.assert_true(data.get("name") == "Ali Kassem", "Person name is Ali Kassem")
                self.assert_true("E-JUST" in data.get("alumniOf", {}).get("name", ""), "AlumniOf mentions E-JUST")
                self.assert_true("E-JUST" in data.get("affiliation", {}).get("name", ""), "Affiliation mentions E-JUST")
                self.assert_true(len(data.get("sameAs", [])) >= 2, "LinkedIn and GitHub profiles linked in sameAs")
            except Exception as e:
                self.assert_true(False, f"JSON-LD valid JSON: {str(e)}")

    def test_anchor_links(self):
        print("\n--- 4. Anchor Link Integrity ---")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        hrefs = set(re.findall(r'href="#([a-zA-Z0-9_\-]+)"', content))
        ids = set(re.findall(r'id="([a-zA-Z0-9_\-]+)"', content))

        for target in hrefs:
            self.assert_true(target in ids, f"Internal link target #{target} has corresponding id")

    def test_asset_references(self):
        print("\n--- 5. Referenced Asset Verification ---")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        imgs = re.findall(r'src="([^"]+)"', content)
        for img in imgs:
            if not img.startswith('http') and not img.startswith('data:') and not img.startswith('${'):
                path = os.path.join(self.root, img)
                self.assert_true(os.path.exists(path), f"Image src '{img}' exists on disk")

        js_imgs = re.findall(r'imageUrl:\s*"([^"]+)"', content)
        for img in js_imgs:
            path = os.path.join(self.root, img)
            self.assert_true(os.path.exists(path), f"JS project imageUrl '{img}' exists on disk")

        downloads = re.findall(r'download="([^"]+)"', content)
        for dl in downloads:
            path = os.path.join(self.root, dl)
            self.assert_true(os.path.exists(path), f"Download target '{dl}' exists on disk")

    def test_content_rules(self):
        print("\n--- 6. Content Rules & Quality Gates ---")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(self.scm_svg_path, 'r', encoding='utf-8') as f:
            svg_content = f.read()

        self.assert_true("High School Diploma" not in content, "High School Diploma removed from portfolio")
        self.assert_true("Victoria College" not in content, "Victoria College removed from portfolio")
        self.assert_true("SQL, MySQL, TypeScript" not in content, "MySQL not categorized as programming language")
        self.assert_true("Japanese (Basics)" not in content, "'Basics' typo removed for Japanese")
        self.assert_true("E-JUST" in content, "E-JUST used in content")
        self.assert_true("EJUST |" not in content, "Inconsistent 'EJUST |' without hyphen removed")
        self.assert_true("Ali_Ahmed_Kassem_Resume_Data_AI_Engineer.pdf" in content, "Resume link points to verified PDF")

        # Rigorous check: no unverified Supabase claim (resume states Firebase)
        self.assert_true("Supabase" not in content, "Hallucinated 'Supabase' removed; verified 'Firebase' retained")
        self.assert_true("120-Node n8n Cluster" not in content, "'Cluster' exaggeration avoided; accurate 'Workflow' description used")

        # Rigorous check: no fabricated performance metrics (60 FPS) in SVG
        self.assert_true("60 FPS" not in svg_content, "Fabricated '60 FPS' metric removed from SCM architecture SVG")
        self.assert_true("v1.2 ACTIVE" not in svg_content, "Invented release version removed from SCM architecture SVG")

    def test_translations_consistency(self):
        print("\n--- 7. Multilingual Translations Integrity ---")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        match_trans = re.search(r'const translations\s*=\s*\{\s*en:\s*\{(.*?)\n\s*\},.*?ar:\s*\{(.*?)\n\s*\},.*?ja:\s*\{(.*?)\n\s*\}', content, re.DOTALL)
        self.assert_true(match_trans is not None, "Translations database defined with en, ar, ja")

        if match_trans:
            en_keys = set(re.findall(r'([a-zA-Z0-9_]+)\s*:', match_trans.group(1)))
            ar_keys = set(re.findall(r'([a-zA-Z0-9_]+)\s*:', match_trans.group(2)))
            ja_keys = set(re.findall(r'([a-zA-Z0-9_]+)\s*:', match_trans.group(3)))

            diff_ar = en_keys - ar_keys
            diff_ja = en_keys - ja_keys
            self.assert_true(len(diff_ar) == 0, f"All English keys translated in Arabic (missing: {diff_ar})")
            self.assert_true(len(diff_ja) == 0, f"All English keys translated in Japanese (missing: {diff_ja})")

            # Check that language names are translated
            for lk in ['lang_ar_name', 'lang_en_name', 'lang_ja_name']:
                self.assert_true(lk in en_keys, f"Language key '{lk}' present in translation matrix")


    def test_accessibility(self):
        print("\n--- 8. Accessibility & Semantics ---")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        with open(self.input_css_path, 'r', encoding='utf-8') as f:
            css_content = f.read()

        h1_matches = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
        self.assert_true(len(h1_matches) == 1, f"Exactly one <h1> tag found (found {len(h1_matches)})")

        self.assert_true('role="dialog"' in content, "Modal dialog has role='dialog'")
        self.assert_true('aria-modal="true"' in content, "Modal dialog has aria-modal='true'")
        self.assert_true('aria-haspopup="dialog"' in content, "Project details buttons declare aria-haspopup='dialog'")
        self.assert_true('aria-label=' in content, "Interactive elements contain aria-label attributes")
        self.assert_true('id="contact-form"' in content, "Accessible contact form exists")
        self.assert_true('aria-required="true"' in content, "Contact form fields declare aria-required")
        self.assert_true('prefers-reduced-motion' in css_content, "Reduced motion considerations present in CSS")

    def test_prerendered_seo_content(self):
        print("\n--- 9. Static Pre-rendered Content Checks (SEO & Progressive Enhancement) ---")
        with open(self.index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Check projects container is not empty
        proj_match = re.search(r'<div class="grid grid-cols-1 md:grid-cols-2 gap-8" id="projects-container">(.*?)</div>\s*</div>\s*</section>', content, re.DOTALL)
        self.assert_true(proj_match is not None and '<article' in proj_match.group(1), "Projects container has pre-rendered semantic <article> cards")
        self.assert_true("Xare AI Platform" in content, "Static HTML contains Xare AI project text")
        self.assert_true("Supply Chain Management Simulation" in content, "Static HTML contains SCM Simulation project text")

        # Check experience container has timeline classes and pre-rendered items
        self.assert_true("timeline-item" in content and "timeline-node" in content, "Experience timeline has RTL-compatible timeline classes")
        self.assert_true("Digital Egypt Pioneers Initiative (DEPI)" in content, "Static HTML contains DEPI experience text")

        # Check education & certifications pre-rendered
        self.assert_true("Bachelor of Computer Science" in content, "Static HTML contains Degree text")
        self.assert_true("AI for You: Training and Assessment" in content, "Static HTML contains Oracle certification text")

    def test_sitemap_xml(self):
        print("\n--- 10. Sitemap & Robots SEO Verification ---")
        sitemap_path = os.path.join(self.root, 'sitemap.xml')
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            self.assert_true('urlset' in root.tag, "sitemap.xml is valid XML with urlset root")
        except Exception as e:
            self.assert_true(False, f"sitemap.xml valid XML: {str(e)}")

        robots_path = os.path.join(self.root, 'robots.txt')
        with open(robots_path, 'r', encoding='utf-8') as f:
            robots_content = f.read()
        self.assert_true("Sitemap:" in robots_content and "User-agent:" in robots_content, "robots.txt declares Sitemap and User-agent")

    def test_css_build(self):
        print("\n--- 11. Production CSS Build Check ---")
        result = subprocess.run(
            ['npx.cmd', 'tailwindcss@3.4.17', '-i', './input.css', '-o', './style.css', '--minify'],
            cwd=self.root,
            capture_output=True,
            text=True,
            shell=True
        )
        self.assert_true(result.returncode == 0, "Tailwind CSS CLI build completed with code 0")

if __name__ == '__main__':
    tester = PortfolioTest(os.path.dirname(os.path.abspath(__file__)))
    success = tester.run_all()
    sys.exit(0 if success else 1)
