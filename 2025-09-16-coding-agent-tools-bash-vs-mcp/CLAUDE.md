## installing packages


- use `bun install` to install packages
- never use `npm install` or `yarn install` or `pnpm install`
- never use a version string


# using linear

fetch an issue

bun run linear-cli/linear-cli.ts get-issue ENG-1709

fetch with comments

bun run linear-cli/linear-cli.ts get-issue ENG-1709 --comments
