# Ticket Management Tool — Project Context

## Goal
A monitor for Fatsoma events (mainly Ministry of Sound "Milkshake" student nights in London).
It tracks ticket tiers, prices and availability, detects changes, and alerts me.
The longer-term idea is buying tickets on Fatsoma and reselling them on TicketSwap.
I still need to check TicketSwap's resale price cap and Fatsoma's transfer terms.
Monitoring only for now. Automated buying would need checking against UK law
(bots buying beyond purchase limits are banned).

## Environment
- Arch Linux, Python, Neovim (LazyVim)
- Project folder: ~/Desktop/ticket-management-tool
- Python 3.14
- Venv: should be `.venv` in the project root (`source .venv/bin/activate`).
  Not created yet. Two old misspelled venvs need deleting once it exists:
  ~/Desktop/ticket-managment-tool/ (whole folder) and ./virtual/enviorment in this project.
- Dependencies: requests (TODO: add requirements.txt)
- TODO: add .gitignore for .venv/, virtual/, __pycache__/

## Current files
- fetch.py: calls the Fatsoma API with `requests` and saves the response to
  fixtures/payload.json (path built with `Path(__file__).parent / "fixtures"`).
  Working, but all code is at module level, so importing it fires a request and
  overwrites the fixture. Only fetches page 1 (12 of 20 events).
- fixtures/payload.json: a saved sample response.
- parser.py: in progress. Has load_payload(), which reads the fixture (temporary,
  the plan is to switch to the live API).
- main.py: empty.

## API
GET https://api.fatsoma.com/v1/events
Params:
  filter[status]=active
  filter[page.id]=cf1c5642-94c6-4078-a72a-125d49a7b90d
  filter[ends-at][gte]=<now, UTC, %Y-%m-%dT%H:%M:%S>
  include=location,ticket-options
  page[number]=1, page[size]=12
  sort=starts-at-day,relevance
  with-co-promoted=true
Use params=, timeout=10, raise_for_status().

## Response structure (JSON:API format)
- data: list of events (12 per page)
- included: related objects (ticket-options, locations, wait-lists, categories)
- meta: total-count (20), total-pages (2). Paginated: follow links.next.
- Event attributes: name, starts-at, ends-at, on-sale, expired, price-min/price-max
  (pence), currency, vanity-name, seo-name
- Event → tickets: data[i].relationships["ticket-options"].data = [{type, id}, ...]
  These point to items in `included` with type "ticket-options" and a matching id.
- Ticket-option attributes: name, price-sub-unit and transaction-fee-sub-unit (pence),
  on-sale-status ("available" / "sold_out"), amount-available, max-per-order,
  on-sale-at, off-sale-at, visible
- Tier names can repeat within an event, so key on the ticket-option id.
- The feed contains other events too (Insomnia at Phonox, Infernos, etc.),
  so filter by name for Milkshake.

## Parser plan (current step)
I want to develop against the live API (r.json()), not the fixture.
1. fetch_events() → returns r.json(); later handles pagination via links.next
2. build_ticket_lookup(payload) → dict {ticket_option_id: attributes}
3. parse_events(payload) → flat list of rows:
   {ticket_id, event_name, starts_at, tier_name, price_pence, fee_pence,
    status, amount_available}
   Use .get("data") or [] for events with no ticket options.
   Keep prices as integer pence.
   Put test prints under if __name__ == "__main__":

## Roadmap after the parser
1. Store snapshots in a database and diff each run against the last one
   (new event, tier goes on sale, price change, sell-out)
2. Alerts via a Discord webhook or Telegram bot
3. Run on a schedule with GitHub Actions cron. Runs are stateless, so use a
   hosted DB (Supabase/Neon Postgres) or commit the state file back to the repo.
4. Keep the polling rate polite to avoid rate limits or blocks.

## How I want to work
I'm learning Python. I write all the code and make all changes myself.
Don't edit, create, rename or delete files unless I explicitly ask you to.
By default: explain, review, point out bugs and suggest what to do next, and I'll implement it.
When I do ask you to change something, explain what you changed and why.
