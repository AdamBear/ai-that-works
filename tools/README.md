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
- `bun run generate-readme` - Generate root README.md with episode table + RSS feed + data.json
- `bun run build` - Run lint:fix + generate-readme

## Metadata Schema

Each episode should have a `meta.md` file in its folder containing YAML frontmatter with required fields like `guid`, `title`, `description`, `eventDate`, etc. The validation script will automatically prefer `meta.md` over README.md frontmatter for metadata storage.

## Migration

If you have existing README.md files with frontmatter, use the migration script:

```bash
bun run move-metadata.ts
```

## Generated Files

The `--generate-readme` command produces three files:

1. **README.md** - Main project README with episode table and CTA
2. **feed.xml** - RSS 2.0 feed for completed episodes with YouTube links
3. **data.json** - Structured JSON data with all episode metadata

### data.json Structure

```json
{
  "episodes": [
    {
      "folder": "2025-XX-XX-episode-name",
      "guid": "aitw-XXX",
      "title": "Episode Title",
      "description": "Episode description...",
      "eventDate": "2025-XX-XXTXX:XX:XXZ",
      "season": 2,
      "episode": 15,
      "isPast": true,
      "isWorkshop": false,
      "links": { ... },
      "media": { ... }
    }
  ],
  "meta": {
    "totalEpisodes": 23,
    "completedEpisodes": 20,
    "upcomingEpisodes": 1,
    "workshops": 2,
    "seasons": [1, 2],
    "lastUpdated": "2025-XX-XXTXX:XX:XX.XXXZ",
    "generatedBy": "validate-metadata.ts"
  }
}
```

This project uses [Bun](https://bun.sh) as the JavaScript runtime.
