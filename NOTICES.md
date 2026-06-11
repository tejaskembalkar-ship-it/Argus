# Notices

## Upstream attribution

- Argus is derived from ECC by affaan-m.
  Source: https://github.com/affaan-m/ECC

## Cross-repo dependency notice

- Argus optionally depends on Daedalus Hermes via `integrations/hermes/adapter.py`.
- This dependency is gated behind `HERMES_ENABLED` and does not bypass Argus governance checks.
