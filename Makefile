PYTHON ?= python3
NODE ?= node
OUT_DIR ?= /tmp/polished-resume-demo

.PHONY: test demo demo-json demo-html demo-pdf clean

test:
	$(PYTHON) -m unittest discover -s tests -v

demo-json:
	mkdir -p $(OUT_DIR)
	$(PYTHON) scripts/intake_to_json.py references/intake-template.md $(OUT_DIR)/resume.json

demo-html:
	mkdir -p $(OUT_DIR)
	$(PYTHON) scripts/render_resume.py assets/sample_resume.json $(OUT_DIR)/resume.html

demo-pdf: demo-html
	$(NODE) scripts/export_pdf.js $(OUT_DIR)/resume.html $(OUT_DIR)/resume.pdf

demo: demo-html demo-pdf
	@printf "HTML: %s\nPDF: %s\n" "$(OUT_DIR)/resume.html" "$(OUT_DIR)/resume.pdf"

clean:
	rm -rf $(OUT_DIR)
