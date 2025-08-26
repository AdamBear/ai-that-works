.PHONY: print-context
print-context:
	@echo "=== CURRENT USER: $$USER ==="
	@echo "=== CURRENT DATE & TIME (PT): $$(TZ='America/Los_Angeles' date '+%Y-%m-%d %H:%M:%S %Z') ==="
	@echo ""
	@echo "=== COMPANY.MD ==="
	@cat ./COMPANY.md
	@echo ""
	@echo "=== RUNNING_INVESTOR_UPDATES.MD ==="
	@cat ./running_investor_updates.md
	@echo ""
	@echo "=== THOUGHTS DIRECTORY STRUCTURE ==="
	@find ./thoughts -name "*.md" -not -path "./real-examples/*" | head -20
	@echo ""
	@echo "=== TOOLS DIRECTORY STRUCTURE ==="
	@find ./tools -name "*.md" -not -path "./real-examples/*" | head -10
	@echo ""
	@echo "=== SOPS DIRECTORY STRUCTURE ==="
	@find ./sops -name "*.md" -not -path "./real-examples/*" | head -10

.PHONY: format
format:
	bunx prettier --write "**/*.md" --ignore-path .gitignore

.PHONY: fileperms
fileperms:
	chmod -R u+w .

.PHONY: print-index
print-index:
	@echo "Listing markdown files in current directory (excluding real-examples)..."
	@find . -name "*.md" -not -path "./real-examples/*" -not -path "./node_modules/*" -not -path "./.git/*" | sort
