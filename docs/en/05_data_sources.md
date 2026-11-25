# 05. Data sources

This document lists the families of sources the substrate can reach, with the access
route and the typical latency of each. Latency is the delay between the reference period
and the availability of the data, which is the quantity that determines whether a question
about the recent past can be answered.

| Family | Examples | Access route | Typical latency |
| --- | --- | --- | --- |
| Notifiable diseases | SINAN line lists, Ministry of Health open data (DEMAS) | Bulk files and REST API | Weeks to months |
| Mortality | SIM | Bulk files by state and year | Months |
| Live births | SINASC | Bulk files by state and year | Months |
| Hospital care | SIH, SIA, CIHA | Monthly files by state | Two to six months |
| Health establishments | CNES | Monthly files | One to three months |
| Immunisation | PNI dose records, adverse event reporting | Annual and monthly files | Months |
| Sanitation and water | SISAGUA | Annual files | Months |
| Primary care | Previne Brasil indicators, medical workforce programmes | REST API | Quarterly |
| Arbovirus surveillance | InfoDengue, Mosqlimate, ovitrap networks | REST API | Days to weeks |
| Vectors and environment | Vector occurrence, climate series, vegetation indices | REST API and raster services | Days |
| Genomics | Pathoplexus | REST API | Days to weeks |
| International surveillance | WHO, PAHO, ECDC, Eurostat, World Bank, UN Data | REST API | Months |
| Geography | IBGE boundaries, GADM administrative units | Bulk files | Annual |
| Regulated terminology and prices | SIGTAP, TUSS, health price database | Bulk files and API | Monthly |
| Scientific literature | PubMed, OpenAlex, CrossRef, arXiv, preprint servers | REST API | Immediate |

## How the catalogue is used

Every source is registered with a descriptor that states origin, licence, temporal
coverage, spatial resolution, refresh cadence and known quality problems. The planner
reads the descriptor before choosing a source. Two behaviours follow from this. A request
that falls outside the coverage of every registered source returns a statement of the gap
rather than a substitute dataset. A request whose answer depends on data that are still
being revised returns the analysis together with the extraction date, so the reader knows
what was available when the number was produced.

## Freshness as a finding

The table above is also a result. Questions about the most recent weeks can be answered
for arbovirus surveillance and for climate, and cannot be answered for mortality or for
hospital admissions. Users discover this through use, and the usage record shows that
freshness is one of the most frequent points of friction. Making the latency explicit is
therefore part of the design, not a caveat added afterwards.
