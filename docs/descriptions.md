## Val av Duckdb (ej snowflake)
#### motevering:
- ej vår "slutdatabas" - kommer använda Lancedb
- kommer inte påverka produkten
- snabbare (slipper users, roles osv)
- gratis
- inget star schema
- inte så stor datamängd
- dlt och dbt stödjer
- används bara i förbehandlingen (raw-staging-mart)
- få användare (mobprogrammerar)
- kan bytas ut mot snowflake senare om vi vill
Nackdelar
- endast en person åt gången som kan köra UI?

### Setup profiles.yml
https://docs.getdbt.com/docs/local/connect-data-platform/duckdb-setup?version=2
