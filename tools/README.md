# Metadata Validation Tools

This directory contains tools for validating and managing episode metadata.

## Installation

```bash
bun install
```

## Scripts

- `bun run validate` - Check all episode metadata for validity
- `bun run validate:watch` - Watch for changes and validate continuously  
- `bun run lint` - Same as validate (alias)
- `bun run lint:fix` - Auto-fix missing metadata fields
- `bun run generate-readme` - Generate root README.md with episode table + RSS feed
- `bun run build` - Run lint:fix + generate-readme

## Metadata Schema

Each episode should have a `meta.md` file in its folder containing YAML frontmatter with required fields like `guid`, `title`, `description`, `eventDate`, etc. The validation script will automatically prefer `meta.md` over README.md frontmatter for metadata storage.

## Migration

If you have existing README.md files with frontmatter, use the migration script:

```bash
bun run move-metadata.ts
```

This project uses [Bun](https://bun.sh) as the JavaScript runtime.
